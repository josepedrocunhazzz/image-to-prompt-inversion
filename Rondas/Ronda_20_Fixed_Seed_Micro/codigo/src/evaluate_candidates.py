from __future__ import annotations

import argparse
import gc
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

import torch
from PIL import Image

from tp2_common import (
    EvalConfig,
    default_device,
    load_image,
    read_csv,
    setup_logging,
    write_csv,
    write_json,
)
from tp2_metrics import (
    add_combined_scores,
    aggregate,
    clip_image_embedding,
    load_clip,
    load_lpips,
    pil_to_lpips_tensor,
    pixel_metrics,
)

log = setup_logging("tp2.evaluate")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate rendered TP2 candidates and rank top-k prompts.")
    parser.add_argument("--manifest", type=Path, required=True, help="Path to manifest.csv or to its run directory.")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu", "mps"])
    parser.add_argument("--clip-model", default=None, help="Override CLIP model (default from EvalConfig).")
    parser.add_argument("--top-k", type=int, default=None, help="Override top-k (default from EvalConfig).")
    parser.add_argument("--copy-top", action="store_true", help="Copy selected renders into top3_selection/.")
    return parser.parse_args()


def resolve_manifest(path: Path) -> Path:
    if path.is_dir():
        path = path / "manifest.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def copy_top_rows(top_rows: list[dict[str, Any]], output_dir: Path) -> None:
    selection_dir = output_dir / "top3_selection"
    selection_dir.mkdir(parents=True, exist_ok=True)
    for row in top_rows:
        target_dir = selection_dir / row["target_name"].replace(".png", "")
        target_dir.mkdir(parents=True, exist_ok=True)
        source = Path(row["render_path"])
        destination = target_dir / f"rank_{int(row['rank']):02d}_{source.name}"
        shutil.copy2(source, destination)


def main() -> None:
    args = parse_args()
    eval_cfg = EvalConfig(
        clip_model=args.clip_model or EvalConfig.clip_model,
        top_k=args.top_k if args.top_k is not None else EvalConfig.top_k,
    )
    manifest_path = resolve_manifest(args.manifest)
    run_dir = manifest_path.parent
    device = default_device(args.device)
    log.info("Manifest: %s", manifest_path)
    log.info("Device: %s", device)
    log.info("CLIP model: %s | LPIPS net: %s | top-k: %d",
             eval_cfg.clip_model, eval_cfg.lpips_net, eval_cfg.top_k)

    rows = read_csv(manifest_path)
    if not rows:
        raise ValueError(f"Manifest is empty: {manifest_path}")

    clip_processor, clip_model = load_clip(eval_cfg.clip_model, device)
    lpips_model = load_lpips(eval_cfg.lpips_net, device)

    target_clip_cache: dict[str, torch.Tensor] = {}
    target_image_cache: dict[str, Image.Image] = {}
    metric_rows: list[dict[str, Any]] = []

    for index, row in enumerate(rows, start=1):
        target_path = row["target_path"]
        render_path = row["render_path"]

        if target_path not in target_image_cache:
            target_image_cache[target_path] = load_image(target_path)
        target_image = target_image_cache[target_path]
        render_image = load_image(render_path)
        if render_image.size != target_image.size:
            render_image = render_image.resize(target_image.size, Image.Resampling.BICUBIC)

        if target_path not in target_clip_cache:
            target_clip_cache[target_path] = clip_image_embedding(target_image, clip_processor, clip_model, device)
        target_clip = target_clip_cache[target_path]
        render_clip = clip_image_embedding(render_image, clip_processor, clip_model, device)
        clip_iisim = float((target_clip * render_clip).sum().item())

        target_lpips = pil_to_lpips_tensor(target_image, device)
        render_lpips = pil_to_lpips_tensor(render_image, device)
        with torch.no_grad():
            lpips_alex = float(lpips_model(target_lpips, render_lpips).item())

        pixel_mse, pixel_rmse = pixel_metrics(target_image, render_image)
        metric_row: dict[str, Any] = {
            **row,
            "clip_model": eval_cfg.clip_model,
            "clip_iisim": clip_iisim,
            "lpips_alex": lpips_alex,
            "pixel_mse_01": pixel_mse,
            "pixel_rmse_01": pixel_rmse,
        }
        metric_rows.append(metric_row)
        log.info("[%d/%d] %s #%s CLIP=%.4f LPIPS=%.4f RMSE=%.4f",
                 index, len(rows), row["target_name"], row["candidate_index"],
                 clip_iisim, lpips_alex, pixel_rmse)

    # Ranking
    add_combined_scores(metric_rows, eval_cfg.clip_weight, eval_cfg.lpips_weight, eval_cfg.rmse_weight)
    metric_rows.sort(key=lambda item: (item["target_name"], -float(item["combined_score"])))

    top_rows: list[dict[str, Any]] = []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in metric_rows:
        grouped[row["target_name"]].append(row)
    for target_name in sorted(grouped):
        ranked = sorted(grouped[target_name], key=lambda item: -float(item["combined_score"]))
        for rank, row in enumerate(ranked[: eval_cfg.top_k], start=1):
            row = dict(row)
            row["rank"] = rank
            top_rows.append(row)

    write_csv(run_dir / "metrics.csv", metric_rows)
    write_json(run_dir / "metrics.json", metric_rows)
    write_csv(run_dir / f"top{eval_cfg.top_k}.csv", top_rows)
    write_json(run_dir / f"top{eval_cfg.top_k}.json", top_rows)

    ranking_desc = (
        f"{eval_cfg.clip_weight:.2f}*normalised_clip"
        f" + {eval_cfg.lpips_weight:.2f}*inverse_normalised_lpips"
        f" + {eval_cfg.rmse_weight:.2f}*inverse_normalised_rmse, normalised per target"
    )
    summary = {
        "all_candidates": aggregate(
            metric_rows,
            ["clip_iisim", "lpips_alex", "pixel_mse_01", "pixel_rmse_01", "combined_score"],
        ),
        f"top{eval_cfg.top_k}": aggregate(
            top_rows,
            ["clip_iisim", "lpips_alex", "pixel_mse_01", "pixel_rmse_01", "combined_score"],
        ),
        "ranking_score": ranking_desc,
    }
    write_json(run_dir / "summary.json", summary)

    if args.copy_top:
        copy_top_rows(top_rows, run_dir)

    log.info("Wrote: %s", run_dir / "metrics.csv")
    log.info("Wrote: %s", run_dir / f"top{eval_cfg.top_k}.csv")
    log.info("Wrote: %s", run_dir / "summary.json")

    # Cleanup VRAM
    del clip_model, lpips_model, target_clip_cache
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
