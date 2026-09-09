from __future__ import annotations

import argparse
import json
from pathlib import Path


SOURCE = "round44_conservative_micro"


PROMPTS: dict[str, list[tuple[str, str]]] = {
    "1159_25.png": [
        (
            "control_round43_best",
            "realistic orange juice still life, single clear glass, pale orange juice without milky creaminess, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "no_creamy_clean",
            "realistic orange juice still life, single clear glass, pale orange juice, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "less_milky_smooth",
            "realistic orange juice still life, single clear glass, smooth pale orange juice without milky creaminess, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "less_milky_target_layout",
            "realistic orange juice still life, single clear glass centered, pale orange juice without milky creaminess, orange slice on the rim, few citrus pieces on brown studio surface, warm realistic product photo",
        ),
    ],
    "1159_29.png": [
        (
            "control",
            "single slender palm tree rising from shallow turquoise ocean, gentle surf and reflective foreground water, low sun reflection behind the tree, shallow turquoise sea, muted colors",
        ),
        (
            "slightly_stronger_surf",
            "single slender palm tree rising from shallow turquoise ocean, slightly stronger small surf and reflective foreground water, low sunset reflection behind the tree, shadowed clouds, shallow turquoise sea, muted colors",
        ),
        (
            "small_active_surf_no_beach",
            "single slender palm tree rising from shallow turquoise ocean, small active surf around the trunk, reflective foreground water, low sunset glow behind the tree, shadowed clouds, no beach, muted colors",
        ),
        (
            "gentle_visible_surf",
            "single slender palm tree rising from shallow turquoise ocean, gentle but visible surf ripples, reflective foreground water, low sunset reflection behind the tree, shadowed clouds, muted colors",
        ),
        (
            "moody_clouds_same_ocean",
            "single slender palm tree rising from shallow turquoise ocean, gentle surf and reflective foreground water, low sunset reflection behind the tree, moody shadowed clouds, shallow turquoise sea, muted colors",
        ),
        (
            "light_foam_around_roots",
            "single slender palm tree rising from shallow turquoise ocean, light foam around the roots, reflective foreground water, low sunset reflection behind the tree, shadowed clouds, shallow turquoise sea, muted colors",
        ),
    ],
    "1159_3.png": [
        (
            "control",
            "single blond anime warrior mage in reflective silver armor, curved amber energy blade crossing the lower body, blue green mist and orange fire clouds behind, soft brushwork, centered square composition, low contrast",
        ),
        (
            "pale_armor_hybrid_blade",
            "single blond anime warrior mage in pale silver armor, curved amber energy blade starting near the center of the chest and crossing the lower body, pale blue green mist and muted orange fire clouds behind, soft brushwork, centered square composition, low contrast",
        ),
        (
            "silver_hybrid_subdued",
            "single blond anime warrior mage in silver armor, curved amber energy blade emerging from the chest center and sweeping across the lower body, subdued blue green mist and pale orange fire clouds behind, soft brushwork, centered square composition, low contrast",
        ),
        (
            "matte_pale_hybrid",
            "single blond anime warrior mage in matte pale silver armor, curved amber energy blade starting at the chest center and bending down across the lower body, muted teal mist and pale orange fire clouds behind, soft brushwork, centered square composition",
        ),
        (
            "non_reflective_same_pose",
            "single blond anime warrior mage in pale silver armor, curved amber energy blade crossing the lower body from a small chest glow, muted blue green mist and soft orange fire clouds behind, low contrast, subdued colors",
        ),
        (
            "washed_colors_original_blade",
            "single blond anime warrior mage in silver armor, curved amber energy blade crossing the lower body, washed blue green mist and pale orange fire clouds behind, soft brushwork, centered square composition, low contrast",
        ),
    ],
    "1159_7.png": [
        (
            "control",
            "small hedgehog with compact cubical wooden block body, warm peach beige cube grid sides, small face mostly hidden below orange spiky fur, soft amber bristles forming a low square cap on top, subtle wood block texture, realistic studio object photo",
        ),
        (
            "no_ears_soft",
            "small hedgehog with compact cubical wooden block body, warm peach beige cube grid sides, no ears visible, only tiny eyes and nose below orange spiky fur, soft bristles forming a low square cap on top, subtle wood block texture, realistic studio object photo",
        ),
        (
            "five_by_five_soft",
            "small hedgehog with compact cubical wooden block body, warm peach beige 5 by 5 cube grid sides, tiny eyes and nose only, no ears visible, orange spiky fur above, soft bristles forming a low square cap, realistic studio object photo",
        ),
        (
            "cubelets_less_literal",
            "small hedgehog with compact cubical wooden block body made of small geometric cube tiles, tiny eyes and nose only, no ears visible, orange spiky fur above, soft bristles forming a low square cap, subtle wood block texture",
        ),
        (
            "head_hidden_grid",
            "small hedgehog with compact cubical wooden block body, square peach beige grid sides, tiny head mostly hidden with only eyes and nose visible, no ears, orange spiky fur, soft bristles forming a low square cap",
        ),
    ],
    "7836.png": [
        (
            "control_round43_best",
            "tiny astronaut standing bottom center, thin curved ground arc reflecting pale pink light, wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, subtle blue nebula clouds across most of the sky, moody realistic space illustration",
        ),
        (
            "reflection_across_ground",
            "tiny astronaut standing bottom center, thin curved ground arc reflecting light from the wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, subtle blue nebula clouds across most of the sky, moody realistic space illustration",
        ),
        (
            "more_nebula_less_edge",
            "tiny astronaut standing bottom center, thin curved ground arc reflecting pale pink light, wide pale pink diagonal planetary stripe, slanted planetary ring, subtle blue nebula clouds spread through most of the image, moody realistic space illustration",
        ),
        (
            "pink_reflection_low_arc",
            "tiny astronaut standing bottom center, low thin curved ground arc with pale pink reflection, wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, subtle blue nebula clouds across the image, moody realistic space illustration",
        ),
    ],
    "9338.png": [
        (
            "control",
            "orange teal fantasy hamster with scales, single creature looking left, orange rounded snout and small ears, blue green glowing belly patch, rainbow scale quills on shoulder and back, tiny paws close to the belly, yellow orange painterly aura, storybook painterly illustration",
        ),
        (
            "chest_paws_only",
            "rainbow fantasy hamster with scales, single creature looking left, orange rounded snout and small ears, blue green glowing belly patch, rainbow scale quills on shoulder and back, tiny paws close to the chest, yellow orange painterly aura, storybook painterly illustration",
        ),
        (
            "rainbow_aura_keep_belly",
            "orange teal fantasy hamster with scales, looking left, orange rounded snout and small ears, blue green glowing belly patch, rainbow scale quills on shoulder and back, tiny paws close to the chest, rainbow painterly aura, storybook painterly illustration",
        ),
        (
            "rainbow_teal_keep_identity",
            "rainbow teal fantasy hamster with scales, looking left, orange rounded snout and small ears, blue green glowing belly patch, rainbow scale quills on shoulder and back, tiny paws close to the chest, yellow orange painterly aura, storybook painterly illustration",
        ),
        (
            "hamster_belly_subtle",
            "orange teal fantasy hamster with scales, looking left, orange rounded snout and small ears, warm hamster colored belly with slight blue green glow, rainbow scale quills on shoulder and back, tiny paws close to the chest, yellow orange painterly aura, storybook painterly illustration",
        ),
    ],
}


def build_round() -> dict[str, list[dict[str, str]]]:
    data: dict[str, list[dict[str, str]]] = {}
    for target, prompts in PROMPTS.items():
        stem = target.removesuffix(".png")
        data[target] = [
            {
                "id": f"{stem}_{SOURCE}_{label}_{index:03d}",
                "prompt": prompt,
                "negative_prompt": "",
                "source": f"{SOURCE}_{stem}_{label}",
            }
            for index, (label, prompt) in enumerate(prompts, start=1)
        ]
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Round44 conservative fixed-seed micro prompt variants.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_round44_conservative_micro.json"))
    args = parser.parse_args()
    data = build_round()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {args.output}")
    print({target: len(entries) for target, entries in data.items()})


if __name__ == "__main__":
    main()
