from __future__ import annotations

import argparse
import json
from pathlib import Path


SOURCE = "round46_palm_minimal_ladder"
TARGET = "1159_29.png"


PROMPTS: list[tuple[str, str]] = [
    (
        "control_best",
        "single slender palm tree rising from shallow turquoise ocean, gentle surf and reflective foreground water, low sun reflection behind the tree, shallow turquoise sea, muted colors",
    ),
    ("simple_water_sunset_no_beach", "single palm tree inside shallow ocean water, sunset, no beach"),
    ("simple_turquoise_sunset_no_beach", "single palm tree standing in shallow turquoise water, sunset, no beach"),
    ("simple_rising_water", "single palm tree rising from shallow ocean water, sunset, no beach"),
    ("simple_slender", "single slender palm tree in shallow ocean water, sunset, no beach"),
    ("simple_trunk_water", "single palm tree trunk emerging from shallow ocean water, sunset, no beach"),
    ("simple_only_water_base", "single palm tree standing in shallow ocean water, only water at the base, sunset"),
    ("simple_no_sand", "single palm tree in shallow turquoise ocean, sunset, no sand"),
    ("simple_no_shore", "single palm tree in shallow turquoise ocean water, sunset, no shore"),
    ("simple_no_land", "single palm tree in shallow ocean water, sunset, no land visible"),
    ("small_waves", "single palm tree in shallow ocean water, small waves, sunset, no beach"),
    ("gentle_surf", "single palm tree in shallow ocean water, gentle surf, sunset, no beach"),
    ("soft_surf", "single palm tree in shallow turquoise ocean, soft surf, sunset, no beach"),
    ("light_foam", "single palm tree in shallow ocean water, light foam around the trunk, sunset, no beach"),
    ("water_ripples", "single palm tree in shallow ocean water, soft water ripples, sunset, no beach"),
    ("reflective_water", "single palm tree in shallow ocean water, reflective water, sunset, no beach"),
    ("sun_reflection", "single palm tree in shallow ocean water, low sun reflection, sunset, no beach"),
    ("warm_glow", "single palm tree in shallow ocean water, warm sunset glow, no beach"),
    ("shadow_clouds", "single palm tree in shallow ocean water, sunset, lightly shadowed clouds, no beach"),
    ("muted_colors", "single palm tree in shallow ocean water, sunset, muted colors, no beach"),
    ("calm_tropical", "single palm tree in calm tropical ocean water, sunset, no beach"),
    ("turquoise_small_waves", "single slender palm tree in shallow turquoise ocean, small waves, sunset, no beach"),
    ("turquoise_gentle_surf", "single slender palm tree in shallow turquoise ocean, gentle surf, sunset, no beach"),
    ("turquoise_ripples", "single slender palm tree in shallow turquoise ocean, soft ripples, sunset, no beach"),
    ("turquoise_reflective", "single slender palm tree in shallow turquoise ocean, reflective foreground water, sunset, no beach"),
    ("turquoise_sun_reflection", "single slender palm tree in shallow turquoise ocean, low sun reflection, sunset, no beach"),
    ("only_water_small_waves", "single palm tree standing in shallow ocean water, only water visible at the base, small waves, sunset"),
    ("only_water_gentle_surf", "single palm tree standing in shallow ocean water, only water visible at the base, gentle surf, sunset"),
    ("only_water_reflection", "single palm tree standing in shallow ocean water, only water visible at the base, low sun reflection, sunset"),
    ("no_beach_small_surf_clouds", "single palm tree in shallow ocean water, gentle surf, shadowed sunset clouds, no beach"),
    ("no_beach_reflection_clouds", "single palm tree in shallow ocean water, low sun reflection, shadowed sunset clouds, no beach"),
    ("no_beach_ripples_clouds", "single palm tree in shallow ocean water, softly rippled foreground water, shadowed sunset clouds, no beach"),
    ("thin_tree_small_surf", "single thin palm tree rising from shallow turquoise water, small surf, sunset, no beach"),
    ("thin_tree_reflection", "single thin palm tree rising from shallow turquoise water, low sun reflection, sunset, no beach"),
    ("thin_tree_muted", "single thin palm tree rising from shallow turquoise water, sunset, muted colors, no beach"),
    ("slender_tree_base_water", "single slender palm tree, trunk base surrounded by shallow turquoise water, sunset, no beach"),
    ("slender_tree_light_foam", "single slender palm tree, trunk base surrounded by light surf foam, sunset, no beach"),
    ("slender_tree_reflective_base", "single slender palm tree, trunk base surrounded by reflective shallow water, sunset, no beach"),
    ("target_like_short", "single slender palm tree rising from shallow turquoise ocean, gentle surf, low sun reflection, muted colors"),
    ("target_like_no_beach", "single slender palm tree rising from shallow turquoise ocean, gentle surf, low sun reflection, no beach, muted colors"),
    ("target_like_clouds", "single slender palm tree rising from shallow turquoise ocean, gentle surf, low sun reflection, shadowed clouds, muted colors"),
    ("target_like_ripples", "single slender palm tree rising from shallow turquoise ocean, gentle surf, softly rippled foreground water, low sun reflection, muted colors"),
    ("target_like_sunset", "single slender palm tree rising from shallow turquoise ocean, gentle surf, warm sunset glow, low sun reflection, muted colors"),
    ("target_like_no_land", "single slender palm tree rising from shallow turquoise ocean, gentle surf, low sun reflection, no beach, no land, muted colors"),
    ("target_like_only_water", "single slender palm tree rising from shallow turquoise ocean, gentle surf, only water visible at the base, low sun reflection, muted colors"),
]


def build_round() -> dict[str, list[dict[str, str]]]:
    stem = TARGET.removesuffix(".png")
    return {
        TARGET: [
            {
                "id": f"{stem}_{SOURCE}_{label}_{index:03d}",
                "prompt": prompt,
                "negative_prompt": "",
                "source": f"{SOURCE}_{stem}_{label}",
            }
            for index, (label, prompt) in enumerate(PROMPTS, start=1)
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Round46 minimal palm prompt ladder.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_round46_palm_minimal_ladder.json"))
    args = parser.parse_args()
    data = build_round()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {args.output}")
    print({target: len(entries) for target, entries in data.items()})


if __name__ == "__main__":
    main()
