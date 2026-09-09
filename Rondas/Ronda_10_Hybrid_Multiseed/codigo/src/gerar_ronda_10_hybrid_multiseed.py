from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

from tp2_prompt_gen import make_entry, unique_keep_order


SOURCE = "ronda_10_hybrid_repair"


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


def ablate(parts: list[str], min_parts: int = 3) -> list[str]:
    prompts = [join_parts(*parts)]
    for index in range(len(parts)):
        kept = [part for i, part in enumerate(parts) if i != index]
        if len(kept) >= min_parts:
            prompts.append(join_parts(*kept))
    for i, j in itertools.combinations(range(len(parts)), 2):
        kept = [part for k, part in enumerate(parts) if k not in {i, j}]
        if len(kept) >= min_parts:
            prompts.append(join_parts(*kept))
    return prompts


def entries_for(target: str, prompts: list[str], limit: int, seed: int, source: str) -> list[dict[str, str]]:
    prompts = sample_prompts(prompts, limit=limit, seed=seed)
    return [make_entry(target, prompt, index + 1, "", source) for index, prompt in enumerate(prompts)]


def cube_hybrid_prompts(limit: int = 340) -> list[dict[str, str]]:
    target = "1159_7.png"
    best_parts = [
        "small hedgehog with compact cubical wooden block body",
        "warm peach beige 4 by 4 cube grid sides",
        "tiny face mostly hidden below orange spiky fur",
        "amber quill fur only on the top surface",
        "realistic studio object photo",
    ]
    ronda_08_parts = [
        "pale wood cube with hidden hedgehog face",
        "tiny nose barely visible below orange quills",
        "amber spiky fur on the top surface",
        "square tiled cube sides",
        "warm brown macro photo",
    ]
    ronda_09_parts = [
        "pale peach square-cell cube hedgehog",
        "front and right sides built from small square cells",
        "tiny dark nose at the top front center",
        "thin orange hairlike quills rising from the top square",
        "soft macro product photo",
    ]

    subjects = [
        "small hedgehog with compact cubical wooden block body",
        "compact cubical hedgehog object",
        "pale peach square-cell cube hedgehog",
        "solid cube hedgehog sculpture",
        "tiny hedgehog embedded in a pale block cube",
        "single cube-shaped hedgehog toy",
    ]
    sides = [
        "warm peach beige 4 by 4 cube grid sides",
        "front and right sides built from small square cells",
        "visible 4 by 4 peach blocks on the front and right face",
        "straight vertical sides divided into square cells",
        "regular square lattice sides with shallow grooves",
        "stacked pale cubical columns forming both visible sides",
    ]
    face = [
        "tiny face mostly hidden below orange spiky fur",
        "tiny nose barely visible below orange quills",
        "pinpoint dark eyes and tiny nose at the top front edge",
        "small centered face peeking from under the top tuft",
        "hidden hedgehog face pressed into the top front edge",
    ]
    top = [
        "amber quill fur only on the top surface",
        "thin orange hairlike quills rising from the top square",
        "orange tan spines concentrated only on the flat top",
        "bristly orange crown with fine pointed strands",
        "messy amber quill tuft covering the top plane",
    ]
    constraints = [
        "closed cube silhouette",
        "body hidden inside the cube",
        "sides stay blocky and visible",
        "top fur compact, side grid dominant",
    ]
    styles = [
        "realistic studio object photo",
        "warm brown macro photo",
        "soft macro product photo",
        "centered square crop with gentle shadows",
    ]

    priority = [
        join_parts(*best_parts),
        join_parts(*ronda_08_parts),
        join_parts(*ronda_09_parts),
        "small hedgehog with compact cubical wooden block body, visible 4 by 4 peach blocks on the front and right face, tiny nose barely visible below orange quills, thin orange hairlike quills rising from the top square, realistic studio object photo",
        "pale peach square-cell cube hedgehog, warm peach beige 4 by 4 cube grid sides, small centered face peeking from under the top tuft, amber quill fur only on the top surface, warm brown macro photo",
        "compact cubical hedgehog object, front and right sides built from small square cells, pinpoint dark eyes and tiny nose at the top front edge, bristly orange crown with fine pointed strands, centered square crop with gentle shadows",
    ]
    prompts = priority
    prompts.extend(ablate(best_parts))
    prompts.extend(ablate(ronda_08_parts))
    prompts.extend(ablate(ronda_09_parts))
    prompts.extend(
        join_parts(subject, side, face_part, top_part, style)
        for subject, side, face_part, top_part, style in itertools.product(subjects, sides, face, top, styles)
    )
    prompts.extend(
        join_parts(constraint, subject, side, face_part, top_part, style)
        for constraint, subject, side, face_part, top_part, style in itertools.product(
            constraints, subjects[:4], sides[:4], face[:4], top[:4], styles[:3]
        )
    )
    return entries_for(target, prompts, limit=limit, seed=3307, source=f"{SOURCE}_cube_hybrid_ablation")


def dragon_hybrid_prompts(limit: int = 360) -> list[dict[str, str]]:
    target = "9338.png"
    ronda_08_parts = [
        "colorful dragon hamster with orange face and teal belly",
        "rainbow quills behind the back",
        "tiny clawed paws",
        "vertical storybook illustration",
    ]
    older_parts = [
        "small upright orange spiny animal",
        "pointed snout and dark eye",
        "glowing teal oval belly",
        "rainbow quills rising behind the back",
        "painterly multicolor background",
    ]
    ronda_09_parts = [
        "orange teal spiky hamster creature",
        "small orange snout",
        "turquoise oval belly",
        "painted scale-like rainbow spines",
        "vertical storybook painting with orange teal glow",
    ]

    subjects = [
        "colorful dragon hamster",
        "orange teal dragon hamster",
        "small upright orange spiny animal",
        "orange teal spiky hamster creature",
        "rainbow quilled hamster dragon",
        "compact fantasy quilled hamster creature",
    ]
    face = [
        "orange face and teal belly",
        "small orange snout and one glossy dark eye",
        "pointed orange snout and dark eye",
        "warm orange animal face",
        "cute rodent face looking left",
    ]
    belly = [
        "teal blue oval belly patch",
        "glowing teal oval belly",
        "turquoise oval belly",
        "blue green chest spot",
    ]
    quills = [
        "rainbow quills behind the back",
        "short rainbow quills along the back",
        "orange yellow teal quills around the silhouette",
        "painted scale-like rainbow spines",
        "rainbow bristles framing the shoulders",
    ]
    paws = [
        "tiny clawed paws",
        "small paws near the belly",
        "little pink paws near the chest",
        "small clawed hands held close to the torso",
    ]
    pose = [
        "upright compact body",
        "side profile creature portrait",
        "round vertical animal body",
        "small standing animal shape",
    ]
    styles = [
        "vertical storybook illustration",
        "dark teal fantasy background with yellow flame arcs",
        "painterly multicolor background",
        "soft glowing brushwork",
        "orange teal glow behind the body",
    ]

    priority = [
        join_parts(*ronda_08_parts),
        join_parts(*older_parts),
        join_parts(*ronda_09_parts),
        "colorful dragon hamster with orange face and teal belly, upright compact body, rainbow quills behind the back, tiny clawed paws, dark teal fantasy background with yellow flame arcs",
        "orange teal dragon hamster, pointed orange snout and dark eye, glowing teal oval belly, painted scale-like rainbow spines, small paws near the belly, vertical storybook illustration",
        "small upright orange spiny animal, cute rodent face looking left, turquoise oval belly, orange yellow teal quills around the silhouette, little pink paws near the chest, painterly multicolor background",
    ]
    prompts = priority
    prompts.extend(ablate(ronda_08_parts, min_parts=3))
    prompts.extend(ablate(older_parts, min_parts=3))
    prompts.extend(ablate(ronda_09_parts, min_parts=3))
    prompts.extend(
        join_parts(subject, face_part, belly_part, quill, paw, style)
        for subject, face_part, belly_part, quill, paw, style in itertools.product(
            subjects, face, belly, quills, paws, styles
        )
    )
    prompts.extend(
        join_parts(subject, pose_part, face_part, belly_part, quill, paw, style)
        for subject, pose_part, face_part, belly_part, quill, paw, style in itertools.product(
            subjects[:5], pose, face[:4], belly, quills[:4], paws[:3], styles[:4]
        )
    )
    return entries_for(target, prompts, limit=limit, seed=3338, source=f"{SOURCE}_dragon_hybrid_ablation")


def build_round() -> dict[str, list[dict[str, str]]]:
    return {
        "1159_7.png": cube_hybrid_prompts(),
        "9338.png": dragon_hybrid_prompts(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 10 hybrid repair prompts.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_10_hybrid_repair.json"))
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
