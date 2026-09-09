from __future__ import annotations

import argparse
import json
from pathlib import Path


SOURCE = "round43_fixed_seed_micro"


PROMPTS: dict[str, list[tuple[str, str]]] = {
    "1159_25.png": [
        (
            "control",
            "realistic orange juice still life, single clear glass, pale creamy orange juice, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "no_creamy",
            "realistic orange juice still life, single clear glass, pale orange juice, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "clear_pale",
            "realistic orange juice still life, single clear glass, clear pale orange juice, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "smooth_pale",
            "realistic orange juice still life, single clear glass, smooth pale orange juice, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "less_milky",
            "realistic orange juice still life, single clear glass, pale orange juice without milky creaminess, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
        (
            "fresh_translucent",
            "realistic orange juice still life, single clear glass, fresh translucent pale orange juice, orange slice on the rim, minimal citrus pieces on brown studio surface, warm realistic product photo",
        ),
    ],
    "1159_29.png": [
        (
            "control",
            "single slender palm tree rising from shallow turquoise ocean, gentle surf and reflective foreground water, low sun reflection behind the tree, shallow turquoise sea, muted colors",
        ),
        (
            "sunset_shadow_clouds",
            "single slender palm tree rising from shallow turquoise ocean at sunset, gentle active surf and reflective foreground water, shadowed clouds, low sun reflection behind the tree, muted colors",
        ),
        (
            "low_rolling_surf",
            "single slender palm tree rising from shallow turquoise ocean at sunset, low rolling surf and reflective foreground water, shadowed clouds, low sun reflection behind the tree, muted colors",
        ),
        (
            "soft_foamy_surf",
            "single slender palm tree rising from shallow turquoise ocean at sunset, soft foamy surf around the trunk, reflective foreground water, shadowed clouds, low sun reflection, muted colors",
        ),
        (
            "active_not_tall",
            "single slender palm tree rising from shallow turquoise ocean, moderately active surf with small waves, reflective foreground water, sunset glow, shadowed clouds, muted colors",
        ),
        (
            "sunset_moody_clouds",
            "single slender palm tree rising from shallow turquoise ocean, sunset atmosphere, moody shadowed clouds, gentle but visible surf, reflective foreground water, low sun reflection, muted colors",
        ),
        (
            "small_wave_lines",
            "single slender palm tree rising from shallow turquoise ocean at sunset, small wave lines and light surf in the foreground, reflective water, shadowed clouds, muted colors",
        ),
    ],
    "1159_3.png": [
        (
            "control",
            "single blond anime warrior mage in reflective silver armor, curved amber energy blade crossing the lower body, blue green mist and orange fire clouds behind, soft brushwork, centered square composition, low contrast",
        ),
        (
            "pale_silver_chest",
            "single blond anime warrior mage in pale silver armor, curved amber energy blade emerging from the center of the chest, pale blue green mist and muted orange fire clouds behind, soft brushwork, centered square composition, low contrast",
        ),
        (
            "silver_chest_subdued",
            "single blond anime warrior mage in silver armor, amber energy blade coming out of the center of the chest, subdued blue green mist and pale orange fire clouds behind, soft brushwork, centered square composition, low contrast",
        ),
        (
            "non_reflective_colors",
            "single blond anime warrior mage in pale silver armor, curved amber energy blade emerging from the chest center, blue green mist and muted orange fire clouds behind, soft brushwork, centered square composition, low contrast, non reflective colors",
        ),
        (
            "washed_elemental",
            "single blond anime warrior mage in pale silver armor, soft amber energy blade starting at the center of the chest, washed blue green mist and pale orange fire clouds behind, centered square composition, low contrast",
        ),
        (
            "matte_armor",
            "single blond anime warrior mage in matte pale silver armor, curved amber energy blade emerging from the center of the chest, muted teal mist and pale orange fire clouds behind, soft brushwork, centered square composition",
        ),
        (
            "chest_glow_muted",
            "single blond anime warrior mage in pale silver armor, amber curved energy blade glowing from the center of the chest, muted blue green mist and soft orange fire clouds behind, low contrast, subdued colors",
        ),
    ],
    "1159_7.png": [
        (
            "control",
            "small hedgehog with compact cubical wooden block body, warm peach beige cube grid sides, small face mostly hidden below orange spiky fur, soft amber bristles forming a low square cap on top, subtle wood block texture, realistic studio object photo",
        ),
        (
            "five_by_five_no_ears",
            "small hedgehog with compact cubical wooden block body, 5 by 5 by 5 geometric cube grid, no ears visible, only tiny head nose and eyes, rest covered by orange spiky fur, soft bristles forming a low square cap on top, subtle wood block texture, realistic studio object photo",
        ),
        (
            "sliced_cubelets",
            "small hedgehog with compact cubical wooden block body sliced into 125 small cubes, no ears visible, only tiny nose and eyes, rest covered by orange spiky fur, soft bristles forming a low square cap on top, realistic studio object photo",
        ),
        (
            "face_only",
            "small hedgehog with compact cubical wooden block body, warm peach beige 5 by 5 cube grid sides, no ears, tiny face with nose and eyes only, orange spiky fur covering the rest, soft bristles forming a low square cap on top",
        ),
        (
            "geometric_grid",
            "small hedgehog object with cubical wooden block body, geometric 5 by 5 cube grid on each side, no visible ears, only tiny eyes and nose below orange spiky fur, soft bristles forming a low square cap, studio object photo",
        ),
        (
            "top_fur_grid_body",
            "small hedgehog with compact 5 by 5 by 5 wooden cube body, tiny eyes and nose only, no ears visible, orange spiky fur on top, soft bristles forming a low square cap, subtle wood block texture",
        ),
        (
            "cube_body_head_only",
            "small hedgehog with sliced cubical wooden block body, 125 geometric cubelets, only head nose and eyes visible, no ears, rest is orange spiky fur, soft bristles forming a low square cap, realistic studio object photo",
        ),
    ],
    "7836.png": [
        (
            "control",
            "tiny astronaut standing bottom center, thin curved ground arc under the astronaut, wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, subtle blue nebula clouds around the edges, moody realistic space illustration",
        ),
        (
            "nebula_across_sky_reflection",
            "tiny astronaut standing bottom center, thin curved ground arc under the astronaut reflecting light from a wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, subtle blue nebula clouds across most of the image, moody realistic space illustration",
        ),
        (
            "reflected_pink_light",
            "tiny astronaut standing bottom center, thin curved ground arc reflecting pale pink light, wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, subtle blue nebula clouds across most of the sky, moody realistic space illustration",
        ),
        (
            "blue_nebula_everywhere",
            "tiny astronaut standing bottom center, curved ground arc under the astronaut with reflected pink light, wide pale pink diagonal planetary stripe, slanted planetary ring, subtle blue nebula haze spread through most of the image, moody realistic space illustration",
        ),
        (
            "stripe_reflection_ground",
            "tiny astronaut standing bottom center, thin curved ground arc reflecting the wide pale pink diagonal planetary stripe, slanted planetary ring from lower left to upper right, blue nebula clouds spread across the image, moody realistic space illustration",
        ),
        (
            "full_sky_nebula",
            "tiny astronaut standing bottom center, thin curved illuminated ground arc, wide pale pink diagonal planetary stripe reflected below, slanted planetary ring, subtle blue nebula clouds through almost the whole sky, moody realistic space illustration",
        ),
    ],
    "9338.png": [
        (
            "control",
            "orange teal fantasy hamster with scales, single creature looking left, orange rounded snout and small ears, blue green glowing belly patch, rainbow scale quills on shoulder and back, tiny paws close to the belly, yellow orange painterly aura, storybook painterly illustration",
        ),
        (
            "rainbow_teal_plain_belly",
            "rainbow teal fantasy hamster with scale quills on shoulder and back, looking left, orange rounded snout and small ears, natural warm hamster colored belly, tiny paws close to the chest, rainbow painterly aura, storybook painterly illustration",
        ),
        (
            "teal_quills_chest_paws",
            "rainbow teal fantasy hamster with scale quills on shoulder and back, looking left, orange rounded snout and small ears, plain tan hamster belly, tiny paws close to the chest, rainbow painterly aura, storybook painterly illustration",
        ),
        (
            "no_rainbow_belly",
            "rainbow teal fantasy hamster with scale quills on shoulder and back, looking left, orange rounded snout and small ears, soft beige hamster belly without rainbow color, tiny paws close to the chest, rainbow painterly aura, storybook painterly illustration",
        ),
        (
            "belly_hamster_color",
            "rainbow teal fantasy hamster with scale quills on shoulder and back, looking left, orange rounded snout and small ears, hamster colored belly patch, tiny paws close to the chest, rainbow painterly aura, storybook painterly illustration",
        ),
        (
            "reduced_belly_glow",
            "rainbow teal fantasy hamster with scale quills on shoulder and back, looking left, orange rounded snout and small ears, muted warm hamster belly, tiny paws close to the chest, rainbow painterly aura, storybook painterly illustration",
        ),
        (
            "profile_chest_paws",
            "rainbow teal fantasy hamster with scale quills on shoulder and back, looking left in profile, orange rounded snout and small ears, natural tan belly, tiny paws close to the chest, rainbow painterly aura, storybook painterly illustration",
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
    parser = argparse.ArgumentParser(description="Generate Round43 fixed-seed micro prompt variants.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_round43_fixed_seed_micro.json"))
    args = parser.parse_args()
    data = build_round()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {args.output}")
    print({target: len(entries) for target, entries in data.items()})


if __name__ == "__main__":
    main()
