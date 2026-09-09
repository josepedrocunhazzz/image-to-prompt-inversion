from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from tp2_prompt_gen import make_entry, sample, unique_keep_order


SOURCE = "ronda_06_precision_ablation"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def ordered_variants(groups: list[list[str]], max_permuted_groups: int = 4) -> list[str]:
    prompts: list[str] = []
    for parts in itertools.product(*groups):
        prompts.append(join_parts(*parts))
        for order in itertools.permutations(parts[:max_permuted_groups]):
            prompts.append(join_parts(*order, *parts[max_permuted_groups:]))
    return prompts


def entries_for(target: str, prompts: list[str], limit: int, seed: int, source: str, head_size: int = 80) -> list[dict[str, str]]:
    prompts = sample(unique_keep_order(prompts), limit=limit, seed=seed, head_size=head_size)
    return [make_entry(target, prompt, index + 1, "", source) for index, prompt in enumerate(prompts)]


def cube_hedgehog_prompts(limit: int = 160) -> list[dict[str, str]]:
    target = "1159_7.png"
    best_ronda_03 = (
        "small hedgehog with compact cubical wooden block body, warm peach beige 4 by 4 cube grid sides, "
        "tiny face mostly hidden below orange spiky fur, amber quill fur only on the top surface, realistic studio object photo"
    )
    priority = [
        best_ronda_03,
        "compact cubical wooden hedgehog body, warm peach beige 4 by 4 cube grid sides, tiny face mostly hidden under orange spiky top fur, amber quills on the top surface, realistic studio object photo",
        "unified cube hedgehog sculpture, body hidden inside a peach wood 4 by 4 block cube, tiny eyes and nose barely visible at the top front, orange tan quills covering the top plane, warm brown macro photo",
        "solid pale wooden cube with hedgehog identity, square block grid on the sides, tiny central face submerged below a tan orange quill crown, compact cubical silhouette, realistic warm studio render",
        "small cubical hedgehog object, peach wooden grid sides, face reduced to tiny dark eyes and nose under top fur, orange spines rising only from the flat top, soft brown studio photo",
        "single compact cube animal sculpture, pale wooden block sides in a 4 by 4 grid, hidden hedgehog face in the top front edge, dense amber quill fur forming the top cap, warm product photography",
        "warm peach cube hedgehog, vertical square tile sides, tiny face almost buried in orange fur, top surface filled with upward tan quills, realistic object render",
        "hedgehog fused into a closed wooden cube, straight cubical block body, 4 by 4 carved side grid, small dark face beneath top bristles, tan orange spines on top, warm studio macro",
    ]
    subjects = [
        "small hedgehog with compact cubical wooden block body",
        "compact cubical wooden hedgehog body",
        "unified cube hedgehog sculpture",
        "solid pale wooden cube with hedgehog identity",
        "small cubical hedgehog object",
        "single compact cube animal sculpture",
        "warm peach cube hedgehog",
        "hedgehog fused into a closed wooden cube",
    ]
    side_phrases = [
        "warm peach beige 4 by 4 cube grid sides",
        "peach wood 4 by 4 block cube",
        "square block grid on the sides",
        "peach wooden grid sides",
        "pale wooden block sides in a 4 by 4 grid",
        "vertical square tile sides",
        "4 by 4 carved side grid",
        "stacked square pale wood blocks on the front and right side",
    ]
    face_phrases = [
        "tiny face mostly hidden below orange spiky fur",
        "tiny eyes and nose barely visible at the top front",
        "tiny central face submerged below a tan orange quill crown",
        "face reduced to tiny dark eyes and nose under top fur",
        "hidden hedgehog face in the top front edge",
        "tiny face almost buried in orange fur",
        "small dark face beneath top bristles",
    ]
    top_phrases = [
        "amber quill fur only on the top surface",
        "orange tan quills covering the top plane",
        "dense amber quill fur forming the top cap",
        "orange spines rising only from the flat top",
        "top surface filled with upward tan quills",
        "tan orange spines on top",
        "soft orange fur spikes forming a low crown on the top plane",
    ]
    style_phrases = [
        "realistic studio object photo",
        "warm brown macro photo",
        "realistic warm studio render",
        "soft brown studio photo",
        "warm product photography",
        "warm studio macro",
    ]
    short_ablation = [
        "wooden cube hedgehog, 4 by 4 grid sides, hidden tiny face, orange quills on top, warm studio photo",
        "cubical wooden hedgehog, peach block sides, tiny buried face, tan spiky top fur, realistic macro",
        "solid cube hedgehog sculpture, square wood grid sides, tiny eyes under orange top quills, warm render",
        "small wood-block hedgehog cube, hidden face, amber quill top, peach square sides, object photo",
    ]
    prompts = priority + short_ablation + ordered_variants(
        [subjects, side_phrases, face_phrases, top_phrases, style_phrases],
        max_permuted_groups=4,
    )
    return entries_for(target, prompts, limit=limit, seed=2907, source=f"{SOURCE}_cube_hedgehog", head_size=90)


def spiny_creature_prompts(limit: int = 120) -> list[dict[str, str]]:
    target = "9338.png"
    best_ronda_05 = (
        "upright fantasy spiny creature, orange animal face with pointed snout, large glowing teal oval belly, "
        "tiny clawed paws, rainbow bristle halo behind the body, vertical storybook painting"
    )
    priority = [
        best_ronda_05,
        "small upright orange spiny animal, pointed snout and dark eye, glowing teal oval belly, tiny clawed paws close to the torso, rainbow quills rising behind the back, painterly multicolor background",
        "compact fantasy porcupine creature, orange face and snout, large teal belly oval, small paws, rainbow quill halo around the shoulders, vertical painterly illustration",
        "short upright quilled creature, warm orange animal face, turquoise oval belly gem, little claws near the chest, rainbow bristles framing the back, soft storybook painting",
        "small orange-faced spiny creature, rounded animal body, blue green oval belly, tiny paws, tall rainbow quills around the silhouette, dark colorful brush background",
        "cute upright echidna creature, orange snout and cheek, glowing teal belly patch, small clawed hands, rainbow quill mane behind the body, fantasy illustration",
    ]
    subjects = [
        "small upright orange spiny animal",
        "compact fantasy porcupine creature",
        "short upright quilled creature",
        "small orange-faced spiny creature",
        "cute upright echidna creature",
        "round vertical quilled animal",
    ]
    faces = [
        "pointed snout and dark eye",
        "orange face and snout",
        "warm orange animal face",
        "orange snout and cheek",
        "small foxlike orange face",
        "rounded orange muzzle",
    ]
    bellies = [
        "glowing teal oval belly",
        "large teal belly oval",
        "turquoise oval belly gem",
        "blue green oval belly",
        "glowing teal belly patch",
        "bright cyan chest oval",
    ]
    paws = [
        "tiny clawed paws close to the torso",
        "small paws",
        "little claws near the chest",
        "tiny paws",
        "small clawed hands",
        "little forepaws beside the belly",
    ]
    quills = [
        "rainbow quills rising behind the back",
        "rainbow quill halo around the shoulders",
        "rainbow bristles framing the back",
        "tall rainbow quills around the silhouette",
        "rainbow quill mane behind the body",
        "orange yellow blue spines behind the shoulders",
    ]
    styles = [
        "painterly multicolor background",
        "vertical painterly illustration",
        "soft storybook painting",
        "dark colorful brush background",
        "fantasy illustration",
        "glowing orange green color streaks",
    ]
    short_ablation = [
        "small orange spiny creature, teal belly oval, rainbow quills, tiny claws, dark painterly background",
        "upright orange porcupine mascot, glowing teal belly, rainbow back quills, small paws, fantasy painting",
        "orange echidna creature, cyan oval belly, rainbow spines, tiny clawed paws, vertical illustration",
        "round orange quilled animal, teal chest gem, rainbow quill halo, small claws, storybook art",
    ]
    prompts = priority + short_ablation + ordered_variants(
        [subjects, faces, bellies, paws, quills, styles],
        max_permuted_groups=4,
    )
    return entries_for(target, prompts, limit=limit, seed=2938, source=f"{SOURCE}_spiny_creature", head_size=80)


def build_round() -> dict[str, list[dict[str, str]]]:
    return {
        "1159_7.png": cube_hedgehog_prompts(),
        "9338.png": spiny_creature_prompts(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 6 precision ablation prompts.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_06_precision_ablation.json"))
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
