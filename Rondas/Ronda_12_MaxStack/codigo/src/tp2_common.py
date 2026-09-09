from __future__ import annotations

import csv
import json
import logging
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET_DIR = PROJECT_ROOT / "TP2-students" / "students" / "tp2-chosen"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "TP2-students" / "students" / "outputs"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging(
    name: str = "tp2",
    level: int = logging.INFO,
    fmt: str = "%(asctime)s [%(levelname)s] %(message)s",
    datefmt: str = "%H:%M:%S",
) -> logging.Logger:
    """Return a configured logger. Safe to call multiple times."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


log = setup_logging()


# ---------------------------------------------------------------------------
# Configuration dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LCMConfig:
    model_id: str = "SimianLuo/LCM_Dreamshaper_v7"
    seed: int = 2026
    num_inference_steps: int = 8
    guidance_scale: float = 8.0
    lcm_origin_steps: int = 50
    width: int = 768
    height: int = 768


@dataclass(frozen=True)
class EvalConfig:
    """Centralised evaluation / ranking settings."""
    clip_model: str = "openai/clip-vit-large-patch14"
    lpips_net: str = "alex"
    clip_weight: float = 0.50
    lpips_weight: float = 0.35
    rmse_weight: float = 0.15
    top_k: int = 3


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------

def list_target_images(path: Path | str = DEFAULT_TARGET_DIR) -> list[Path]:
    path = Path(path)
    if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
        return [path]
    if not path.exists():
        return []
    return sorted(p for p in path.rglob("*") if p.suffix.lower() in IMAGE_EXTENSIONS)


def seed_from_filename(path: Path | str, fallback: int = 2026) -> int:
    match = re.match(r"^(\d+)", Path(path).stem)
    return int(match.group(1)) if match else fallback


def safe_stem(path: Path | str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in Path(path).stem)


def load_image(path: Path | str) -> Image.Image:
    return Image.open(path).convert("RGB")


def create_run_dir(base_dir: Path | str = DEFAULT_OUTPUT_DIR, identity: str = "run") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = Path(base_dir) / f"{timestamp}_{identity}"
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


# ---------------------------------------------------------------------------
# JSON / CSV I/O
# ---------------------------------------------------------------------------

def read_json(path: Path | str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path | str, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path | str, rows: Iterable[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(dict.fromkeys(k for row in rows for k in row))

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path | str) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


# ---------------------------------------------------------------------------
# Device helpers
# ---------------------------------------------------------------------------

def default_device(preferred: str = "auto") -> str:
    import torch

    if preferred != "auto":
        return preferred
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


# ---------------------------------------------------------------------------
# LCM pipeline
# ---------------------------------------------------------------------------

def load_lcm_pipeline(config: LCMConfig, device: str = "auto"):
    import torch
    from diffusers import DiffusionPipeline

    resolved_device = default_device(device)
    dtype = torch.float16 if resolved_device in {"cuda", "mps"} else torch.float32
    load_kwargs = {
        "torch_dtype": dtype,
        "use_safetensors": True,
        "low_cpu_mem_usage": True,
        "disable_mmap": True,
    }
    try:
        pipe = DiffusionPipeline.from_pretrained(config.model_id, **load_kwargs)
    except TypeError:
        load_kwargs.pop("disable_mmap", None)
        pipe = DiffusionPipeline.from_pretrained(config.model_id, **load_kwargs)
    if hasattr(pipe, "safety_checker"):
        pipe.safety_checker = None
    pipe.to(resolved_device)
    return pipe, resolved_device


def render_prompt(prompt: str, seed: int, pipe, config: LCMConfig, device: str, negative_prompt: str = ""):
    import torch

    generator_device = "cpu" if device == "mps" else device
    generator = torch.Generator(device=generator_device).manual_seed(seed)
    # LatentConsistencyModelPipeline ignores negative prompts internally. Keep
    # the argument for backwards-compatible manifests, but do not spend search
    # budget treating it as a controllable variable.
    return pipe(
        prompt=prompt,
        num_inference_steps=config.num_inference_steps,
        guidance_scale=config.guidance_scale,
        original_inference_steps=config.lcm_origin_steps,
        width=config.width,
        height=config.height,
        output_type="pil",
        generator=generator,
    ).images[0]


# ---------------------------------------------------------------------------
# Prompt normalisation
# ---------------------------------------------------------------------------

def normalise_prompt_entries(raw_prompts: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for image_name, entries in raw_prompts.items():
        normalised_entries: list[dict[str, str]] = []
        for index, entry in enumerate(entries, start=1):
            if isinstance(entry, str):
                normalised_entries.append(
                    {
                        "id": f"{Path(image_name).stem}_{index:03d}",
                        "prompt": entry,
                        "negative_prompt": "",
                        "source": "manual",
                    }
                )
            elif isinstance(entry, dict):
                prompt = str(entry["prompt"])
                normalised_entries.append(
                    {
                        "id": str(entry.get("id") or f"{Path(image_name).stem}_{index:03d}"),
                        "prompt": prompt,
                        "negative_prompt": str(entry.get("negative_prompt") or ""),
                        "source": str(entry.get("source") or "manual"),
                    }
                )
            else:
                raise TypeError(f"Unsupported prompt entry for {image_name}: {entry!r}")
        result[image_name] = normalised_entries
    return result
