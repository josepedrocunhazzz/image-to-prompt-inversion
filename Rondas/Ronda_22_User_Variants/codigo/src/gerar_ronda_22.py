from __future__ import annotations

import argparse
import json
from pathlib import Path


SOURCE = "round45_user_variants"


PROMPTS: dict[str, list[tuple[str, str]]] = {
    "1159_25.png": [
        (
            "user_translucent",
            "realistic orange juice still life, single clear glass, translucent orange juice, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "translucent_pale",
            "realistic orange juice still life, single clear glass, pale translucent orange juice, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "translucent_less_milky",
            "realistic orange juice still life, single clear glass, translucent orange juice without milky creaminess, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "warm_translucent_centered",
            "realistic orange juice still life, single clear glass centered, translucent orange juice, orange slice on the rim, few citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "control_less_milky",
            "realistic orange juice still life, single clear glass, pale orange juice without milky creaminess, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
    ],
    "1159_29.png": [
        (
            "user_sunset_ripples",
            "single slender palm tree rising from shallow turquoise ocean, gentle surf, softly rippled foreground water, warm sunset glow behind the tree, lightly shadowed sunset clouds, shallow turquoise sea, subtle water reflections, calm tropical atmosphere, muted colors",
        ),
        (
            "sunset_ripples_no_beach",
            "single slender palm tree rising from shallow turquoise ocean, gentle surf, softly rippled foreground water, warm sunset glow behind the tree, lightly shadowed sunset clouds, no beach, subtle water reflections, muted colors",
        ),
        (
            "small_surf_shadow_clouds",
            "single slender palm tree rising from shallow turquoise ocean, small gentle surf around the trunk, softly rippled foreground water, warm sunset glow behind the tree, lightly shadowed clouds, subtle water reflections, muted colors",
        ),
        (
            "calm_tropical_original",
            "single slender palm tree rising from shallow turquoise ocean, gentle surf and reflective foreground water, warm sunset glow behind the tree, lightly shadowed sunset clouds, shallow turquoise sea, calm tropical atmosphere, muted colors",
        ),
        (
            "control",
            "single slender palm tree rising from shallow turquoise ocean, gentle surf and reflective foreground water, low sun reflection behind the tree, shallow turquoise sea, muted colors",
        ),
    ],
    "1159_3.png": [
        (
            "user_no_weapon_chest_fire",
            "single blond anime warrior mage in pale silver armor, glowing golden chest fissure, golden fire emerging from the center of the chest, no weapon, blue green mist and pale orange fire clouds behind, desaturated colors, matte surfaces, soft brushwork, centered square composition, low contrast",
        ),
        (
            "chest_fire_desaturated",
            "single blond anime warrior mage in pale silver armor, glowing golden chest fissure, golden fire emerging from the chest center, no weapon, blue green mist and pale orange fire clouds behind, desaturated colors, soft brushwork, centered square composition, low contrast",
        ),
        (
            "chest_fissure_no_weapon",
            "single blond anime warrior mage in matte pale silver armor, glowing golden chest fissure, soft golden fire from the center of the chest, no weapon, muted blue green mist and pale orange fire clouds behind, centered square composition, low contrast",
        ),
        (
            "subtle_chest_fire",
            "single blond anime warrior mage in pale silver armor, subtle golden chest fissure, small golden fire emerging from the chest center, no weapon, subdued blue green mist and pale orange fire clouds behind, desaturated soft brushwork, low contrast",
        ),
        (
            "hybrid_chest_blade_control",
            "single blond anime warrior mage in pale silver armor, glowing golden chest fissure, curved amber energy blade crossing the lower body, blue green mist and pale orange fire clouds behind, soft brushwork, centered square composition, low contrast",
        ),
        (
            "control",
            "single blond anime warrior mage in reflective silver armor, curved amber energy blade crossing the lower body, blue green mist and orange fire clouds behind, soft brushwork, centered square composition, low contrast",
        ),
    ],
    "1159_7.png": [
        (
            "user_125_voxel",
            "small hedgehog with body made from 125 individual wooden cubes arranged in a precise 5x5x5 grid, clearly separated cube blocks, visible gaps between cubes, geometric voxel structure, tiny face with only eyes and nose visible, no visible ears, dense orange spiky fur covering the head, realistic studio object photo",
        ),
        (
            "voxel_cube_soft",
            "small hedgehog with body made from individual wooden cubes in a precise 5x5x5 grid, separated cube blocks, geometric voxel structure, tiny eyes and nose only, no visible ears, dense orange spiky fur covering the head, realistic studio object photo",
        ),
        (
            "visible_cube_gaps",
            "small hedgehog with compact cubical wooden body, 5x5x5 grid of separated wooden cube blocks with visible gaps, geometric voxel structure, tiny eyes and nose only, no ears, dense orange spiky fur on the head, realistic studio object photo",
        ),
        (
            "cube_blocks_head_fur",
            "small hedgehog with cubical wooden body built from clearly separated cube blocks, precise 5x5x5 voxel grid, tiny face with eyes and nose only, no ears, dense orange spiky fur covering the head, studio object photo",
        ),
        (
            "control",
            "small hedgehog with compact cubical wooden block body, warm peach beige cube grid sides, small face mostly hidden below orange spiky fur, soft amber bristles forming a low square cap on top, subtle wood block texture, realistic studio object photo",
        ),
    ],
    "7836.png": [
        (
            "user_full_haze",
            "tiny astronaut standing bottom center, thin curved ground arc reflecting the light from a wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, faint blue nebula haze across the entire image, atmospheric space haze, moody realistic space illustration",
        ),
        (
            "full_haze_short",
            "tiny astronaut standing bottom center, thin curved ground arc reflecting pale pink light from a wide diagonal planetary stripe, slanted planetary ring from lower left to upper right, faint blue nebula haze across the entire image, moody realistic space illustration",
        ),
        (
            "atmospheric_haze_reflection",
            "tiny astronaut standing bottom center, thin curved ground arc reflecting the wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, faint blue nebula haze across the image, atmospheric space haze, moody realistic space illustration",
        ),
        (
            "reflection_plus_haze",
            "tiny astronaut standing bottom center, low curved ground arc with pale pink reflection, wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, faint blue nebula haze across the entire image, moody realistic space illustration",
        ),
        (
            "control_reflected",
            "tiny astronaut standing bottom center, thin curved ground arc reflecting pale pink light, wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, subtle blue nebula clouds across most of the sky, moody realistic space illustration",
        ),
    ],
    "9338.png": [
        (
            "user_natural_belly",
            "rainbow teal fantasy hamster, cute hamster anatomy, looking left, orange rounded snout and small ears, natural beige hamster belly, rainbow scale quills only on the shoulders and back, tiny paws close to the chest, rainbow painterly aura, storybook painterly illustration",
        ),
        (
            "natural_belly_keep_teal",
            "rainbow teal fantasy hamster with cute hamster anatomy, looking left, orange rounded snout and small ears, natural beige hamster belly, rainbow scale quills only on shoulders and back, tiny paws close to the chest, rainbow painterly aura, storybook painterly illustration",
        ),
        (
            "shoulder_back_quills",
            "rainbow teal fantasy hamster, looking left, orange rounded snout and small ears, natural beige hamster belly, rainbow scale quills only on the shoulders and back, tiny paws close to the chest, rainbow painterly aura, storybook painterly illustration",
        ),
        (
            "less_rainbow_belly",
            "orange teal fantasy hamster with cute hamster anatomy, looking left, orange rounded snout and small ears, natural beige hamster belly with slight blue green glow, rainbow scale quills on shoulders and back, tiny paws close to the chest, rainbow painterly aura, storybook painterly illustration",
        ),
        (
            "control",
            "orange teal fantasy hamster with scales, single creature looking left, orange rounded snout and small ears, blue green glowing belly patch, rainbow scale quills on shoulder and back, tiny paws close to the belly, yellow orange painterly aura, storybook painterly illustration",
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
    parser = argparse.ArgumentParser(description="Generate Round45 user-requested fixed-seed prompt variants.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_round45_user_variants.json"))
    args = parser.parse_args()
    data = build_round()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {args.output}")
    print({target: len(entries) for target, entries in data.items()})


if __name__ == "__main__":
    main()
