from __future__ import annotations

import argparse
import gc
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

import torch
from PIL import Image

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
    visual_specific_metrics,
)

log = setup_logging("tp2.streaming")

# ---------------------------------------------------------------------------
# Default patience for early stopping (no improvement over N candidates).
# Keep disabled by default: CLIP-only early stopping can skip candidates that
# improve LPIPS/RMSE or visual geometry.
# ---------------------------------------------------------------------------
DEFAULT_PATIENCE = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Disk-light TP2 prompt search: render candidates in memory, score them, and save only top-k renders."
    )
    parser.add_argument("--prompts", type=Path, default=Path("prompts/refinement_round6_auto.json"))
    parser.add_argument("--targets", type=Path, default=DEFAULT_TARGET_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--identity", default="streaming_search")
    parser.add_argument("--render-device", default="auto", choices=["auto", "cuda", "cpu", "mps"])
    parser.add_argument("--metric-device", default="cpu", choices=["cuda", "cpu", "mps"])
    parser.add_argument("--clip-model", default=None, help="Override CLIP model (default from EvalConfig).")
    parser.add_argument("--top-k", type=int, default=None, help="Override top-k (default from EvalConfig).")
    parser.add_argument("--limit-per-target", type=int, default=0)
    parser.add_argument("--only", nargs="*", help="Optional target filenames, e.g. 1159_7.png 9338.png")
    parser.add_argument("--offline", action="store_true", help="Use only locally cached Hugging Face files.")
    parser.add_argument("--patience", type=int, default=DEFAULT_PATIENCE,
                        help="Early stopping: skip remaining candidates for a target after N consecutive non-improvements.")
    parser.add_argument("--no-early-stop", action="store_true", help="Disable early stopping.")
    parser.add_argument("--disable-progress-bar", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"

    config = LCMConfig()
    eval_cfg = EvalConfig(
        clip_model=args.clip_model or EvalConfig.clip_model,
        top_k=args.top_k if args.top_k is not None else EvalConfig.top_k,
    )
    targets = list_target_images(args.targets)
    if args.only:
        wanted = set(args.only)
        targets = [path for path in targets if path.name in wanted]
    if not targets:
        raise FileNotFoundError(f"No target images found in {args.targets}")

    prompt_bank = normalise_prompt_entries(read_json(args.prompts))
    target_by_name = {path.name: path for path in targets}
    local_files_only = args.offline

    log.info("Targets: %s", ", ".join(target_by_name))
    log.info("Prompt file: %s", args.prompts)
    log.info("CLIP model: %s | LPIPS net: %s | top-k: %d",
             eval_cfg.clip_model, eval_cfg.lpips_net, eval_cfg.top_k)
    early_stop_enabled = (not args.no_early_stop) and args.patience > 0
    log.info("Early stopping: %s (patience=%d)",
             "ON" if early_stop_enabled else "OFF", args.patience)

    pipe, render_device = load_lcm_pipeline(config, args.render_device)
    if hasattr(pipe, "set_progress_bar_config"):
        pipe.set_progress_bar_config(disable=args.disable_progress_bar)
    log.info("Render device: %s | Metric device: %s", render_device, args.metric_device)

    # Load metric models after the LCM pipeline to reduce peak memory during
    # the heaviest checkpoint load.
    clip_processor, clip_model = load_clip(
        eval_cfg.clip_model, args.metric_device, local_files_only=local_files_only,
    )
    lpips_model = load_lpips(eval_cfg.lpips_net, args.metric_device)

    run_dir = create_run_dir(args.output_dir, args.identity)
    log.info("Run directory: %s", run_dir)

    target_clip_cache: dict[str, torch.Tensor] = {}
    metric_rows: list[dict[str, Any]] = []

    # Pre-count total for progress display.
    total = 0
    for target_name in target_by_name:
        entries = prompt_bank.get(target_name, [])
        if args.limit_per_target > 0:
            entries = entries[: args.limit_per_target]
        total += len(entries)

    counter = 0
    for target_name, target_path in target_by_name.items():
        entries = prompt_bank.get(target_name, [])
        if args.limit_per_target > 0:
            entries = entries[: args.limit_per_target]
        if not entries:
            log.info("Skipping target without prompts: %s", target_name)
            continue

        target_image = load_image(target_path)
        target_clip_cache[str(target_path)] = clip_image_embedding(
            target_image, clip_processor, clip_model, args.metric_device,
        )
        target_lpips = pil_to_lpips_tensor(target_image, args.metric_device)
        seed = seed_from_filename(target_path, config.seed)

        # Early stopping state for this target.
        best_clip_for_target = -1.0
        no_improvement_count = 0
        skipped = 0

        for index, entry in enumerate(entries, start=1):
            counter += 1
            prompt = entry["prompt"]
            negative_prompt = entry.get("negative_prompt", "")

            # Early stopping check.
            if early_stop_enabled and no_improvement_count >= args.patience:
                skipped += 1
                continue

            log.info("[%d/%d] %s #%03d: %s", counter, total, target_name, index, prompt)
            render_image = render_prompt(
                prompt,
                seed=seed,
                pipe=pipe,
                config=config,
                device=render_device,
                negative_prompt=negative_prompt,
            )
            if render_image.size != target_image.size:
                render_image = render_image.resize(target_image.size, Image.Resampling.BICUBIC)

            render_clip = clip_image_embedding(render_image, clip_processor, clip_model, args.metric_device)
            clip_iisim = float((target_clip_cache[str(target_path)] * render_clip).sum().item())

            render_lpips = pil_to_lpips_tensor(render_image, args.metric_device)
            with torch.no_grad():
                lpips_alex = float(lpips_model(target_lpips, render_lpips).item())

            pixel_mse, pixel_rmse, pixel_ssim = pixel_metrics_with_ssim(target_image, render_image)
            visual_metrics = visual_specific_metrics(target_image, render_image)
            metric_rows.append(
                {
                    "target_name": target_name,
                    "target_path": str(target_path),
                    "render_seed": seed,
                    "candidate_index": index,
                    "prompt_id": entry["id"],
                    "prompt_source": entry["source"],
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "clip_model": eval_cfg.clip_model,
                    "clip_iisim": clip_iisim,
                    "lpips_alex": lpips_alex,
                    "pixel_mse_01": pixel_mse,
                    "pixel_rmse_01": pixel_rmse,
                    "pixel_ssim_01": pixel_ssim,
                    **visual_metrics,
                    "model_id": config.model_id,
                    "num_inference_steps": config.num_inference_steps,
                    "guidance_scale": config.guidance_scale,
                    "original_inference_steps": config.lcm_origin_steps,
                    "width": config.width,
                    "height": config.height,
                }
            )

            # Track early stopping based on CLIP (the dominant metric).
            if clip_iisim > best_clip_for_target:
                best_clip_for_target = clip_iisim
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            # Drop references promptly; the image will be re-rendered only if it reaches top-k.
            del render_image, render_clip, render_lpips

        if skipped:
            log.info("Early-stopped %s: skipped %d candidates after %d without improvement.",
                     target_name, skipped, args.patience)

    # Ranking & output.
    add_weighted_scores(metric_rows)
    write_csv(run_dir / "metrics.csv", metric_rows)
    write_json(run_dir / "metrics.json", metric_rows)

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in metric_rows:
        grouped[row["target_name"]].append(row)

    top_rows: list[dict[str, Any]] = []
    for target_name in sorted(grouped):
        ranked = sorted(grouped[target_name], key=lambda item: -float(item.get("selection_score", item["combined_score"])))
        target_path = Path(ranked[0]["target_path"])
        seed = int(ranked[0]["render_seed"])
        target_output_dir = run_dir / safe_stem(target_path)
        target_output_dir.mkdir(parents=True, exist_ok=True)

        for rank, row in enumerate(ranked[: eval_cfg.top_k], start=1):
            top_row = dict(row)
            render_image = render_prompt(
                top_row["prompt"],
                seed=seed,
                pipe=pipe,
                config=config,
                device=render_device,
                negative_prompt=top_row.get("negative_prompt", ""),
            )
            image_path = target_output_dir / f"rank_{rank:02d}_candidate_{int(top_row['candidate_index']):03d}.png"
            render_image.save(image_path)
            top_row["rank"] = rank
            top_row["render_path"] = str(image_path)
            top_rows.append(top_row)

    write_csv(run_dir / f"top{eval_cfg.top_k}.csv", top_rows)
    write_json(run_dir / f"top{eval_cfg.top_k}.json", top_rows)

    ranking_desc = (
        "target-specific weighted normalised CLIP/LPIPS/RMSE/SSIM/color/edge/layout plus a small Pareto-front bonus"
    )
    summary = {
        "all_candidates": aggregate(
            metric_rows,
            [
                "clip_iisim", "lpips_alex", "pixel_mse_01", "pixel_rmse_01", "pixel_ssim_01",
                "color_hist_sim", "edge_sim", "layout_sim", "visual_specific_score",
                "combined_score", "selection_score",
            ],
        ),
        f"top{eval_cfg.top_k}": aggregate(
            top_rows,
            [
                "clip_iisim", "lpips_alex", "pixel_mse_01", "pixel_rmse_01", "pixel_ssim_01",
                "color_hist_sim", "edge_sim", "layout_sim", "visual_specific_score",
                "combined_score", "selection_score",
            ],
        ),
        "ranking_score": ranking_desc,
        "mode": "streaming: candidates rendered in memory; only top-k images saved",
    }
    write_json(run_dir / "summary.json", summary)
    log.info("Wrote: %s", run_dir / "metrics.csv")
    log.info("Wrote: %s", run_dir / f"top{eval_cfg.top_k}.csv")
    log.info("Wrote: %s", run_dir / "summary.json")

    # Cleanup VRAM.
    del pipe, clip_model, lpips_model, target_clip_cache
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
