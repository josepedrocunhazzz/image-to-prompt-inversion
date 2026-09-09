"""Shared evaluation metrics for TP2 prompt inversion pipeline.

Consolidates CLIP, LPIPS, pixel-level metrics and ranking logic
previously duplicated across evaluate_candidates.py and search_streaming_topk.py.
"""
from __future__ import annotations

import math
from collections import defaultdict
from typing import Any

import numpy as np
import torch
from PIL import Image
from torchvision.transforms import functional as TF


# ---------------------------------------------------------------------------
# Tensor helpers
# ---------------------------------------------------------------------------

def pil_to_lpips_tensor(image: Image.Image, device: str) -> torch.Tensor:
    """Convert a PIL image to a [-1, 1] tensor suitable for LPIPS."""
    tensor = TF.to_tensor(image).unsqueeze(0)
    return (tensor * 2.0 - 1.0).to(device)


# ---------------------------------------------------------------------------
# Pixel-level metrics
# ---------------------------------------------------------------------------

def global_ssim(target_arr: np.ndarray, render_arr: np.ndarray) -> float:
    """Return a compact global SSIM approximation for arrays in [0, 1]."""
    weights = np.asarray([0.299, 0.587, 0.114], dtype=np.float32)
    if target_arr.ndim == 3:
        target_gray = (target_arr[..., :3] * weights).sum(axis=2)
        render_gray = (render_arr[..., :3] * weights).sum(axis=2)
    else:
        target_gray = target_arr
        render_gray = render_arr
    c1 = 0.01 ** 2
    c2 = 0.03 ** 2
    mu_x = float(target_gray.mean())
    mu_y = float(render_gray.mean())
    var_x = float(((target_gray - mu_x) ** 2).mean())
    var_y = float(((render_gray - mu_y) ** 2).mean())
    cov_xy = float(((target_gray - mu_x) * (render_gray - mu_y)).mean())
    denom = (mu_x ** 2 + mu_y ** 2 + c1) * (var_x + var_y + c2)
    if abs(denom) < 1e-12:
        return 0.0
    return float(max(-1.0, min(1.0, ((2 * mu_x * mu_y + c1) * (2 * cov_xy + c2)) / denom)))


def pixel_metrics(target: Image.Image, render: Image.Image) -> tuple[float, float]:
    """Return (MSE, RMSE) in [0, 1] scale between *target* and *render*."""
    if target.size != render.size:
        render = render.resize(target.size, Image.Resampling.BICUBIC)
    target_arr = np.asarray(target, dtype=np.float32) / 255.0
    render_arr = np.asarray(render, dtype=np.float32) / 255.0
    mse = float(np.mean((target_arr - render_arr) ** 2))
    return mse, float(math.sqrt(mse))


def pixel_metrics_with_ssim(target: Image.Image, render: Image.Image) -> tuple[float, float, float]:
    """Return (MSE, RMSE, global SSIM) in [0, 1] image scale."""
    if target.size != render.size:
        render = render.resize(target.size, Image.Resampling.BICUBIC)
    target_arr = np.asarray(target, dtype=np.float32) / 255.0
    render_arr = np.asarray(render, dtype=np.float32) / 255.0
    mse = float(np.mean((target_arr - render_arr) ** 2))
    return mse, float(math.sqrt(mse)), global_ssim(target_arr, render_arr)


def _rgb_arrays(target: Image.Image, render: Image.Image) -> tuple[np.ndarray, np.ndarray]:
    if target.size != render.size:
        render = render.resize(target.size, Image.Resampling.BICUBIC)
    target_arr = np.asarray(target.convert("RGB"), dtype=np.float32) / 255.0
    render_arr = np.asarray(render.convert("RGB"), dtype=np.float32) / 255.0
    return target_arr, render_arr


def color_histogram_similarity(target_arr: np.ndarray, render_arr: np.ndarray, bins: int = 32) -> float:
    """Return mean per-channel histogram intersection in [0, 1]."""
    scores = []
    for channel in range(3):
        target_hist, _ = np.histogram(target_arr[..., channel], bins=bins, range=(0.0, 1.0), density=False)
        render_hist, _ = np.histogram(render_arr[..., channel], bins=bins, range=(0.0, 1.0), density=False)
        target_hist = target_hist.astype(np.float64)
        render_hist = render_hist.astype(np.float64)
        target_total = target_hist.sum() or 1.0
        render_total = render_hist.sum() or 1.0
        target_hist /= target_total
        render_hist /= render_total
        scores.append(float(np.minimum(target_hist, render_hist).sum()))
    return float(np.mean(scores))


def _sobel_edges(gray: np.ndarray) -> np.ndarray:
    padded = np.pad(gray, 1, mode="edge")
    gx = (
        -padded[:-2, :-2] - 2 * padded[1:-1, :-2] - padded[2:, :-2]
        + padded[:-2, 2:] + 2 * padded[1:-1, 2:] + padded[2:, 2:]
    )
    gy = (
        -padded[:-2, :-2] - 2 * padded[:-2, 1:-1] - padded[:-2, 2:]
        + padded[2:, :-2] + 2 * padded[2:, 1:-1] + padded[2:, 2:]
    )
    edges = np.sqrt(gx * gx + gy * gy)
    return edges / (float(edges.max()) + 1e-8)


def edge_similarity(target_arr: np.ndarray, render_arr: np.ndarray) -> tuple[float, float]:
    """Return (edge_rmse, edge_similarity) using Sobel luminance maps."""
    weights = np.asarray([0.299, 0.587, 0.114], dtype=np.float32)
    target_edges = _sobel_edges((target_arr[..., :3] * weights).sum(axis=2))
    render_edges = _sobel_edges((render_arr[..., :3] * weights).sum(axis=2))
    rmse = float(math.sqrt(float(np.mean((target_edges - render_edges) ** 2))))
    return rmse, float(max(0.0, min(1.0, 1.0 - rmse)))


def _saliency_center(arr: np.ndarray) -> tuple[float, float, float, float]:
    gray = (arr[..., :3] * np.asarray([0.299, 0.587, 0.114], dtype=np.float32)).sum(axis=2)
    channel_max = arr.max(axis=2)
    channel_min = arr.min(axis=2)
    saliency = np.abs(gray - float(np.median(gray))) + 0.5 * (channel_max - channel_min)
    saliency = np.maximum(saliency, 0.0)
    total = float(saliency.sum())
    height, width = saliency.shape
    if total < 1e-8:
        return 0.5, 0.5, 0.5, 0.5
    yy, xx = np.mgrid[0:height, 0:width]
    cx = float((saliency * xx).sum() / total / max(1, width - 1))
    cy = float((saliency * yy).sum() / total / max(1, height - 1))
    sx = float(math.sqrt(float((saliency * ((xx / max(1, width - 1)) - cx) ** 2).sum() / total)))
    sy = float(math.sqrt(float((saliency * ((yy / max(1, height - 1)) - cy) ** 2).sum() / total)))
    return cx, cy, sx, sy


def layout_similarity(target_arr: np.ndarray, render_arr: np.ndarray) -> float:
    """Compare rough visual mass center and spread in [0, 1]."""
    target_center = _saliency_center(target_arr)
    render_center = _saliency_center(render_arr)
    distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(target_center, render_center)))
    return float(max(0.0, min(1.0, 1.0 - distance)))


def visual_specific_metrics(target: Image.Image, render: Image.Image) -> dict[str, float]:
    """Cheap visual metrics that catch color, contour and layout failures."""
    target_arr, render_arr = _rgb_arrays(target, render)
    edge_rmse, edge_sim = edge_similarity(target_arr, render_arr)
    color_sim = color_histogram_similarity(target_arr, render_arr)
    layout_sim = layout_similarity(target_arr, render_arr)
    return {
        "color_hist_sim": color_sim,
        "edge_rmse": edge_rmse,
        "edge_sim": edge_sim,
        "layout_sim": layout_sim,
        "visual_specific_score": 0.45 * color_sim + 0.35 * edge_sim + 0.20 * layout_sim,
    }


def _crop_fraction(arr: np.ndarray, box: tuple[float, float, float, float]) -> np.ndarray:
    height, width = arr.shape[:2]
    x0, y0, x1, y1 = box
    left = max(0, min(width - 1, int(round(x0 * width))))
    top = max(0, min(height - 1, int(round(y0 * height))))
    right = max(left + 1, min(width, int(round(x1 * width))))
    bottom = max(top + 1, min(height, int(round(y1 * height))))
    return arr[top:bottom, left:right]


def _horizontal_asymmetry(arr: np.ndarray) -> float:
    gray = (arr[..., :3] * np.asarray([0.299, 0.587, 0.114], dtype=np.float32)).sum(axis=2)
    flipped = np.flip(gray, axis=1)
    return float(np.mean(np.abs(gray - flipped)))


def _teal_fraction(arr: np.ndarray) -> float:
    red = arr[..., 0]
    green = arr[..., 1]
    blue = arr[..., 2]
    chroma = arr.max(axis=2) - arr.min(axis=2)
    mask = (green > 0.32) & (blue > 0.32) & (green > red * 0.82) & (blue > red * 0.68) & (chroma > 0.10)
    return float(np.mean(mask))


def _component_stats(arr: np.ndarray) -> tuple[int, float]:
    """Return rough salient component count and largest component fraction."""
    height, width = arr.shape[:2]
    stride = max(1, int(math.ceil(max(height, width) / 128)))
    if stride > 1:
        arr = arr[::stride, ::stride]
    gray = (arr[..., :3] * np.asarray([0.299, 0.587, 0.114], dtype=np.float32)).sum(axis=2)
    chroma = arr.max(axis=2) - arr.min(axis=2)
    saliency = np.abs(gray - float(np.median(gray))) + 0.75 * chroma
    threshold = float(np.quantile(saliency, 0.82))
    mask = saliency > threshold
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    sizes: list[int] = []
    for y in range(height):
        for x in range(width):
            if not mask[y, x] or visited[y, x]:
                continue
            stack = [(y, x)]
            visited[y, x] = True
            size = 0
            while stack:
                cy, cx = stack.pop()
                size += 1
                for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                    if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True
                        stack.append((ny, nx))
            if size >= 0.0025 * height * width:
                sizes.append(size)
    if not sizes:
        return 0, 0.0
    total = sum(sizes)
    return len(sizes), float(max(sizes) / total) if total else 0.0


def target_region_metrics(target_name: str, target: Image.Image, render: Image.Image) -> dict[str, float]:
    """Region-aware and heuristic metrics for difficult target-specific failures."""
    target_arr, render_arr = _rgb_arrays(target, render)
    if target_name == "1159_7.png":
        boxes = {
            "top": (0.10, 0.02, 0.90, 0.48),
            "left_side": (0.02, 0.36, 0.52, 0.98),
            "right_side": (0.45, 0.34, 0.98, 0.98),
        }
        scores = []
        for name, box in boxes.items():
            target_crop = _crop_fraction(target_arr, box)
            render_crop = _crop_fraction(render_arr, box)
            _, edge_sim = edge_similarity(target_crop, render_crop)
            color_sim = color_histogram_similarity(target_crop, render_crop, bins=24)
            score = 0.58 * edge_sim + 0.42 * color_sim
            scores.append(score)
        component_count, largest_fraction = _component_stats(render_arr)
        component_score = max(0.0, min(1.0, largest_fraction - 0.10 * max(0, component_count - 3)))
        region_score = float(np.mean(scores))
        heuristic_score = 0.75 * region_score + 0.25 * component_score
        return {
            "region_score": region_score,
            "heuristic_score": heuristic_score,
            "saliency_component_count": float(component_count),
            "largest_component_fraction": largest_fraction,
        }
    if target_name == "9338.png":
        boxes = {
            "body": (0.14, 0.12, 0.80, 0.94),
            "head_profile": (0.10, 0.06, 0.52, 0.42),
            "belly_jewel": (0.26, 0.38, 0.64, 0.72),
            "right_scales": (0.42, 0.16, 0.88, 0.64),
            "aura": (0.02, 0.02, 0.98, 0.98),
        }
        scores = []
        for name, box in boxes.items():
            target_crop = _crop_fraction(target_arr, box)
            render_crop = _crop_fraction(render_arr, box)
            _, edge_sim = edge_similarity(target_crop, render_crop)
            color_sim = color_histogram_similarity(target_crop, render_crop, bins=24)
            weight_edge = 0.48 if name in {"aura", "belly_jewel"} else 0.62
            scores.append(weight_edge * edge_sim + (1.0 - weight_edge) * color_sim)
        target_belly = _crop_fraction(target_arr, boxes["belly_jewel"])
        render_belly = _crop_fraction(render_arr, boxes["belly_jewel"])
        target_body = _crop_fraction(target_arr, boxes["body"])
        render_body = _crop_fraction(render_arr, boxes["body"])
        target_teal = _teal_fraction(target_belly)
        render_teal = _teal_fraction(render_belly)
        teal_score = max(0.0, min(1.0, 1.0 - abs(render_teal - target_teal) / 0.18))
        target_asym = _horizontal_asymmetry(target_body)
        render_asym = _horizontal_asymmetry(render_body)
        asymmetry_score = max(0.0, min(1.0, 1.0 - abs(render_asym - target_asym) / 0.12))
        component_count, largest_fraction = _component_stats(render_arr)
        single_subject_score = max(0.0, min(1.0, largest_fraction - 0.14 * max(0, component_count - 4)))
        region_score = float(np.mean(scores))
        heuristic_score = (
            0.46 * region_score +
            0.20 * single_subject_score +
            0.20 * teal_score +
            0.14 * asymmetry_score
        )
        return {
            "region_score": region_score,
            "heuristic_score": heuristic_score,
            "teal_belly_score": teal_score,
            "side_asymmetry_score": asymmetry_score,
            "saliency_component_count": float(component_count),
            "largest_component_fraction": largest_fraction,
        }
    return {
        "region_score": float(visual_specific_metrics(target, render)["visual_specific_score"]),
        "heuristic_score": 0.5,
        "saliency_component_count": 0.0,
        "largest_component_fraction": 0.0,
    }


# ---------------------------------------------------------------------------
# CLIP helpers
# ---------------------------------------------------------------------------

def load_clip(
    model_name: str,
    device: str,
    local_files_only: bool = False,
) -> tuple[Any, Any]:
    """Load a CLIP image processor and model, returning ``(processor, model)``."""
    from transformers import CLIPImageProcessor, CLIPModel

    processor = CLIPImageProcessor.from_pretrained(
        model_name, local_files_only=local_files_only,
    )
    model = CLIPModel.from_pretrained(
        model_name, local_files_only=local_files_only,
    ).to(device)
    model.eval()
    return processor, model


@torch.no_grad()
def clip_image_embedding(
    image: Image.Image,
    processor: Any,
    model: Any,
    device: str,
) -> torch.Tensor:
    """Return the L2-normalised CLIP image embedding for *image*."""
    inputs = processor(images=image, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}
    embedding = model.get_image_features(**inputs)
    return embedding / embedding.norm(dim=-1, keepdim=True)


# ---------------------------------------------------------------------------
# LPIPS loader
# ---------------------------------------------------------------------------

def load_lpips(net: str, device: str) -> Any:
    """Load and return an LPIPS model on *device*."""
    import lpips as _lpips

    model = _lpips.LPIPS(net=net).to(device)
    model.eval()
    return model


# ---------------------------------------------------------------------------
# Ranking utilities
# ---------------------------------------------------------------------------

def minmax_good(values: list[float], higher_is_better: bool) -> list[float]:
    """Min-max normalise *values* so that the 'good' end maps to 1.0."""
    if not values:
        return []
    lo = min(values)
    hi = max(values)
    if abs(hi - lo) < 1e-12:
        return [0.5 for _ in values]
    scaled = [(v - lo) / (hi - lo) for v in values]
    return scaled if higher_is_better else [1.0 - v for v in scaled]


def add_combined_scores(
    rows: list[dict[str, Any]],
    clip_weight: float = 0.50,
    lpips_weight: float = 0.35,
    rmse_weight: float = 0.15,
) -> None:
    """Add a ``combined_score`` key to each row, normalised per target."""
    by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_target[row["target_name"]].append(row)

    for group in by_target.values():
        clip_good = minmax_good([float(r["clip_iisim"]) for r in group], True)
        lpips_good = minmax_good([float(r["lpips_alex"]) for r in group], False)
        rmse_good = minmax_good([float(r["pixel_rmse_01"]) for r in group], False)
        for row, c, l, r in zip(group, clip_good, lpips_good, rmse_good):
            row["combined_score"] = clip_weight * c + lpips_weight * l + rmse_weight * r


DEFAULT_SCORE_WEIGHTS = {
    "clip": 0.28,
    "lpips": 0.32,
    "rmse": 0.12,
    "ssim": 0.08,
    "color": 0.10,
    "edge": 0.06,
    "layout": 0.04,
}
TARGET_SCORE_WEIGHTS = {
    "9338.png": {"clip": 0.20, "lpips": 0.28, "rmse": 0.12, "ssim": 0.10, "color": 0.16, "edge": 0.09, "layout": 0.05},
    "1159_3.png": {"clip": 0.34, "lpips": 0.25, "rmse": 0.16, "ssim": 0.08, "color": 0.08, "edge": 0.06, "layout": 0.03},
    "1159_7.png": {"clip": 0.12, "lpips": 0.34, "rmse": 0.15, "ssim": 0.13, "color": 0.09, "edge": 0.12, "layout": 0.05},
    "1159_25.png": {"clip": 0.25, "lpips": 0.36, "rmse": 0.12, "ssim": 0.08, "color": 0.12, "edge": 0.04, "layout": 0.03},
    "1159_29.png": {"clip": 0.34, "lpips": 0.30, "rmse": 0.10, "ssim": 0.08, "color": 0.09, "edge": 0.05, "layout": 0.04},
    "7836.png": {"clip": 0.16, "lpips": 0.16, "rmse": 0.20, "ssim": 0.26, "color": 0.10, "edge": 0.08, "layout": 0.04},
}


def score_weights_for_target(target_name: str) -> dict[str, float]:
    weights = dict(DEFAULT_SCORE_WEIGHTS)
    weights.update(TARGET_SCORE_WEIGHTS.get(target_name, {}))
    total = sum(float(value) for value in weights.values()) or 1.0
    return {key: float(value) / total for key, value in weights.items()}


def mark_pareto(group: list[dict[str, Any]]) -> None:
    """Mark rows that are not dominated across CLIP, LPIPS, RMSE and SSIM."""
    for row in group:
        row["is_pareto"] = True
        row["pareto_rank"] = 0
    for row in group:
        for other in group:
            if row is other:
                continue
            better_or_equal = (
                float(other["clip_iisim"]) >= float(row["clip_iisim"]) and
                float(other["lpips_alex"]) <= float(row["lpips_alex"]) and
                float(other["pixel_rmse_01"]) <= float(row["pixel_rmse_01"]) and
                float(other.get("pixel_ssim_01", 0.0)) >= float(row.get("pixel_ssim_01", 0.0))
            )
            strictly_better = (
                float(other["clip_iisim"]) > float(row["clip_iisim"]) or
                float(other["lpips_alex"]) < float(row["lpips_alex"]) or
                float(other["pixel_rmse_01"]) < float(row["pixel_rmse_01"]) or
                float(other.get("pixel_ssim_01", 0.0)) > float(row.get("pixel_ssim_01", 0.0))
            )
            if better_or_equal and strictly_better:
                row["is_pareto"] = False
                row["pareto_rank"] = 1
                break


def add_weighted_scores(rows: list[dict[str, Any]], pareto_bonus: float = 0.03) -> None:
    """Add target-specific combined and selection scores to each row."""
    by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_target[row["target_name"]].append(row)

    for target_name, group in by_target.items():
        clip_good = minmax_good([float(r["clip_iisim"]) for r in group], True)
        lpips_good = minmax_good([float(r["lpips_alex"]) for r in group], False)
        rmse_good = minmax_good([float(r["pixel_rmse_01"]) for r in group], False)
        ssim_good = minmax_good([float(r.get("pixel_ssim_01", 0.0)) for r in group], True)
        color_good = minmax_good([float(r.get("color_hist_sim", 0.5)) for r in group], True)
        edge_good = minmax_good([float(r.get("edge_sim", 0.5)) for r in group], True)
        layout_good = minmax_good([float(r.get("layout_sim", 0.5)) for r in group], True)
        weights = score_weights_for_target(target_name)
        active_weights = dict(weights)
        for key, field in (("color", "color_hist_sim"), ("edge", "edge_sim"), ("layout", "layout_sim")):
            if not any(field in row for row in group):
                active_weights[key] = 0.0
        active_total = sum(active_weights.values()) or 1.0
        active_weights = {key: value / active_total for key, value in active_weights.items()}
        for row, c, l, r, s, color, edge, layout in zip(
            group, clip_good, lpips_good, rmse_good, ssim_good, color_good, edge_good, layout_good,
        ):
            row["clip_norm"] = c
            row["lpips_norm"] = l
            row["rmse_norm"] = r
            row["ssim_norm"] = s
            row["color_norm"] = color
            row["edge_norm"] = edge
            row["layout_norm"] = layout
            row["combined_score"] = (
                active_weights.get("clip", 0.0) * c +
                active_weights.get("lpips", 0.0) * l +
                active_weights.get("rmse", 0.0) * r +
                active_weights.get("ssim", 0.0) * s +
                active_weights.get("color", 0.0) * color +
                active_weights.get("edge", 0.0) * edge +
                active_weights.get("layout", 0.0) * layout
            )
        mark_pareto(group)
        for row in group:
            row["selection_score"] = float(row["combined_score"]) + (pareto_bonus if row["is_pareto"] else 0.0)


def aggregate(
    rows: list[dict[str, Any]],
    metric_names: list[str],
) -> dict[str, dict[str, float]]:
    """Compute mean/std for each metric across *rows*."""
    result: dict[str, dict[str, float]] = {}
    for name in metric_names:
        vals = np.asarray([float(row[name]) for row in rows], dtype=np.float64)
        result[name] = {
            "mean": float(vals.mean()) if len(vals) else float("nan"),
            "std": float(vals.std(ddof=1)) if len(vals) > 1 else 0.0,
        }
    return result
