from __future__ import annotations

import argparse
import gc
import os
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


log = setup_logging("tp2.seed_sweep")


def safe_label(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in value)[:80] or "prompt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render the same prompt per target across many seeds and rank outputs.")
    parser.add_argument("--prompts", type=Path, default=Path("prompts/refinement_round42_seed_sweep_best.json"))
    parser.add_argument("--targets", type=Path, default=DEFAULT_TARGET_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--identity", default="round42_seed_sweep")
    parser.add_argument("--render-device", default="auto", choices=["auto", "cuda", "cpu", "mps"])
    parser.add_argument("--metric-device", default="cpu", choices=["cuda", "cpu", "mps"])
    parser.add_argument("--clip-model", default=None)
    parser.add_argument("--seed-offsets", nargs="*", type=int, default=list(range(0, 64)))
    parser.add_argument("--seed-map", type=Path, default=None,
                        help="Optional JSON mapping target filename to base seed, e.g. {'9338.png': 9375}.")
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--prompt-source", default="metric_best", choices=["metric_best", "visual_pick", "all"])
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--disable-progress-bar", action="store_true")
    parser.add_argument("--maxstack-scoring", action="store_true")
    return parser.parse_args()


def evaluate_seed_render(
    *,
    target_name: str,
    target_path: Path,
    target_image: Image.Image,
    target_clip: torch.Tensor,
    target_lpips: torch.Tensor,
    render_image: Image.Image,
    entry: dict[str, str],
    prompt_index: int,
    seed: int,
    seed_offset: int,
    clip_processor: Any,
    clip_model: Any,
    lpips_model: Any,
    metric_device: str,
    eval_cfg: EvalConfig,
    config: LCMConfig,
    use_maxstack: bool,
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
        "stage": "seed_sweep",
        "target_name": target_name,
        "target_path": str(target_path),
        "prompt_index": prompt_index,
        "prompt_id": entry["id"],
        "prompt_source": entry["source"],
        "prompt": entry["prompt"],
        "negative_prompt": entry.get("negative_prompt", ""),
        "render_seed": seed,
        "seed_offset": seed_offset,
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


def fit_square(image: Image.Image, size: int) -> Image.Image:
    image = image.copy()
    image.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), "white")
    canvas.paste(image, ((size - image.width) // 2, (size - image.height) // 2))
    return canvas


def make_contact_sheet(rows: list[dict[str, Any]], output: Path, top_k: int, thumb: int = 192) -> None:
    by_target: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_target.setdefault(row["target_name"], []).append(row)
    for group in by_target.values():
        group.sort(key=lambda row: int(row["rank"]))
    gap = 16
    label_h = 34
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
        draw.rectangle((gap, y, gap + thumb, y + label_h - 4), fill="white")
        draw.text((gap + 4, y + 2), f"{target_name} target", fill="black", font=font)
        for col_i, row in enumerate(group[:top_k], start=1):
            x = gap + col_i * (thumb + gap)
            render = fit_square(load_image(row["render_path"]), thumb)
            sheet.paste(render, (x, y + label_h))
            draw.rectangle((x, y, x + thumb, y + label_h - 4), fill="white")
            draw.text((x + 4, y + 2), f"rank {row['rank']} seed {row['render_seed']}", fill="black", font=font)
            draw.text((x + 4, y + 16), f"{row['prompt_source']}", fill="black", font=font)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def add_seed_sweep_scores(rows: list[dict[str, Any]], use_maxstack: bool) -> None:
    add_weighted_scores(rows)
    if not use_maxstack:
        for row in rows:
            row["seed_sweep_score"] = row["selection_score"]
        return
    from search_multiseed_validate import add_maxstack_scores

    add_maxstack_scores(rows)
    for row in rows:
        row["seed_sweep_score"] = row.get("maxstack_score", row["selection_score"])


def main() -> None:
    args = parse_args()
    if args.offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"

    config = LCMConfig()
    eval_cfg = EvalConfig(clip_model=args.clip_model or EvalConfig.clip_model, top_k=args.top_k)
    prompt_bank = normalise_prompt_entries(read_json(args.prompts))
    seed_map = read_json(args.seed_map) if args.seed_map else {}
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
    log.info("Seed offsets: %s", args.seed_offsets)

    all_rows: list[dict[str, Any]] = []
    final_rows: list[dict[str, Any]] = []
    total = 0
    for path in targets:
        entries = prompt_bank[path.name]
        if args.prompt_source != "all":
            entries = [entry for entry in entries if entry["source"].endswith(args.prompt_source)]
        total += len(entries) * len(args.seed_offsets)
    counter = 0

    for target_path in targets:
        target_name = target_path.name
        entries = prompt_bank[target_name]
        if args.prompt_source != "all":
            entries = [entry for entry in entries if entry["source"].endswith(args.prompt_source)]
        if not entries:
            continue
        target_image = load_image(target_path)
        target_clip = clip_image_embedding(target_image, clip_processor, clip_model, args.metric_device)
        target_lpips = pil_to_lpips_tensor(target_image, args.metric_device)
        base_seed = int(seed_map.get(target_name, seed_from_filename(target_path, config.seed)))
        target_rows: list[dict[str, Any]] = []
        image_dir = run_dir / safe_stem(target_path)
        image_dir.mkdir(parents=True, exist_ok=True)

        for prompt_index, entry in enumerate(entries, start=1):
            prompt_slug = safe_label(entry["source"])
            for offset in args.seed_offsets:
                counter += 1
                seed = base_seed + offset
                if counter == 1 or counter % 10 == 0:
                    log.info("[seed-sweep %d/%d] %s prompt %d seed %+d", counter, total, target_name, prompt_index, offset)
                render_image = render_prompt(
                    entry["prompt"], seed=seed, pipe=pipe, config=config, device=render_device,
                    negative_prompt=entry.get("negative_prompt", ""),
                )
                image_path = image_dir / f"{prompt_slug}_seed_{seed:05d}_offset_{offset:+04d}.png"
                render_image.save(image_path)
                row = evaluate_seed_render(
                    target_name=target_name, target_path=target_path, target_image=target_image,
                    target_clip=target_clip, target_lpips=target_lpips, render_image=render_image,
                    entry=entry, prompt_index=prompt_index, seed=seed, seed_offset=offset,
                    clip_processor=clip_processor, clip_model=clip_model, lpips_model=lpips_model,
                    metric_device=args.metric_device, eval_cfg=eval_cfg, config=config,
                    use_maxstack=args.maxstack_scoring,
                )
                row["render_path"] = str(image_path)
                target_rows.append(row)
                del render_image

        add_seed_sweep_scores(target_rows, args.maxstack_scoring)
        target_rows.sort(key=lambda row: -float(row["seed_sweep_score"]))
        for rank, row in enumerate(target_rows[: args.top_k], start=1):
            final = dict(row)
            final["rank"] = rank
            final_rows.append(final)
        write_csv(run_dir / f"{safe_stem(target_path)}_seed_sweep_metrics.csv", target_rows)
        all_rows.extend(target_rows)
        del target_clip, target_lpips

    write_csv(run_dir / "seed_sweep_metrics.csv", all_rows)
    write_csv(run_dir / f"top{args.top_k}_seed_sweep.csv", final_rows)
    if final_rows:
        make_contact_sheet(final_rows, run_dir / f"contact_sheet_top{args.top_k}_seed_sweep.jpg", args.top_k)
    write_json(run_dir / "summary.json", {
        "mode": "same prompt seed sweep",
        "prompt_source": args.prompt_source,
        "seed_offsets": args.seed_offsets,
        "maxstack_scoring": args.maxstack_scoring,
        "metrics": aggregate(all_rows, [
            "clip_iisim", "lpips_alex", "pixel_rmse_01", "pixel_ssim_01",
            "color_hist_sim", "edge_sim", "layout_sim", "visual_specific_score",
            "combined_score", "selection_score", "seed_sweep_score",
        ]),
    })
    log.info("Wrote seed-sweep top-k: %s", run_dir / f"top{args.top_k}_seed_sweep.csv")

    del pipe, clip_model, lpips_model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
