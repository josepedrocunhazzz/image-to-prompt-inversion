from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from tp2_prompt_gen import make_entry, sample, unique_keep_order


SOURCE = "ronda_04_final_focus"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def entries_for(target: str, prompts: list[str], limit: int, seed: int, source: str, head_size: int = 70) -> list[dict[str, str]]:
    prompts = sample(unique_keep_order(prompts), limit=limit, seed=seed, head_size=head_size)
    return [make_entry(target, prompt, index + 1, "", source) for index, prompt in enumerate(prompts)]


def build_cube_hedgehog_prompts(limit: int = 130) -> list[dict[str, str]]:
    target = "1159_7.png"
    priority = [
        "small hedgehog with compact cubical wooden block body, visible vertical 4 by 4 peach wood tile sides, tiny face recessed into the upper front edge, orange spiky fur only on the flat top plane, straight cube silhouette, warm brown studio macro photo",
        "compact cube hedgehog object, blocky peach beige wooden side walls, square tile grid visible on front and right side, small eyes and snout hidden below orange top quills, warm realistic object photo",
        "single cubical hedgehog made of carved peach wood blocks, vertical tiled cube sides, tiny face peeking from top front row, dense orange tan quills on top surface only, soft brown studio background",
        "warm peach wooden cube hedgehog, straight vertical tiled sides, small dark eyes under orange spiky top fur, dense quills forming a square cap, macro product render",
        "tiny hedgehog embedded in a compact wooden cube, front wall made of small peach square blocks, face tucked into upper front, orange quill fur on top face only, shallow depth of field",
    ]
    bodies = [
        "small hedgehog with compact cubical wooden block body",
        "compact cube hedgehog object",
        "single cubical hedgehog made of carved peach wood blocks",
        "warm peach wooden cube hedgehog",
        "tiny hedgehog embedded in a compact wooden cube",
        "strict cube shaped hedgehog with wooden block sides",
    ]
    sides = [
        "visible vertical 4 by 4 peach wood tile sides",
        "blocky peach beige wooden side walls",
        "vertical tiled cube sides",
        "straight vertical tiled sides",
        "front wall made of small peach square blocks",
        "front and side faces divided into neat wooden squares",
        "stacked vertical wood-block columns on each side",
    ]
    face = [
        "tiny face recessed into the upper front edge",
        "small eyes and snout hidden below orange top quills",
        "tiny face peeking from top front row",
        "small dark eyes under orange spiky top fur",
        "face tucked into upper front",
        "one small snout centered below the top fur",
    ]
    top = [
        "orange spiky fur only on the flat top plane",
        "dense orange tan quills on top surface only",
        "dense quills forming a square cap",
        "orange quill fur on top face only",
        "caramel orange bristles spread across the top square",
        "soft amber hedgehog fur forming the top lid",
    ]
    style = [
        "straight cube silhouette, warm brown studio macro photo",
        "warm realistic object photo",
        "soft brown studio background",
        "macro product render",
        "shallow depth of field",
        "gentle shadows and warm beige material",
    ]
    prompts = priority + [
        join_parts(body, side, face_part, top_part, style_part)
        for body, side, face_part, top_part, style_part in itertools.product(bodies, sides, face, top, style)
    ]
    return entries_for(target, prompts, limit=limit, seed=2707, source=f"{SOURCE}_cube_hedgehog", head_size=90)


def build_spiny_creature_prompts(limit: int = 110) -> list[dict[str, str]]:
    target = "9338.png"
    priority = [
        "small round fuzzy porcupine mascot, orange face and snout, glossy black eye, large teal oval belly gem, tiny claws, shaggy rainbow quills around shoulders, centered storybook fantasy painting",
        "tiny upright orange faced spiny creature, round fuzzy body, bright turquoise oval chest patch, small paws, rainbow bristles framing the back, warm multicolor painterly background",
        "compact cute quilled creature, orange muzzle and cheek, teal belly shield, little claws, short rainbow quills behind shoulders, vertical orange green light streaks, textured fantasy illustration",
        "small round echidna porcupine mascot, warm orange face, cyan oval belly patch, stubby arms, colorful soft spines around the body, centered painterly portrait",
        "tiny fuzzy orange faced creature, dark bead eye, blue green belly oval, rainbow quill mane, little claws, warm storybook painting",
    ]
    subjects = [
        "small round fuzzy porcupine mascot",
        "tiny upright orange faced spiny creature",
        "compact cute quilled creature",
        "small round echidna porcupine mascot",
        "tiny fuzzy orange faced creature",
        "small round rainbow spined animal",
    ]
    face = [
        "orange face and snout, glossy black eye",
        "warm orange face",
        "orange muzzle and cheek",
        "soft orange head with dark bead eye",
        "bright orange cheek and tiny nose",
        "round orange face with small snout",
    ]
    belly = [
        "large teal oval belly gem",
        "bright turquoise oval chest patch",
        "teal belly shield",
        "cyan oval belly patch",
        "blue green belly oval",
        "turquoise chest oval on a fuzzy body",
    ]
    limbs = [
        "tiny claws",
        "small paws",
        "little claws",
        "stubby arms",
        "tiny hands near the belly",
    ]
    spines = [
        "shaggy rainbow quills around shoulders",
        "rainbow bristles framing the back",
        "short rainbow quills behind shoulders",
        "colorful soft spines around the body",
        "rainbow quill mane",
        "orange yellow green bristles rising behind the head",
    ]
    style = [
        "centered storybook fantasy painting",
        "warm multicolor painterly background",
        "vertical orange green light streaks, textured fantasy illustration",
        "centered painterly portrait",
        "warm storybook painting",
        "textured brush strokes and soft glow",
    ]
    prompts = priority + [
        join_parts(subject, face_part, belly_part, limb_part, spine_part, style_part)
        for subject, face_part, belly_part, limb_part, spine_part, style_part in itertools.product(
            subjects, face, belly, limbs, spines, style
        )
    ]
    return entries_for(target, prompts, limit=limit, seed=2738, source=f"{SOURCE}_spiny_creature", head_size=85)


def build_round() -> dict[str, list[dict[str, str]]]:
    return {
        "1159_7.png": build_cube_hedgehog_prompts(),
        "9338.png": build_spiny_creature_prompts(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 4 final focused visual-anchor prompts.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_04_final_focus.json"))
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
