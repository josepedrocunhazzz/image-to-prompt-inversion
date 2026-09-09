from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from tp2_prompt_gen import make_entry, sample, unique_keep_order


SOURCE = "ronda_05_visual_metric_micro"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def entries_for(target: str, prompts: list[str], limit: int, seed: int, source: str, head_size: int = 40) -> list[dict[str, str]]:
    prompts = sample(unique_keep_order(prompts), limit=limit, seed=seed, head_size=head_size)
    return [make_entry(target, prompt, index + 1, "", source) for index, prompt in enumerate(prompts)]


def build_cube_hedgehog_prompts(limit: int = 72) -> list[dict[str, str]]:
    target = "1159_7.png"
    priority = [
        "pale wooden cube hedgehog sculpture, vertical 4 by 4 block grid on the front and side, tiny dark face recessed in the top center, dense tan orange spines rising from the top plane, warm brown studio render",
        "cubical hedgehog fused into a pale wood block, visible square wooden tiles on both side faces, small sleepy face hidden below the orange spiky crown, closed cube form, soft brown macro photo",
        "warm peach wooden block cube with hedgehog face embedded in the upper front, regular 4 by 4 carved tile sides, orange tan quills covering the top surface, centered object photo",
        "small hedgehog face inside a tiled wooden cube, pale square block sides, orange fur spikes forming a compact crown on top, realistic warm studio product render",
        "closed pale timber cube creature, front wall made of small square wooden blocks, tiny eyes and nose under tan orange spines, spines grow from top plane, soft realistic lighting",
    ]
    cube_forms = [
        "pale wooden cube hedgehog sculpture",
        "cubical hedgehog fused into a pale wood block",
        "warm peach wooden block cube with hedgehog face embedded in the upper front",
        "small hedgehog face inside a tiled wooden cube",
        "closed pale timber cube creature",
        "compact square wood-block hedgehog object",
    ]
    grids = [
        "vertical 4 by 4 block grid on the front and side",
        "visible square wooden tiles on both side faces",
        "regular 4 by 4 carved tile sides",
        "pale square block sides",
        "front wall made of small square wooden blocks",
        "stacked pale wood columns forming straight cube sides",
    ]
    faces = [
        "tiny dark face recessed in the top center",
        "small sleepy face hidden below the orange spiky crown",
        "tiny eyes and nose tucked into the upper front edge",
        "small central face peeking through the top fur",
        "face mostly buried in the tan fur at the top front",
    ]
    tops = [
        "dense tan orange spines rising from the top plane",
        "orange tan quills covering the top surface",
        "orange fur spikes forming a compact crown on top",
        "tan orange bristles grow from the top plane",
        "soft amber quill fur concentrated on the flat top",
    ]
    styles = [
        "warm brown studio render",
        "soft brown macro photo",
        "centered object photo",
        "realistic warm studio product render",
        "shallow depth of field and gentle shadows",
    ]
    prompts = priority + [
        join_parts(cube, grid, face, top, style)
        for cube, grid, face, top, style in itertools.product(cube_forms, grids, faces, tops, styles)
    ]
    return entries_for(target, prompts, limit=limit, seed=2807, source=f"{SOURCE}_cube_hedgehog", head_size=45)


def build_spiny_creature_prompts(limit: int = 72) -> list[dict[str, str]]:
    target = "9338.png"
    priority = [
        "upright fantasy spiny creature, orange animal face with pointed snout, large glowing teal oval belly, tiny clawed paws, rainbow quills and bristles rising behind the back, painterly dark multicolor background",
        "small vertical porcupine creature, warm orange face and snout, bright turquoise oval chest gem, thin arms with little claws, colorful spines framing the silhouette, soft fantasy illustration",
        "round quilled fantasy animal, orange face, teal oval belly shield, small claws near the belly, rainbow spines radiating from shoulders and back, vertical storybook painting",
        "tiny echidna-like creature portrait, orange muzzle and cheek, blue green oval belly jewel, clawed paws, tall rainbow quill mane around the body, moody painterly glow",
        "compact spiny animal standing upright, orange head and dark eye, luminous teal belly oval, little claws, rainbow bristle halo behind the body, textured fantasy art",
    ]
    subjects = [
        "upright fantasy spiny creature",
        "small vertical porcupine creature",
        "round quilled fantasy animal",
        "tiny echidna-like creature portrait",
        "compact spiny animal standing upright",
        "small orange-faced quilled creature",
    ]
    faces = [
        "orange animal face with pointed snout",
        "warm orange face and snout",
        "orange face",
        "orange muzzle and cheek",
        "orange head and dark eye",
        "small foxlike orange face",
    ]
    bellies = [
        "large glowing teal oval belly",
        "bright turquoise oval chest gem",
        "teal oval belly shield",
        "blue green oval belly jewel",
        "luminous teal belly oval",
        "cyan oval belly patch centered on the torso",
    ]
    paws = [
        "tiny clawed paws",
        "thin arms with little claws",
        "small claws near the belly",
        "clawed paws",
        "little hands held beside the belly",
    ]
    quills = [
        "rainbow quills and bristles rising behind the back",
        "colorful spines framing the silhouette",
        "rainbow spines radiating from shoulders and back",
        "tall rainbow quill mane around the body",
        "rainbow bristle halo behind the body",
        "orange yellow blue quills along the back",
    ]
    styles = [
        "painterly dark multicolor background",
        "soft fantasy illustration",
        "vertical storybook painting",
        "moody painterly glow",
        "textured fantasy art",
        "saturated brushwork and glowing color streaks",
    ]
    prompts = priority + [
        join_parts(subject, face, belly, paw, quill, style)
        for subject, face, belly, paw, quill, style in itertools.product(subjects, faces, bellies, paws, quills, styles)
    ]
    return entries_for(target, prompts, limit=limit, seed=2838, source=f"{SOURCE}_spiny_creature", head_size=45)


def build_round() -> dict[str, list[dict[str, str]]]:
    return {
        "1159_7.png": build_cube_hedgehog_prompts(),
        "9338.png": build_spiny_creature_prompts(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 5 micro prompts for visual-metric ranking.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_05_visual_metric_micro.json"))
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
