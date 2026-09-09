from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from tp2_prompt_gen import make_entry, unique_keep_order


SOURCE = "ronda_09_targeted_corrections"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def expand_tier(*groups: list[str]) -> list[str]:
    return [join_parts(*parts) for parts in itertools.product(*groups)]


def entries_for(target: str, tiers: list[tuple[str, list[str]]]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    index = 1
    for tier_name, prompts in tiers:
        for prompt in unique_keep_order(prompts):
            entries.append(make_entry(target, prompt, index, "", f"{SOURCE}_{tier_name}"))
            index += 1
    return entries


def cube_hedgehog_corrections() -> list[dict[str, str]]:
    target = "1159_7.png"

    tier_1_material_reset = [
        "pale peach foam cube hedgehog",
        "soft cubical hedgehog block",
        "spiky hamster in a pale foam cube",
        "pale peach block cube with tiny hedgehog face",
        "cubical creature with orange bristles on top",
        "pale square cell cube with hidden hedgehog face",
        "stacked soft cube hedgehog sculpture",
        "4 by 4 peach cube hedgehog object",
    ]

    tier_2_grid_sides = expand_tier(
        [
            "pale peach foam cube hedgehog",
            "soft cubical hedgehog block",
            "pale square cell cube with hidden hedgehog face",
            "stacked soft cube hedgehog sculpture",
        ],
        [
            "front side made of vertical square foam cells",
            "right side made of vertical square foam cells",
            "4 by 4 block grid on the front and side",
            "soft square columns covering the cube sides",
            "peach cubical cells stacked in a clean grid",
            "small pale blocks forming a square lattice",
        ],
    )

    tier_3_top_face = expand_tier(
        [
            "pale peach cube with 4 by 4 block grid sides",
            "soft foam cube with square cell sides",
            "cubical hedgehog object with vertical square cells",
            "pale peach block cube with stacked cubical sides",
        ],
        [
            "tiny dark nose at the top front center",
            "small black eyes hidden under orange bristles",
            "tiny animal face emerging from the top front edge",
            "small hedgehog snout tucked into the top center",
        ],
        [
            "long orange bristles radiating upward",
            "amber fur spikes only on the top surface",
            "thin hairlike quills rising from the top square",
            "soft orange spiky tuft covering the top",
        ],
    )

    tier_4_precision = expand_tier(
        [
            "pale peach foam cube hedgehog",
            "soft cubical hedgehog block",
            "pale square cell cube creature",
            "peach 4 by 4 cube grid hedgehog object",
        ],
        [
            "front and right sides built from small square cells",
            "vertical block grid sides with rounded soft edges",
            "stacked pale cubical columns on both visible sides",
            "regular square lattice sides with shallow grooves",
        ],
        [
            "tiny nose and eyes barely visible under the bristles",
            "small centered face peeking from under the top tuft",
            "hidden hedgehog face pressed into the top front edge",
        ],
        [
            "orange hairlike quills fanning upward",
            "amber bristly crown with thin pointed strands",
            "warm orange spines forming a messy top tuft",
        ],
    )

    tier_5_style = expand_tier(
        [
            "pale peach foam cube hedgehog, 4 by 4 block grid sides, tiny face under orange bristles",
            "soft cubical hedgehog object, vertical square cell sides, tiny nose at top front center",
            "pale square cell cube creature, stacked cubical sides, orange hairlike quills on top",
        ],
        [
            "warm brown studio background",
            "soft macro product photo",
            "realistic toy object render",
            "shallow depth of field",
        ],
    )

    tier_6_best_hybrids = [
        "pale peach foam cube hedgehog, front and right sides built from 4 by 4 square cells, tiny dark nose at the top front center, long orange bristles radiating upward, warm brown studio background",
        "soft cubical hedgehog block, stacked pale cubical columns on both visible sides, tiny animal face emerging from the top front edge, amber fur spikes only on the top surface, soft macro product photo",
        "pale square cell cube with hidden hedgehog face, regular square lattice sides with shallow grooves, small black eyes hidden under orange bristles, thin hairlike quills rising from the top square, realistic toy object render",
        "peach 4 by 4 cube grid hedgehog object, vertical block grid sides with rounded soft edges, small centered face peeking from under the top tuft, warm orange spines forming a messy top tuft, shallow depth of field",
        "soft foam cube with square cell sides, tiny hedgehog snout tucked into the top center, orange hairlike quills fanning upward, warm brown studio background",
    ]

    return entries_for(
        target,
        [
            ("cube_material_reset", tier_1_material_reset),
            ("cube_grid_sides", tier_2_grid_sides),
            ("cube_top_face", tier_3_top_face),
            ("cube_precision", tier_4_precision),
            ("cube_style", tier_5_style),
            ("cube_best_hybrids", tier_6_best_hybrids),
        ],
    )


def dragon_hamster_corrections() -> list[dict[str, str]]:
    target = "9338.png"

    tier_1_identity_reset = [
        "colorful spiky hamster creature",
        "orange teal spiky hamster creature",
        "rainbow quilled hamster creature",
        "tiny fantasy hamster with colorful spines",
        "dragon hamster with quills",
        "round hamster dragon creature",
        "painted rainbow hamster monster",
        "small orange teal fantasy rodent",
    ]

    tier_2_body_color = expand_tier(
        [
            "colorful spiky hamster creature",
            "orange teal spiky hamster creature",
            "rainbow quilled hamster creature",
            "tiny fantasy hamster with colorful spines",
        ],
        [
            "orange muzzle and cheek",
            "warm orange face",
            "small orange snout",
            "orange rodent head",
        ],
        [
            "teal blue belly patch",
            "turquoise oval belly",
            "blue green chest spot",
            "glowing teal belly center",
        ],
    )

    tier_3_quills_not_wings = expand_tier(
        [
            "colorful spiky hamster creature with warm orange face and teal blue belly patch",
            "orange teal spiky hamster creature with small orange snout and turquoise oval belly",
            "rainbow quilled hamster creature with orange muzzle and blue green chest spot",
            "tiny fantasy hamster with orange rodent head and glowing teal belly center",
        ],
        [
            "short rainbow quills along the back",
            "colorful shoulder bristles around the body",
            "painted scale-like rainbow spines",
            "small orange blue purple spikes on the shoulders",
            "curved flame colored quills behind the body",
        ],
        [
            "tiny paws close to the belly",
            "small clawed hands held in front",
            "little pink paws near the chest",
        ],
    )

    tier_4_face_pose = expand_tier(
        [
            "round hamster dragon creature",
            "colorful spiky hamster creature",
            "painted rainbow hamster monster",
            "small orange teal fantasy rodent",
        ],
        [
            "side profile orange face",
            "one large glossy black eye",
            "small pointed ears and orange snout",
            "cute rodent face looking left",
        ],
        [
            "white cream belly with teal center",
            "turquoise scales across the chest",
            "blue green oval belly spot",
        ],
        [
            "rainbow bristles and little back spines",
            "orange yellow teal quills around the silhouette",
            "painted scale texture on the body",
        ],
    )

    tier_5_background = expand_tier(
        [
            "colorful spiky hamster creature, orange muzzle, teal blue belly patch, rainbow back quills",
            "orange teal spiky hamster creature, small orange snout, turquoise oval belly, colorful shoulder bristles",
            "tiny fantasy hamster, warm orange face, glowing teal belly center, painted rainbow spines",
        ],
        [
            "dark teal fantasy background with yellow flame arcs",
            "painterly rainbow aura behind the body",
            "vertical storybook painting with orange teal glow",
            "soft brushwork fantasy creature portrait",
        ],
    )

    tier_6_best_hybrids = [
        "colorful spiky hamster creature, warm orange face, teal blue belly patch, short rainbow quills along the back, tiny paws close to the belly, dark teal fantasy background with yellow flame arcs",
        "orange teal spiky hamster creature, small orange snout, turquoise oval belly, colorful shoulder bristles around the body, small clawed hands held in front, painterly rainbow aura behind the body",
        "rainbow quilled hamster creature, orange muzzle and cheek, blue green chest spot, painted scale-like rainbow spines, little pink paws near the chest, vertical storybook painting with orange teal glow",
        "tiny fantasy hamster with colorful spines, side profile orange face, one large glossy black eye, white cream belly with teal center, orange yellow teal quills around the silhouette, soft brushwork fantasy creature portrait",
        "round hamster dragon creature, cute rodent face looking left, turquoise scales across the chest, small orange blue purple spikes on the shoulders, dark teal orange painterly background",
    ]

    return entries_for(
        target,
        [
            ("dragon_identity_reset", tier_1_identity_reset),
            ("dragon_body_color", tier_2_body_color),
            ("dragon_quills_not_wings", tier_3_quills_not_wings),
            ("dragon_face_pose", tier_4_face_pose),
            ("dragon_background", tier_5_background),
            ("dragon_best_hybrids", tier_6_best_hybrids),
        ],
    )


def build_round() -> dict[str, list[dict[str, str]]]:
    return {
        "1159_7.png": cube_hedgehog_corrections(),
        "9338.png": dragon_hamster_corrections(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 9 targeted correction prompts.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_09_targeted_corrections.json"))
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
