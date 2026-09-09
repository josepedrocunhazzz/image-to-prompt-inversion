from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

from tp2_prompt_gen import make_entry, unique_keep_order


SOURCE = "ronda_11_token_compression"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def sample_prompts(prompts: list[str], limit: int, seed: int, head_size: int = 80) -> list[str]:
    prompts = unique_keep_order(prompts)
    if len(prompts) <= limit:
        return prompts
    rng = random.Random(seed)
    head = prompts[: min(head_size, limit)]
    tail = prompts[min(head_size, len(prompts)):]
    rng.shuffle(tail)
    return head + tail[: limit - len(head)]


def entries_for(target: str, prompts: list[str], limit: int, seed: int, source: str) -> list[dict[str, str]]:
    prompts = sample_prompts(prompts, limit=limit, seed=seed)
    return [make_entry(target, prompt, index + 1, "", source) for index, prompt in enumerate(prompts)]


def cube_token_prompts(limit: int = 260) -> list[dict[str, str]]:
    target = "1159_7.png"

    anchors = [
        "cube hedgehog, peach 4x4 grid sides, tiny hidden face, orange top quills, brown studio",
        "cubical hedgehog, 4x4 block sides, tiny face, orange quills, warm macro",
        "block hedgehog, peach cube grid, hidden nose, amber top spines, studio photo",
        "wood cube hedgehog, square cell sides, buried face, orange quill crown",
        "hedgehog cube sculpture, visible block sides, tiny top face, orange bristles",
        "peach grid cube, hidden hedgehog face, orange top quills, brown background",
        "cubical animal, 4x4 peach blocks, tiny nose, spiky orange top",
        "cube with hedgehog face, peach block grid, amber quills on top",
    ]

    subjects = [
        "cube hedgehog",
        "cubical hedgehog",
        "block hedgehog",
        "wood cube hedgehog",
        "hedgehog cube sculpture",
        "peach grid cube hedgehog",
    ]
    sides = [
        "peach 4x4 grid sides",
        "4x4 block sides",
        "square cell sides",
        "peach cube grid",
        "visible block sides",
        "vertical tile sides",
    ]
    face = [
        "tiny hidden face",
        "tiny top face",
        "small dark nose",
        "buried face",
        "hidden nose",
        "small peeking face",
    ]
    top = [
        "orange top quills",
        "amber top spines",
        "spiky orange top",
        "orange quill crown",
        "amber bristle crown",
        "thin orange quills",
    ]
    style = [
        "brown studio",
        "warm macro",
        "studio photo",
        "soft shadow",
    ]

    prompts = list(anchors)
    # Extremely short semantic cores.
    prompts.extend(
        join_parts(subject, side, face_part, top_part)
        for subject, side, face_part, top_part in itertools.product(subjects, sides, face, top)
    )
    # Add style only after the core geometry.
    prompts.extend(
        join_parts(subject, side, face_part, top_part, style_part)
        for subject, side, face_part, top_part, style_part in itertools.product(
            subjects[:5], sides[:5], face[:5], top[:5], style
        )
    )
    # Ordered variants that put the grid first for candidates where geometry matters most.
    prompts.extend(
        join_parts(side, subject, face_part, top_part, style_part)
        for side, subject, face_part, top_part, style_part in itertools.product(
            sides[:4], subjects[:4], face[:4], top[:4], style[:3]
        )
    )
    return entries_for(target, prompts, limit=limit, seed=3407, source=f"{SOURCE}_cube_short_dense")


def dragon_token_prompts(limit: int = 280) -> list[dict[str, str]]:
    target = "9338.png"

    anchors = [
        "dragon hamster, orange face, teal belly, rainbow quills, tiny claws, dark fantasy glow",
        "orange teal dragon hamster, rainbow quills, tiny paws, storybook painting",
        "spiky hamster dragon, orange snout, turquoise belly, rainbow spines, dark teal glow",
        "quilled dragon hamster, orange face, blue green belly, tiny claws, flame arcs",
        "fantasy hamster dragon, orange muzzle, teal chest, rainbow bristles, vertical painting",
        "orange spiky hamster, teal belly gem, rainbow quills, painterly aura",
        "small dragon hamster, orange head, teal oval belly, rainbow back quills",
        "upright dragon hamster, orange face, turquoise belly, tiny paws, yellow flame arcs",
    ]

    subjects = [
        "dragon hamster",
        "orange teal dragon hamster",
        "spiky hamster dragon",
        "quilled dragon hamster",
        "fantasy hamster dragon",
        "orange spiky hamster",
        "upright dragon hamster",
    ]
    face = [
        "orange face",
        "orange snout",
        "orange muzzle",
        "pointed orange snout",
        "warm orange head",
    ]
    belly = [
        "teal belly",
        "turquoise belly",
        "blue green belly",
        "teal oval belly",
        "teal belly gem",
    ]
    quills = [
        "rainbow quills",
        "rainbow spines",
        "rainbow bristles",
        "orange teal quills",
        "painted scale spines",
    ]
    paws = [
        "tiny claws",
        "tiny paws",
        "small paws",
        "clawed paws",
    ]
    style = [
        "dark fantasy glow",
        "storybook painting",
        "flame arcs",
        "dark teal glow",
        "painterly aura",
    ]
    pose = [
        "upright body",
        "side profile",
        "round body",
        "compact body",
    ]

    prompts = list(anchors)
    prompts.extend(
        join_parts(subject, face_part, belly_part, quill, paw)
        for subject, face_part, belly_part, quill, paw in itertools.product(subjects, face, belly, quills, paws)
    )
    prompts.extend(
        join_parts(subject, face_part, belly_part, quill, paw, style_part)
        for subject, face_part, belly_part, quill, paw, style_part in itertools.product(
            subjects[:6], face[:4], belly[:4], quills[:4], paws[:3], style
        )
    )
    prompts.extend(
        join_parts(subject, pose_part, face_part, belly_part, quill, style_part)
        for subject, pose_part, face_part, belly_part, quill, style_part in itertools.product(
            subjects[:5], pose, face[:4], belly[:4], quills[:4], style[:4]
        )
    )
    return entries_for(target, prompts, limit=limit, seed=3438, source=f"{SOURCE}_dragon_short_dense")


def build_round() -> dict[str, list[dict[str, str]]]:
    return {
        "1159_7.png": cube_token_prompts(),
        "9338.png": dragon_token_prompts(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 11 token-compressed prompt bank.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_11_token_compression.json"))
    args = parser.parse_args()

    data = build_round()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Wrote:", args.output)
    print("Total prompts:", sum(len(entries) for entries in data.values()))
    for target, entries in data.items():
        print(target, len(entries))


if __name__ == "__main__":
    main()
