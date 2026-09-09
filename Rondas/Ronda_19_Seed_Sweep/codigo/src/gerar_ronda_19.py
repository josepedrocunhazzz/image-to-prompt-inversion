from __future__ import annotations

import argparse
import json
from pathlib import Path

from tp2_prompt_gen import make_entry


SOURCE = "round42_seed_sweep"


METRIC_BEST = {
    "1159_25.png": "realistic orange juice still life, single clear glass, pale creamy orange juice, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
    "1159_29.png": "single slender palm tree rising from shallow turquoise ocean, gentle surf and reflective foreground water, low sun reflection behind the tree, shallow turquoise sea, muted colors",
    "1159_3.png": "single blond anime warrior mage in reflective silver armor, curved amber energy blade crossing the lower body, blue green mist and orange fire clouds behind, soft brushwork, centered square composition, low contrast",
    "1159_7.png": "small hedgehog with compact cubical wooden block body, warm peach beige cube grid sides, small face mostly hidden below orange spiky fur, soft amber bristles forming a low square cap on top, subtle wood block texture, realistic studio object photo",
    "7836.png": "tiny astronaut standing bottom center, thin curved ground arc under the astronaut, wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, subtle blue nebula clouds around the edges, moody realistic space illustration",
    "9338.png": "orange teal fantasy hamster with scales, single creature looking left, orange rounded snout and small ears, blue green glowing belly patch, rainbow scale quills on shoulder and back, tiny paws close to the belly, yellow orange painterly aura, storybook painterly illustration",
}


VISUAL_PICK = {
    "1159_25.png": "realistic orange juice still life, single tall clear glass, pale creamy orange juice, orange slice on the rim, scattered tiny citrus pieces on brown tabletop, warm realistic product photo",
    "1159_29.png": "solitary palm tree in choppy shallow water, white surf swirling around the tree roots, large foamy waves in the foreground, low sunset reflection behind the trunk, small dark island shape at far right, cinematic tropical seascape",
    "1159_3.png": "single stern blond anime warrior mage, light grey segmented armor, curved yellow energy blade crossing the torso, soft teal and orange elemental smoke, centered square composition",
    "7836.png": "tiny astronaut standing bottom center, thin curved ground arc under the astronaut, massive diagonal pink planet band crossing the sky, dark blue black starfield, cinematic realistic space landscape",
}


def build_round(include_visual_alternates: bool = True) -> dict[str, list[dict[str, str]]]:
    data: dict[str, list[dict[str, str]]] = {}
    for target, prompt in METRIC_BEST.items():
        entries = [make_entry(target, prompt, 1, "", f"{SOURCE}_metric_best")]
        if include_visual_alternates and target in VISUAL_PICK:
            entries.append(make_entry(target, VISUAL_PICK[target], 2, "", f"{SOURCE}_visual_pick"))
        data[target] = entries
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate round-42 seed-sweep prompt bank from current best prompts.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_round42_seed_sweep_best.json"))
    parser.add_argument("--metric-only", action="store_true")
    args = parser.parse_args()

    data = build_round(include_visual_alternates=not args.metric_only)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {sum(len(entries) for entries in data.values())} prompt entries to {args.output}")
    print({target: len(entries) for target, entries in data.items()})


if __name__ == "__main__":
    main()
