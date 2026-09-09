from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from tp2_prompt_gen import make_entry, sample, unique_keep_order


SOURCE = "ronda_03_visual_anchor"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def entries_for(
    target: str,
    prompts: list[str],
    limit: int,
    seed: int,
    source: str,
    head_size: int = 60,
) -> list[dict[str, str]]:
    prompts = sample(unique_keep_order(prompts), limit=limit, seed=seed, head_size=head_size)
    return [make_entry(target, prompt, index + 1, "", source) for index, prompt in enumerate(prompts)]


def build_orange_glass_prompts(limit: int = 55) -> list[dict[str, str]]:
    target = "1159_25.png"
    priority = [
        "single tall clear glass of pale creamy orange juice, orange slice on the rim, tiny pale citrus cubes scattered on warm brown tabletop, realistic food photography",
        "photorealistic orange juice still life, centered straight glass, small orange garnish on rim, scattered pale citrus cubes, smooth warm brown studio surface",
        "pale orange smoothie in a cylindrical clear glass, orange wheel attached to the rim, orange halves and small cubes around it, soft brown background",
        "single creamy orange drink in a transparent glass, thick pale juice, orange slice garnish, tiny yellow fruit cubes on brown table, warm product photo",
    ]
    glasses = [
        "single tall clear glass of pale creamy orange juice",
        "centered straight cylindrical glass of pale orange smoothie",
        "transparent glass filled with creamy orange juice",
        "single pale orange drink in a clear glass",
    ]
    garnishes = [
        "orange slice on the rim",
        "thin orange wheel attached to the glass rim",
        "small orange garnish on the rim",
        "bright orange slice leaning against the glass",
    ]
    tables = [
        "tiny pale citrus cubes scattered on warm brown tabletop",
        "small fruit cubes arranged around the base",
        "orange halves and tiny cubes on a smooth brown surface",
        "minimal warm brown table with scattered citrus pieces",
    ]
    styles = [
        "realistic food photography",
        "warm product photo, shallow depth of field",
        "commercial drink still life, square crop",
        "soft studio lighting and gentle shadows",
    ]
    prompts = priority + [
        join_parts(glass, garnish, table, style)
        for glass, garnish, table, style in itertools.product(glasses, garnishes, tables, styles)
    ]
    return entries_for(target, prompts, limit, seed=2625, source=f"{SOURCE}_orange_glass")


def build_palm_prompts(limit: int = 55) -> list[dict[str, str]]:
    target = "1159_29.png"
    priority = [
        "single slender palm tree rising from shallow turquoise ocean, water fills foreground around the trunk, low sun reflection behind the tree, muted realistic seascape",
        "lone tropical palm rooted in calm blue green water, small waves at the trunk base, pale sunset glow and distant island horizon, natural ocean photograph",
        "delicate palm tree isolated in shallow sea, trunk centered in water, sun low behind the leaves, soft cloudy sky, realistic coastal landscape",
    ]
    subjects = [
        "single slender palm tree rising from shallow turquoise ocean",
        "lone tropical palm rooted in calm blue green water",
        "delicate palm tree isolated in shallow sea",
        "one palm tree standing in clear ocean water",
    ]
    water = [
        "water fills foreground around the trunk",
        "small waves at the trunk base",
        "calm ripples surrounding exposed roots",
        "shallow surf and reflective water in foreground",
    ]
    sky = [
        "low sun reflection behind the tree",
        "pale sunset glow and distant island horizon",
        "soft cloudy sky with warm light near horizon",
        "misty horizontal clouds and gentle ocean haze",
    ]
    style = [
        "muted realistic seascape",
        "natural ocean photograph",
        "realistic coastal landscape, square crop",
        "soft atmospheric tropical photo",
    ]
    prompts = priority + [
        join_parts(subject, water_part, sky_part, style_part)
        for subject, water_part, sky_part, style_part in itertools.product(subjects, water, sky, style)
    ]
    return entries_for(target, prompts, limit, seed=2629, source=f"{SOURCE}_palm")


def build_spellblade_prompts(limit: int = 65) -> list[dict[str, str]]:
    target = "1159_3.png"
    priority = [
        "single blond anime warrior mage in reflective silver armor, diagonal yellow energy blade across the waist, teal smoke on the left and orange fire cloud on the right, moody anime key art",
        "front facing blond knight mage with polished silver breastplate, warm yellow blade arc across lower frame, turquoise smoke aura and orange flame backlight, painterly fantasy portrait",
        "centered blond armored spellblade, silver armor and focused face, golden blade glow at the bottom edge, blue green mist and orange fire clouds behind, desaturated anime concept art",
    ]
    subjects = [
        "single blond anime warrior mage in reflective silver armor",
        "front facing blond knight mage with polished silver breastplate",
        "centered blond armored spellblade",
        "one blond fantasy fighter in shiny silver armor",
    ]
    blade = [
        "diagonal yellow energy blade across the waist",
        "warm yellow blade arc across lower frame",
        "golden blade glow at the bottom edge",
        "curved amber energy blade crossing the lower body",
    ]
    background = [
        "teal smoke on the left and orange fire cloud on the right",
        "turquoise smoke aura and orange flame backlight",
        "blue green mist and orange fire clouds behind",
        "dark smoky background split between teal and warm orange",
    ]
    style = [
        "moody anime key art",
        "painterly fantasy portrait",
        "desaturated anime concept art",
        "soft brushwork, square crop",
    ]
    prompts = priority + [
        join_parts(subject, blade_part, background_part, style_part)
        for subject, blade_part, background_part, style_part in itertools.product(subjects, blade, background, style)
    ]
    return entries_for(target, prompts, limit, seed=2603, source=f"{SOURCE}_spellblade")


def build_cube_hedgehog_prompts(limit: int = 150) -> list[dict[str, str]]:
    target = "1159_7.png"
    priority = [
        "small hedgehog with compact cubical wooden block body, warm peach beige 4 by 4 cube grid sides, tiny face mostly hidden below orange spiky fur, dense orange tan quills covering only the top plane, straight vertical cube edges, warm brown studio macro photo",
        "compact cube hedgehog object, vertical tiled wooden cube body, small eyes and snout tucked into the top front, orange spiky fur blanket on the flat top square, warm brown background",
        "single cubical wooden block hedgehog, square peach beige tile walls, tiny face recessed into upper front tiles, amber quill fur only on the top surface, realistic studio object photo",
        "small hedgehog cube with straight vertical sides, 4 by 4 wooden tile grid, face mostly hidden under the spiky top, orange tan fur crown, shallow depth of field",
        "warm peach wooden cube hedgehog, compact square body with tiled sides, tiny dark eyes below orange spines, dense quills on top plane, macro product render",
    ]
    bodies = [
        "small hedgehog with compact cubical wooden block body",
        "compact cube hedgehog object",
        "single cubical wooden block hedgehog",
        "small hedgehog cube with straight vertical sides",
        "warm peach wooden cube hedgehog",
        "cube shaped hedgehog with solid vertical tile walls",
        "tiny hedgehog embedded in a wooden cube body",
        "strict cubic hedgehog sculpture with tiled wood sides",
    ]
    cube = [
        "warm peach beige 4 by 4 cube grid sides",
        "vertical tiled wooden cube body",
        "square peach beige tile walls",
        "4 by 4 wooden tile grid",
        "compact square body with tiled sides",
        "flush square tile walls and straight cube edges",
        "continuous cube walls made of small wooden blocks",
        "front and side faces divided into neat square tiles",
    ]
    face = [
        "tiny face mostly hidden below orange spiky fur",
        "small eyes and snout tucked into the top front",
        "tiny face recessed into upper front tiles",
        "face mostly hidden under the spiky top",
        "tiny dark eyes below orange spines",
        "small snout peeking from the upper front edge",
        "little bead eyes nestled under the fur crown",
        "one small face centered on the top front row",
    ]
    top = [
        "dense orange tan quills covering only the top plane",
        "orange spiky fur blanket on the flat top square",
        "amber quill fur only on the top surface",
        "orange tan fur crown on the top square",
        "dense quills on top plane",
        "warm caramel spikes rising from the flat top",
        "soft orange hedgehog fur spread across the top face",
        "spiky amber bristles forming a square top cap",
    ]
    style = [
        "warm brown studio macro photo",
        "realistic studio object photo",
        "shallow depth of field",
        "macro product render with warm brown background",
        "soft focus brown studio surface",
        "gentle shadows and warm beige material",
    ]
    prompts = priority + [
        join_parts(body, cube_part, face_part, top_part, style_part)
        for body, cube_part, face_part, top_part, style_part in itertools.product(bodies, cube, face, top, style)
    ]
    return entries_for(target, prompts, limit, seed=2607, source=f"{SOURCE}_cube_hedgehog", head_size=100)


def build_space_prompts(limit: int = 55) -> list[dict[str, str]]:
    target = "7836.png"
    priority = [
        "small space explorer at bottom edge, sloping pink white cosmic dust stripe in empty sky, moody blue black cosmic background, small rim-lit grey ground below the figure, dark high contrast digital painting",
        "tiny astronaut standing on a curved lunar ridge, diagonal pink white nebula dust lane across dark blue space, sparse stars, cinematic science fiction matte painting",
        "small lone astronaut on low grey moon arc, broad slanted rose and teal galaxy cloud overhead, black blue starfield, dramatic scale concept art",
    ]
    subjects = [
        "small space explorer at bottom edge",
        "tiny astronaut standing on a curved lunar ridge",
        "small lone astronaut on low grey moon arc",
        "single astronaut silhouette near the bottom",
    ]
    sky = [
        "sloping pink white cosmic dust stripe in empty sky",
        "diagonal pink white nebula dust lane across dark blue space",
        "broad slanted rose and teal galaxy cloud overhead",
        "luminous diagonal galaxy band in black blue space",
    ]
    ground = [
        "small rim-lit grey ground below the figure",
        "curved lunar foreground at the bottom",
        "low grey moon ridge under the astronaut",
        "thin blue rim light along the horizon curve",
    ]
    style = [
        "dark high contrast digital painting",
        "cinematic science fiction matte painting",
        "dramatic scale concept art",
        "realistic sci fi landscape, square crop",
    ]
    prompts = priority + [
        join_parts(subject, sky_part, ground_part, style_part)
        for subject, sky_part, ground_part, style_part in itertools.product(subjects, sky, ground, style)
    ]
    return entries_for(target, prompts, limit, seed=2678, source=f"{SOURCE}_space")


def build_spiny_creature_prompts(limit: int = 115) -> list[dict[str, str]]:
    target = "9338.png"
    priority = [
        "small round rainbow spined creature, orange face and snout, glossy black eye, bright teal oval belly patch, tiny claws, multicolor quills around shoulders, vertical rainbow light streaks, textured fantasy painting",
        "tiny upright fuzzy porcupine mascot, warm orange rounded face, turquoise chest oval, small paws, rainbow bristles framing the back, painterly dark warm background",
        "compact orange faced spiny creature, cyan belly patch, little claws, shaggy rainbow quills behind shoulders, centered storybook fantasy illustration",
        "small cute echidna porcupine creature, orange muzzle and cheek, teal belly gem, short colorful quills, round fuzzy body, warm multicolor backdrop",
    ]
    subjects = [
        "small round rainbow spined creature",
        "tiny upright fuzzy porcupine mascot",
        "compact orange faced spiny creature",
        "small cute echidna porcupine creature",
        "round fuzzy orange faced fantasy animal",
        "tiny colorful quilled mascot creature",
    ]
    face = [
        "orange face and snout, glossy black eye",
        "warm orange rounded face",
        "orange muzzle and cheek",
        "small black eyes and orange snout",
        "soft orange head with tiny nose",
        "bright orange cheek and dark bead eye",
    ]
    body = [
        "bright teal oval belly patch",
        "turquoise chest oval",
        "cyan belly patch and little claws",
        "teal belly gem and small paws",
        "blue green oval chest on a fuzzy body",
        "round body with turquoise belly shield",
    ]
    spines = [
        "multicolor quills around shoulders",
        "rainbow bristles framing the back",
        "shaggy rainbow quills behind shoulders",
        "short colorful quills",
        "rainbow spines rising from the back",
        "soft orange yellow green bristles around the body",
    ]
    style = [
        "vertical rainbow light streaks, textured fantasy painting",
        "painterly dark warm background",
        "centered storybook fantasy illustration",
        "warm multicolor backdrop",
        "soft fantasy illustration, square crop",
        "textured brush strokes and glowing color bands",
    ]
    prompts = priority + [
        join_parts(subject, face_part, body_part, spine_part, style_part)
        for subject, face_part, body_part, spine_part, style_part in itertools.product(subjects, face, body, spines, style)
    ]
    return entries_for(target, prompts, limit, seed=2638, source=f"{SOURCE}_spiny_creature", head_size=90)


def build_round() -> dict[str, list[dict[str, str]]]:
    return {
        "1159_25.png": build_orange_glass_prompts(),
        "1159_29.png": build_palm_prompts(),
        "1159_3.png": build_spellblade_prompts(),
        "1159_7.png": build_cube_hedgehog_prompts(),
        "7836.png": build_space_prompts(),
        "9338.png": build_spiny_creature_prompts(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 3 visual-anchor refinement prompts.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_03_visual_anchor.json"))
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
