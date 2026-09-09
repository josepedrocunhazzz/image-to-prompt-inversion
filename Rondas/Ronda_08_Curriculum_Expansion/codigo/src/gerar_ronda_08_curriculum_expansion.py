from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from tp2_prompt_gen import make_entry, unique_keep_order


SOURCE = "ronda_08_curriculum_expansion"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def entries_for(target: str, tiers: list[tuple[str, list[str]]]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    index = 1
    for tier_name, prompts in tiers:
        for prompt in unique_keep_order(prompts):
            entries.append(make_entry(target, prompt, index, "", f"{SOURCE}_{tier_name}"))
            index += 1
    return entries


def expand_tier(*groups: list[str]) -> list[str]:
    return [join_parts(*parts) for parts in itertools.product(*groups)]


def cube_hedgehog_curriculum() -> list[dict[str, str]]:
    target = "1159_7.png"
    tier_1_identity = [
        "wooden hedgehog cube",
        "spiky wooden cube hedgehog",
        "hedgehog cube made of wood",
        "tiny hedgehog in a wooden cube",
        "wood block hedgehog",
        "cubical hedgehog sculpture",
        "spiky fur wooden cube",
        "wooden cube with hedgehog face",
    ]
    tier_2_structure = expand_tier(
        [
            "wooden hedgehog cube",
            "spiky wooden cube hedgehog",
            "hedgehog cube made of wood",
            "wooden cube with hidden hedgehog face",
        ],
        [
            "4 by 4 square block sides",
            "peach wood grid sides",
            "pale wooden block grid",
            "square tiled wood sides",
            "front and right side made of small wood cubes",
        ],
    )
    tier_3_face_top = expand_tier(
        [
            "wooden hedgehog cube with 4 by 4 square block sides",
            "spiky wooden cube hedgehog with peach wood grid sides",
            "pale wood cube with hidden hedgehog face",
            "cubical hedgehog sculpture with tiled wood sides",
        ],
        [
            "tiny face hidden under orange top fur",
            "small dark eyes buried in the top front edge",
            "tiny nose barely visible below orange quills",
            "face mostly covered by amber spines",
        ],
        [
            "orange quills on top",
            "amber spiky fur on the top surface",
            "tan orange spines rising from the top",
            "soft quill crown on the top square",
        ],
    )
    tier_4_render = expand_tier(
        [
            "wooden hedgehog cube with 4 by 4 square block sides",
            "pale wood cube hedgehog with hidden tiny face",
            "spiky wooden cube hedgehog with peach grid sides",
            "cubical hedgehog object with tiled wooden sides",
        ],
        [
            "tiny face hidden under orange top fur",
            "small dark eyes buried in the top front edge",
            "tiny nose barely visible below amber quills",
        ],
        [
            "orange quills on top",
            "amber spiky fur on the top surface",
            "tan orange spines rising from the top square",
        ],
        [
            "warm studio photo",
            "soft brown macro photo",
            "realistic product render",
            "shallow depth of field",
        ],
    )
    tier_5_best_variants = [
        "wooden hedgehog cube, 4 by 4 square block sides, tiny face hidden under orange top fur, amber quills on top, warm studio photo",
        "spiky wooden cube hedgehog, peach wood grid sides, tiny dark eyes buried in the top front edge, orange quills on top, soft brown macro photo",
        "pale wood cube with hidden hedgehog face, square tiled wood sides, tiny nose barely visible below amber quills, tan orange spines rising from the top square, realistic product render",
        "cubical hedgehog object, front and right side made of small wood cubes, face mostly covered by amber spines, soft quill crown on the top square, warm studio photo",
        "wood block hedgehog, pale wooden block grid, hidden tiny face, orange spiky fur only on the top, shallow depth of field",
    ]
    return entries_for(
        target,
        [
            ("cube_tier1_identity", tier_1_identity),
            ("cube_tier2_structure", tier_2_structure),
            ("cube_tier3_face_top", tier_3_face_top),
            ("cube_tier4_render", tier_4_render),
            ("cube_tier5_best_variants", tier_5_best_variants),
        ],
    )


def dragon_hamster_curriculum() -> list[dict[str, str]]:
    target = "9338.png"
    tier_1_identity = [
        "colorful dragon hamster",
        "rainbow dragon hamster",
        "orange dragon hamster",
        "spiky dragon hamster",
        "fantasy dragon hamster",
        "cute dragon hamster",
        "colorful spiky hamster",
        "rainbow quilled hamster",
        "tiny dragon hamster",
        "orange teal dragon hamster",
    ]
    tier_2_color_body = expand_tier(
        [
            "colorful dragon hamster",
            "rainbow dragon hamster",
            "spiky dragon hamster",
            "orange teal dragon hamster",
            "tiny dragon hamster",
        ],
        [
            "orange face",
            "orange snout",
            "warm orange animal face",
            "small pointed orange muzzle",
        ],
        [
            "teal belly",
            "blue green oval belly",
            "turquoise chest oval",
            "glowing teal belly patch",
        ],
    )
    tier_3_quills = expand_tier(
        [
            "colorful dragon hamster with orange face and teal belly",
            "rainbow dragon hamster with orange snout and blue green oval belly",
            "spiky dragon hamster with small pointed orange muzzle and turquoise chest oval",
            "tiny dragon hamster with warm orange animal face and glowing teal belly patch",
        ],
        [
            "rainbow quills behind the back",
            "colorful bristles around the shoulders",
            "orange yellow blue spines",
            "rainbow spiky halo",
            "dragon-like colorful quills",
        ],
        [
            "tiny clawed paws",
            "small paws near the belly",
            "little claws close to the torso",
        ],
    )
    tier_4_style = expand_tier(
        [
            "colorful dragon hamster with orange face and teal belly",
            "rainbow dragon hamster with orange snout and blue green oval belly",
            "spiky dragon hamster with turquoise chest oval",
            "tiny dragon hamster with glowing teal belly patch",
        ],
        [
            "rainbow quills behind the back",
            "colorful bristles around the shoulders",
            "orange yellow blue spines",
            "dragon-like colorful quills",
        ],
        [
            "tiny clawed paws",
            "small paws near the belly",
        ],
        [
            "painterly fantasy background",
            "dark teal orange fantasy painting",
            "vertical storybook illustration",
            "soft glowing brushwork",
        ],
    )
    tier_5_best_variants = [
        "colorful dragon hamster, orange face, teal belly, rainbow quills behind the back, tiny clawed paws, painterly fantasy background",
        "rainbow dragon hamster, orange snout, blue green oval belly, colorful bristles around the shoulders, small paws near the belly, vertical storybook illustration",
        "spiky dragon hamster, small pointed orange muzzle, turquoise chest oval, orange yellow blue spines, little claws close to the torso, dark teal orange fantasy painting",
        "tiny dragon hamster, warm orange animal face, glowing teal belly patch, dragon-like colorful quills, tiny clawed paws, soft glowing brushwork",
        "orange teal dragon hamster, rainbow spiky halo, small paws near the belly, painterly multicolor background",
    ]
    return entries_for(
        target,
        [
            ("dragon_tier1_identity", tier_1_identity),
            ("dragon_tier2_color_body", tier_2_color_body),
            ("dragon_tier3_quills", tier_3_quills),
            ("dragon_tier4_style", tier_4_style),
            ("dragon_tier5_best_variants", tier_5_best_variants),
        ],
    )


def build_round() -> dict[str, list[dict[str, str]]]:
    return {
        "1159_7.png": cube_hedgehog_curriculum(),
        "9338.png": dragon_hamster_curriculum(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 8 curriculum expansion prompts.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_08_curriculum_expansion.json"))
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
