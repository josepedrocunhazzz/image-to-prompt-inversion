from __future__ import annotations

import argparse
import json
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import torch

from tp2_common import DEFAULT_TARGET_DIR, load_image
from tp2_prompt_gen import make_entry, unique_keep_order


CLIP_MODEL_ID = "openai/clip-vit-large-patch14"
SOURCE = "ronda_01_clip_guided_hard_prompt"


@dataclass(frozen=True)
class PromptSpec:
    target: str
    anchors: list[str]
    stages: list[list[str]]
    limit: int
    beam_size: int
    seed: int


def join_parts(*parts: str) -> str:
    return ", ".join(part for part in parts if part)


def append_part(prompt: str, part: str) -> str:
    if not prompt:
        return part
    if not part:
        return prompt
    return f"{prompt}, {part}"


def batched(items: list[str], batch_size: int) -> Iterable[list[str]]:
    for index in range(0, len(items), batch_size):
        yield items[index:index + batch_size]


def score_text_prompts(
    prompts: list[str],
    target_image,
    processor,
    model,
    device: str,
    batch_size: int,
) -> list[float]:
    image_inputs = processor(images=target_image, return_tensors="pt")
    image_inputs = {key: value.to(device) for key, value in image_inputs.items()}
    with torch.no_grad():
        image_embedding = model.get_image_features(**image_inputs)
        image_embedding = image_embedding / image_embedding.norm(dim=-1, keepdim=True)

    scores: list[float] = []
    for batch in batched(prompts, batch_size):
        text_inputs = processor(
            text=batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=77,
        )
        text_inputs = {key: value.to(device) for key, value in text_inputs.items()}
        with torch.no_grad():
            text_embedding = model.get_text_features(**text_inputs)
            text_embedding = text_embedding / text_embedding.norm(dim=-1, keepdim=True)
            batch_scores = (text_embedding @ image_embedding.T).squeeze(1)
        scores.extend(float(value) for value in batch_scores.detach().cpu())
    return scores


def rank_prompts(
    prompts: list[str],
    target_image,
    processor,
    model,
    device: str,
    batch_size: int,
) -> list[tuple[str, float]]:
    prompts = unique_keep_order([prompt.strip() for prompt in prompts if prompt.strip()])
    if not prompts:
        return []
    scores = score_text_prompts(prompts, target_image, processor, model, device, batch_size)
    return sorted(zip(prompts, scores), key=lambda item: item[1], reverse=True)


def beam_search_prompts(
    spec: PromptSpec,
    target_image,
    processor,
    model,
    device: str,
    batch_size: int,
) -> list[tuple[str, float]]:
    rng = random.Random(spec.seed)
    beam = unique_keep_order(spec.anchors)
    scored_archive: list[tuple[str, float]] = rank_prompts(
        beam, target_image, processor, model, device, batch_size,
    )

    for stage in spec.stages:
        shuffled_stage = list(stage)
        rng.shuffle(shuffled_stage)
        expanded = [append_part(prompt, part) for prompt in beam for part in shuffled_stage]
        ranked = rank_prompts(expanded, target_image, processor, model, device, batch_size)
        scored_archive.extend(ranked[: max(spec.beam_size, spec.limit)])
        beam = [prompt for prompt, _ in ranked[: spec.beam_size]]

    final_pool = [prompt for prompt, _ in scored_archive] + beam
    ranked_final = rank_prompts(final_pool, target_image, processor, model, device, batch_size)
    return ranked_final[: spec.limit]


def build_prompt_specs() -> dict[str, PromptSpec]:
    return {
        "1159_25.png": PromptSpec(
            target="1159_25.png",
            limit=45,
            beam_size=90,
            seed=2425,
            anchors=[
                "single clear glass of pale creamy orange juice",
                "clear cylindrical orange juice glass",
                "pale orange smoothie in a straight glass",
                "photorealistic orange juice still life",
            ],
            stages=[
                [
                    "orange slice on rim",
                    "thin orange wheel attached to glass rim",
                    "small orange garnish on the rim",
                    "orange slice and tiny citrus pieces",
                ],
                [
                    "scattered pale citrus cubes on brown tabletop",
                    "orange halves around the glass",
                    "smooth warm brown background",
                    "minimal brown studio surface",
                ],
                [
                    "commercial food photography",
                    "warm realistic product photo",
                    "soft depth of field",
                    "square crop, gentle shadows",
                ],
            ],
        ),
        "1159_29.png": PromptSpec(
            target="1159_29.png",
            limit=45,
            beam_size=90,
            seed=2429,
            anchors=[
                "single slender palm tree in calm turquoise water",
                "delicate palm tree isolated in shallow ocean",
                "one tropical palm rising from blue green sea",
                "realistic square seascape with lone palm",
            ],
            stages=[
                [
                    "small waves around the trunk",
                    "shallow surf surrounding the roots",
                    "calm ripples at the trunk base",
                    "water fills foreground around the palm",
                ],
                [
                    "low sun reflection behind the tree",
                    "misty horizontal cloud layers",
                    "distant rocky island silhouette",
                    "soft pale sunset haze",
                ],
                [
                    "photorealistic tropical seascape",
                    "muted colors, natural ocean photograph",
                    "square crop, gentle atmospheric light",
                    "realistic coastal landscape",
                ],
            ],
        ),
        "1159_3.png": PromptSpec(
            target="1159_3.png",
            limit=60,
            beam_size=110,
            seed=2403,
            anchors=[
                "one blond anime warrior mage in reflective silver armor",
                "centered blond spellblade with silver breastplate",
                "front facing blond knight mage in polished armor",
                "single blond armored battle mage portrait",
            ],
            stages=[
                [
                    "glowing golden blade crossing the lower frame",
                    "diagonal yellow energy blade across the waist",
                    "curved amber blade arc in foreground",
                    "warm blade glow at the bottom edge",
                ],
                [
                    "teal smoke on the left and orange fire cloud on the right",
                    "blue green mist behind one shoulder, orange flame behind the other",
                    "dark grey smoke with teal edge and warm orange flame",
                    "turquoise smoke aura and restrained orange backlight",
                ],
                [
                    "moody anime key art",
                    "desaturated fantasy portrait",
                    "painterly digital character concept art",
                    "square crop, soft brushwork",
                ],
            ],
        ),
        "1159_7.png": PromptSpec(
            target="1159_7.png",
            limit=90,
            beam_size=150,
            seed=2407,
            anchors=[
                "cube-shaped hedgehog made of pale wooden tiles",
                "hedgehog face embedded in a pale wooden cube",
                "small hedgehog with cubical wooden block body",
                "soft cube hedgehog object with tiled wood sides",
                "tiny face peeking from a square wooden cube",
            ],
            stages=[
                [
                    "tiny face peeking from the top front",
                    "eyes and snout nestled into the upper front edge",
                    "face mostly hidden below the spiky top",
                    "small dark eyes barely visible",
                    "rounded furry face tucked into the cube",
                ],
                [
                    "dense soft orange bristles on top",
                    "short tan quills blending into the top surface",
                    "soft spiky fur covering the top plane",
                    "orange quill blanket rising upward",
                    "shaggy amber spines, not sharp geometric spikes",
                ],
                [
                    "pale wooden tiled sides with visible square seams",
                    "4 by 4 cube grid, straight block edges",
                    "block sides divided into small square tiles",
                    "warm beige wooden cube body",
                    "macro object render, soft brown background",
                ],
                [
                    "warm studio product photo",
                    "realistic object render, gentle shadows",
                    "soft focus brown studio surface",
                    "square crop, shallow depth of field",
                ],
            ],
        ),
        "7836.png": PromptSpec(
            target="7836.png",
            limit=70,
            beam_size=130,
            seed=2436,
            anchors=[
                "small astronaut bottom center on curved moon ridge",
                "tiny astronaut standing on low lunar arc",
                "single astronaut silhouette on curved grey moon ground",
                "small space explorer at bottom edge",
            ],
            stages=[
                [
                    "diagonal pink white nebula dust lane sweeping across the sky",
                    "broad slanted rose and teal nebula cloud",
                    "wide diagonal luminous galaxy dust lane overhead",
                    "sloping pink white cosmic dust stripe in empty sky",
                ],
                [
                    "empty dark blue starfield",
                    "black blue space with sparse stars",
                    "deep blue sky with warm orange nebula core",
                    "moody blue black cosmic background",
                ],
                [
                    "curved moon ridge at the bottom",
                    "low grey lunar arc below",
                    "dark curved lunar foreground",
                    "small rim-lit grey ground below the figure",
                ],
                [
                    "cinematic science fiction matte painting",
                    "realistic sci fi landscape, square crop",
                    "dark high contrast digital painting",
                    "cinematic space concept art, dramatic scale",
                ],
            ],
        ),
        "9338.png": PromptSpec(
            target="9338.png",
            limit=90,
            beam_size=150,
            seed=2438,
            anchors=[
                "tiny upright quilled fantasy creature with orange face",
                "small rainbow spined magical creature with teal chest",
                "compact orange faced porcupine dragon critter",
                "tiny upright echidna dragon creature",
                "small colorful quilled creature, round orange face",
            ],
            stages=[
                [
                    "alert dark eye and warm orange muzzle",
                    "round orange face with glossy black eye",
                    "orange reptile face, small snout",
                    "bright bead eye and orange cheek",
                ],
                [
                    "turquoise scale chest under the face",
                    "blue green oval belly gem",
                    "cyan chest patch and tiny claws",
                    "teal armored belly scales",
                ],
                [
                    "shaggy rainbow quills rising from shoulders",
                    "multicolor spines along the back",
                    "rainbow bristles framing the compact body",
                    "tall colored back quills",
                ],
                [
                    "vertical yellow green orange light streaks",
                    "painterly aura matching target colors",
                    "warm multicolor flame aura",
                    "storybook fantasy creature painting",
                    "textured brush strokes, detailed fur and scales",
                ],
            ],
        ),
    }


def generate_clip_guided_round(
    target_dir: Path,
    output: Path,
    offline: bool,
    device: str,
    batch_size: int,
) -> dict[str, list[dict[str, object]]]:
    if offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"

    from transformers import CLIPModel, CLIPProcessor

    resolved_device = "cuda" if device == "auto" and torch.cuda.is_available() else ("cpu" if device == "auto" else device)
    processor = CLIPProcessor.from_pretrained(CLIP_MODEL_ID, local_files_only=offline)
    model = CLIPModel.from_pretrained(CLIP_MODEL_ID, local_files_only=offline).to(resolved_device).eval()

    result: dict[str, list[dict[str, object]]] = {}
    for target_name, spec in build_prompt_specs().items():
        target_path = target_dir / target_name
        if not target_path.exists():
            raise FileNotFoundError(target_path)
        target_image = load_image(target_path)
        ranked = beam_search_prompts(
            spec,
            target_image=target_image,
            processor=processor,
            model=model,
            device=resolved_device,
            batch_size=batch_size,
        )
        entries = []
        for index, (prompt, score) in enumerate(ranked, start=1):
            entry = make_entry(target_name, prompt, index, "", SOURCE)
            entry["clip_text_image_score"] = score
            entries.append(entry)
        result[target_name] = entries
        print(target_name, len(entries), "best", f"{ranked[0][1]:.4f}", ranked[0][0])

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 1 CLIP-guided hard prompt candidates.")
    parser.add_argument("--target-dir", type=Path, default=DEFAULT_TARGET_DIR)
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_01_clip_guided_hard_prompt.json"))
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu", "mps"])
    parser.add_argument("--batch-size", type=int, default=64)
    args = parser.parse_args()

    data = generate_clip_guided_round(
        target_dir=args.target_dir,
        output=args.output,
        offline=args.offline,
        device=args.device,
        batch_size=args.batch_size,
    )
    print("Wrote:", args.output)
    print("Total prompts:", sum(len(entries) for entries in data.values()))


if __name__ == "__main__":
    main()
