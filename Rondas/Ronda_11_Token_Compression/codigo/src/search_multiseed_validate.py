from __future__ import annotations

import argparse
import gc
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

import torch
from PIL import Image, ImageDraw, ImageFont

from tp2_common import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TARGET_DIR,
    EvalConfig,
    LCMConfig,
    create_run_dir,
    list_target_images,
    load_image,
    load_lcm_pipeline,
    normalise_prompt_entries,
    read_json,
    render_prompt,
    safe_stem,
    seed_from_filename,
    setup_logging,
    write_csv,
    write_json,
)
from tp2_metrics import (
    add_weighted_scores,
    aggregate,
    clip_image_embedding,
    load_clip,
    load_lpips,
    pil_to_lpips_tensor,
    pixel_metrics_with_ssim,
    target_region_metrics,
    visual_specific_metrics,
)


log = setup_logging("tp2.multiseed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Two-stage TP2 prompt search: fixed-seed search, ensemble candidate selection, multi-seed validation, fixed-seed final render."
    )
    parser.add_argument("--prompts", type=Path, default=Path("prompts/refinement_ronda_10_hybrid_repair.json"))
    parser.add_argument("--targets", type=Path, default=DEFAULT_TARGET_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--identity", default="ronda_10_multiseed")
    parser.add_argument("--render-device", default="auto", choices=["auto", "cuda", "cpu", "mps"])
    parser.add_argument("--metric-device", default="cpu", choices=["cuda", "cpu", "mps"])
    parser.add_argument("--clip-model", default=None)
    parser.add_argument("--top-k", type=int, default=12, help="Final fixed-seed renders saved per target.")
    parser.add_argument("--stage1-save-k", type=int, default=20, help="Fixed-seed stage-1 rows saved per target for audit.")
    parser.add_argument("--validation-top-n", type=int, default=30, help="Prompt candidates validated with auxiliary seeds per target.")
    parser.add_argument("--ensemble-per-metric", type=int, default=8, help="Extra candidates selected from each metric ranking.")
    parser.add_argument("--limit-per-target", type=int, default=0)
    parser.add_argument("--seed-offsets", nargs="*", type=int, default=[1, 2, 3], help="Auxiliary offsets added to each target seed.")
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--disable-progress-bar", action="store_true")
    parser.add_argument("--maxstack-scoring", action="store_true",
                        help="Use target-specific region-aware heuristics in candidate selection and robustness scoring.")
    return parser.parse_args()


def evaluate_render(
    *,
    target_name: str,
    target_path: Path,
    target_image: Image.Image,
    target_clip: torch.Tensor,
    target_lpips: torch.Tensor,
    render_image: Image.Image,
    entry: dict[str, str],
    candidate_index: int,
    seed: int,
    seed_role: str,
    stage: str,
    clip_processor: Any,
    clip_model: Any,
    lpips_model: Any,
    metric_device: str,
    eval_cfg: EvalConfig,
    config: LCMConfig,
    use_maxstack: bool = False,
) -> dict[str, Any]:
    if render_image.size != target_image.size:
        render_image = render_image.resize(target_image.size, Image.Resampling.BICUBIC)
    render_clip = clip_image_embedding(render_image, clip_processor, clip_model, metric_device)
    clip_iisim = float((target_clip * render_clip).sum().item())
    render_lpips = pil_to_lpips_tensor(render_image, metric_device)
    with torch.no_grad():
        lpips_alex = float(lpips_model(target_lpips, render_lpips).item())
    pixel_mse, pixel_rmse, pixel_ssim = pixel_metrics_with_ssim(target_image, render_image)
    visual_metrics = visual_specific_metrics(target_image, render_image)
    region_metrics = target_region_metrics(target_name, target_image, render_image) if use_maxstack else {}
    return {
        "stage": stage,
        "target_name": target_name,
        "target_path": str(target_path),
        "render_seed": seed,
        "seed_role": seed_role,
        "candidate_index": candidate_index,
        "prompt_id": entry["id"],
        "prompt_source": entry["source"],
        "prompt": entry["prompt"],
        "negative_prompt": entry.get("negative_prompt", ""),
        "clip_model": eval_cfg.clip_model,
        "clip_iisim": clip_iisim,
        "lpips_alex": lpips_alex,
        "pixel_mse_01": pixel_mse,
        "pixel_rmse_01": pixel_rmse,
        "pixel_ssim_01": pixel_ssim,
        **visual_metrics,
        **region_metrics,
        "model_id": config.model_id,
        "num_inference_steps": config.num_inference_steps,
        "guidance_scale": config.guidance_scale,
        "original_inference_steps": config.lcm_origin_steps,
        "width": config.width,
        "height": config.height,
    }


def select_ensemble_candidates(rows: list[dict[str, Any]], validation_top_n: int, per_metric: int) -> list[dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    rankings = [
        ("selection_score", True),
        ("combined_score", True),
        ("clip_iisim", True),
        ("lpips_alex", False),
        ("pixel_rmse_01", False),
        ("pixel_ssim_01", True),
        ("color_hist_sim", True),
        ("edge_sim", True),
        ("layout_sim", True),
        ("visual_specific_score", True),
        ("region_score", True),
        ("heuristic_score", True),
        ("maxstack_score", True),
    ]
    for metric, higher in rankings:
        ranked = sorted(rows, key=lambda row: float(row.get(metric, 0.0)), reverse=higher)
        take = validation_top_n if metric == "selection_score" else per_metric
        for row in ranked[:take]:
            selected.setdefault(row["prompt_id"], row)
    ranked_selected = sorted(selected.values(), key=lambda row: -float(row.get("maxstack_score", row.get("selection_score", row["combined_score"]))))
    cap = validation_top_n + per_metric * 4
    return ranked_selected[:cap]


def add_maxstack_scores(rows: list[dict[str, Any]]) -> None:
    by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_target[row["target_name"]].append(row)
    for group in by_target.values():
        if not group or "region_score" not in group[0]:
            for row in group:
                row["maxstack_score"] = row.get("selection_score", row.get("combined_score", 0.0))
            continue
        region_good = normalise_metric(group, "region_score", True)
        heuristic_good = normalise_metric(group, "heuristic_score", True)
        visual_good = normalise_metric(group, "visual_specific_score", True)
        for row, region, heuristic, visual in zip(group, region_good, heuristic_good, visual_good):
            row["region_norm"] = region
            row["heuristic_norm"] = heuristic
            row["maxstack_score"] = (
                0.58 * float(row.get("selection_score", row.get("combined_score", 0.0))) +
                0.20 * region +
                0.14 * heuristic +
                0.08 * visual
            )


def normalise_metric(rows: list[dict[str, Any]], field: str, higher_is_better: bool) -> list[float]:
    values = [float(row.get(field, 0.0)) for row in rows]
    if not values:
        return []
    lo = min(values)
    hi = max(values)
    if abs(hi - lo) < 1e-12:
        return [0.5 for _ in values]
    scaled = [(value - lo) / (hi - lo) for value in values]
    return scaled if higher_is_better else [1.0 - value for value in scaled]


def aggregate_validation(
    stage1_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    use_maxstack: bool = False,
) -> list[dict[str, Any]]:
    stage1_by_prompt = {row["prompt_id"]: row for row in stage1_rows}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in validation_rows:
        grouped[row["prompt_id"]].append(row)
    result: list[dict[str, Any]] = []
    for prompt_id, rows in grouped.items():
        fixed = stage1_by_prompt[prompt_id]
        mean_selection = sum(float(row["selection_score"]) for row in rows) / len(rows)
        mean_combined = sum(float(row["combined_score"]) for row in rows) / len(rows)
        mean_clip = sum(float(row["clip_iisim"]) for row in rows) / len(rows)
        mean_visual = sum(float(row["visual_specific_score"]) for row in rows) / len(rows)
        mean_region = sum(float(row.get("region_score", 0.0)) for row in rows) / len(rows)
        mean_heuristic = sum(float(row.get("heuristic_score", 0.0)) for row in rows) / len(rows)
        worst_selection = min(float(row["selection_score"]) for row in rows)
        best_selection = max(float(row["selection_score"]) for row in rows)
        fixed_base = float(fixed.get("maxstack_score" if use_maxstack else "selection_score", fixed["selection_score"]))
        aux_base_values = [
            float(row.get("maxstack_score" if use_maxstack else "selection_score", row["selection_score"]))
            for row in rows
        ]
        mean_base = sum(aux_base_values) / len(aux_base_values)
        worst_base = min(aux_base_values)
        best_base = max(aux_base_values)
        robustness_score = (
            0.50 * fixed_base +
            0.25 * mean_base +
            0.15 * best_base +
            0.10 * worst_base
        )
        result.append({
            **fixed,
            "stage1_selection_score": fixed["selection_score"],
            "stage1_combined_score": fixed["combined_score"],
            "validation_count": len(rows),
            "validation_mean_selection": mean_selection,
            "validation_mean_combined": mean_combined,
            "validation_mean_clip": mean_clip,
            "validation_mean_visual": mean_visual,
            "validation_mean_region": mean_region,
            "validation_mean_heuristic": mean_heuristic,
            "validation_worst_selection": worst_selection,
            "validation_best_selection": best_selection,
            "robustness_score": robustness_score,
        })
    return sorted(result, key=lambda row: -float(row["robustness_score"]))


def fit_square(image: Image.Image, size: int) -> Image.Image:
    image = image.copy()
    image.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), "white")
    canvas.paste(image, ((size - image.width) // 2, (size - image.height) // 2))
    return canvas


def make_contact_sheet(rows: list[dict[str, Any]], output: Path, top_k: int, thumb: int = 192) -> None:
    by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_target[row["target_name"]].append(row)
    for group in by_target.values():
        group.sort(key=lambda row: int(row["rank"]))
    gap = 16
    label_h = 24
    cols = min(top_k + 1, 7)
    width = cols * thumb + (cols + 1) * gap
    height = len(by_target) * (thumb + label_h + gap) + gap
    sheet = Image.new("RGB", (width, height), (245, 245, 245))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for row_i, target_name in enumerate(sorted(by_target)):
        y = gap + row_i * (thumb + label_h + gap)
        group = by_target[target_name]
        target = fit_square(load_image(group[0]["target_path"]), thumb)
        sheet.paste(target, (gap, y + label_h))
        draw.rectangle((gap, y, gap + 180, y + 18), fill="white")
        draw.text((gap + 4, y + 2), f"{target_name} target", fill="black", font=font)
        for col_i, row in enumerate(group[: top_k], start=1):
            x = gap + col_i * (thumb + gap)
            render = fit_square(load_image(row["render_path"]), thumb)
            sheet.paste(render, (x, y + label_h))
            draw.rectangle((x, y, x + 180, y + 18), fill="white")
            draw.text((x + 4, y + 2), f"rank {row['rank']} cand {row['candidate_index']}", fill="black", font=font)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def main() -> None:
    args = parse_args()
    if args.offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"

    config = LCMConfig()
    eval_cfg = EvalConfig(clip_model=args.clip_model or EvalConfig.clip_model, top_k=args.top_k)
    prompt_bank = normalise_prompt_entries(read_json(args.prompts))
    targets = list_target_images(args.targets)
    if args.only:
        wanted = set(args.only)
        targets = [path for path in targets if path.name in wanted]
    targets = [path for path in targets if path.name in prompt_bank]
    if not targets:
        raise FileNotFoundError("No matching targets for prompt bank.")

    pipe, render_device = load_lcm_pipeline(config, args.render_device)
    if hasattr(pipe, "set_progress_bar_config"):
        pipe.set_progress_bar_config(disable=args.disable_progress_bar)
    clip_processor, clip_model = load_clip(eval_cfg.clip_model, args.metric_device, local_files_only=args.offline)
    lpips_model = load_lpips(eval_cfg.lpips_net, args.metric_device)

    run_dir = create_run_dir(args.output_dir, args.identity)
    log.info("Run directory: %s", run_dir)
    log.info("Stage 1 fixed-seed search, then validating top candidates with offsets: %s", args.seed_offsets)

    all_stage1_rows: list[dict[str, Any]] = []
    all_validation_rows: list[dict[str, Any]] = []
    all_final_rows: list[dict[str, Any]] = []
    total = sum(
        len(prompt_bank[path.name][: args.limit_per_target or None])
        for path in targets
    )
    counter = 0

    for target_path in targets:
        target_name = target_path.name
        entries = prompt_bank[target_name]
        if args.limit_per_target > 0:
            entries = entries[: args.limit_per_target]
        target_image = load_image(target_path)
        target_clip = clip_image_embedding(target_image, clip_processor, clip_model, args.metric_device)
        target_lpips = pil_to_lpips_tensor(target_image, args.metric_device)
        fixed_seed = seed_from_filename(target_path, config.seed)

        stage1_rows: list[dict[str, Any]] = []
        for candidate_index, entry in enumerate(entries, start=1):
            counter += 1
            if counter == 1 or counter % 10 == 0:
                log.info("[stage1 %d/%d] %s #%03d", counter, total, target_name, candidate_index)
            render_image = render_prompt(
                entry["prompt"], seed=fixed_seed, pipe=pipe, config=config, device=render_device,
                negative_prompt=entry.get("negative_prompt", ""),
            )
            row = evaluate_render(
                target_name=target_name, target_path=target_path, target_image=target_image,
                target_clip=target_clip, target_lpips=target_lpips, render_image=render_image,
                entry=entry, candidate_index=candidate_index, seed=fixed_seed, seed_role="fixed",
                stage="stage1_fixed_seed", clip_processor=clip_processor, clip_model=clip_model,
                lpips_model=lpips_model, metric_device=args.metric_device, eval_cfg=eval_cfg, config=config,
                use_maxstack=args.maxstack_scoring,
            )
            stage1_rows.append(row)
            del render_image

        add_weighted_scores(stage1_rows)
        if args.maxstack_scoring:
            add_maxstack_scores(stage1_rows)
        all_stage1_rows.extend(stage1_rows)
        ranking_field = "maxstack_score" if args.maxstack_scoring else "selection_score"
        stage1_top = sorted(stage1_rows, key=lambda row: -float(row.get(ranking_field, row["combined_score"])))[: args.stage1_save_k]
        write_csv(run_dir / f"{safe_stem(target_path)}_stage1_fixed_seed_top{args.stage1_save_k}.csv", stage1_top)

        selected = select_ensemble_candidates(stage1_rows, args.validation_top_n, args.ensemble_per_metric)
        write_csv(run_dir / f"{safe_stem(target_path)}_selected_for_multiseed.csv", selected)
        log.info("%s selected for multi-seed: %d", target_name, len(selected))

        validation_rows: list[dict[str, Any]] = []
        id_to_entry = {entry["id"]: (index, entry) for index, entry in enumerate(entries, start=1)}
        for selected_index, fixed_row in enumerate(selected, start=1):
            candidate_index, entry = id_to_entry[fixed_row["prompt_id"]]
            for offset in args.seed_offsets:
                aux_seed = fixed_seed + offset
                log.info("[validate %s %02d/%02d] cand %03d seed %+d", target_name, selected_index, len(selected), candidate_index, offset)
                render_image = render_prompt(
                    entry["prompt"], seed=aux_seed, pipe=pipe, config=config, device=render_device,
                    negative_prompt=entry.get("negative_prompt", ""),
                )
                row = evaluate_render(
                    target_name=target_name, target_path=target_path, target_image=target_image,
                    target_clip=target_clip, target_lpips=target_lpips, render_image=render_image,
                    entry=entry, candidate_index=candidate_index, seed=aux_seed, seed_role=f"offset_{offset:+d}",
                    stage="stage2_aux_seed_validation", clip_processor=clip_processor, clip_model=clip_model,
                    lpips_model=lpips_model, metric_device=args.metric_device, eval_cfg=eval_cfg, config=config,
                    use_maxstack=args.maxstack_scoring,
                )
                validation_rows.append(row)
                del render_image
        add_weighted_scores(validation_rows)
        if args.maxstack_scoring:
            add_maxstack_scores(validation_rows)
        all_validation_rows.extend(validation_rows)

        robust_rows = aggregate_validation(stage1_rows, validation_rows, use_maxstack=args.maxstack_scoring)
        write_csv(run_dir / f"{safe_stem(target_path)}_robust_prompt_ranking.csv", robust_rows)
        target_output_dir = run_dir / safe_stem(target_path)
        target_output_dir.mkdir(parents=True, exist_ok=True)
        for rank, row in enumerate(robust_rows[: args.top_k], start=1):
            render_image = render_prompt(
                row["prompt"], seed=fixed_seed, pipe=pipe, config=config, device=render_device,
                negative_prompt=row.get("negative_prompt", ""),
            )
            image_path = target_output_dir / f"rank_{rank:02d}_candidate_{int(row['candidate_index']):03d}.png"
            render_image.save(image_path)
            final_row = dict(row)
            final_row["stage"] = "stage3_fixed_seed_final"
            final_row["rank"] = rank
            final_row["render_path"] = str(image_path)
            final_row["render_seed"] = fixed_seed
            final_row["seed_role"] = "fixed_final"
            all_final_rows.append(final_row)

        del target_clip, target_lpips

    write_csv(run_dir / "stage1_fixed_seed_metrics.csv", all_stage1_rows)
    write_csv(run_dir / "stage2_aux_seed_metrics.csv", all_validation_rows)
    write_csv(run_dir / f"top{args.top_k}_robust_fixed_seed.csv", all_final_rows)
    if all_final_rows:
        make_contact_sheet(all_final_rows, run_dir / f"contact_sheet_top{args.top_k}_robust.jpg", args.top_k)
    summary = {
        "mode": "two-stage: fixed-seed full search, ensemble metric selection, auxiliary multi-seed validation, fixed-seed final renders",
        "maxstack_scoring": args.maxstack_scoring,
        "seed_offsets": args.seed_offsets,
        "stage1": aggregate(all_stage1_rows, ["clip_iisim", "lpips_alex", "pixel_rmse_01", "pixel_ssim_01", "color_hist_sim", "edge_sim", "layout_sim", "visual_specific_score", "combined_score", "selection_score"] + (["region_score", "heuristic_score", "maxstack_score"] if args.maxstack_scoring else [])),
        "validation": aggregate(all_validation_rows, ["clip_iisim", "lpips_alex", "pixel_rmse_01", "pixel_ssim_01", "color_hist_sim", "edge_sim", "layout_sim", "visual_specific_score", "combined_score", "selection_score"] + (["region_score", "heuristic_score", "maxstack_score"] if args.maxstack_scoring else [])),
    }
    write_json(run_dir / "summary.json", summary)
    log.info("Wrote final robust top-k: %s", run_dir / f"top{args.top_k}_robust_fixed_seed.csv")

    del pipe, clip_model, lpips_model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
