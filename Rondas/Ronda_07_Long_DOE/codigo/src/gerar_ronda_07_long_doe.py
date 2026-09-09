from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

from tp2_prompt_gen import make_entry, unique_keep_order


SOURCE = "ronda_07_doe_long"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def deterministic_sample(items: list[str], limit: int, seed: int, head_size: int = 80) -> list[str]:
    items = unique_keep_order(items)
    if len(items) <= limit:
        return items
    rng = random.Random(seed)
    head = items[: min(head_size, limit)]
    tail = items[min(head_size, len(items)):]
    rng.shuffle(tail)
    return head + tail[: limit - len(head)]


def add_entries(target: str, prompts: list[str], source: str, offset: int = 1) -> list[dict[str, str]]:
    return [make_entry(target, prompt, index, "", source) for index, prompt in enumerate(prompts, start=offset)]


def grid_prompts(groups: list[list[str]], limit: int, seed: int, priority: list[str] | None = None) -> list[str]:
    prompts = list(priority or [])
    prompts.extend(join_parts(*parts) for parts in itertools.product(*groups))
    return deterministic_sample(prompts, limit=limit, seed=seed)


def cube_hedgehog_blocks() -> list[dict[str, list[str] | int]]:
    winner = (
        "small hedgehog with compact cubical wooden block body, warm peach beige 4 by 4 cube grid sides, "
        "tiny face mostly hidden below orange spiky fur, amber quill fur only on the top surface, realistic studio object photo"
    )
    subjects = [
        "small hedgehog with compact cubical wooden block body",
        "compact cubical wood-block hedgehog",
        "single cube-shaped hedgehog sculpture",
        "hedgehog fused inside a closed wooden cube",
        "tiny hedgehog embedded in a pale wooden block cube",
        "surreal cubical hedgehog object",
        "solid peach wood cube with hidden hedgehog face",
    ]
    sides = [
        "warm peach beige 4 by 4 cube grid sides",
        "front and side faces made of small square wood blocks",
        "straight vertical sides divided into a pale wooden tile grid",
        "regular carved square-block grid on the visible sides",
        "stacked pale wood columns forming a compact cube",
        "visible 4 by 4 peach wood blocks on the front face and right face",
        "neat pale balsa wood cube sides with square tiles",
    ]
    face = [
        "tiny face mostly hidden below orange spiky fur",
        "pinpoint dark eyes and tiny nose recessed into the top front edge",
        "face reduced to two tiny eyes under the top quill crown",
        "small sleepy face buried inside the top front fur",
        "tiny central muzzle barely visible beneath orange bristles",
        "face almost swallowed by the tan orange top fur",
    ]
    top = [
        "amber quill fur only on the top surface",
        "dense orange tan spines rising from the flat top plane",
        "soft amber bristles forming a low square cap on top",
        "orange hedgehog quills concentrated on the top face",
        "tan orange fur spikes covering the top while side walls stay wooden",
        "upward orange quills emerging from the top square",
    ]
    style = [
        "realistic studio object photo",
        "warm brown macro photo",
        "soft shallow depth of field",
        "warm studio product render",
        "centered square crop with gentle shadows",
    ]
    compactness = [
        "body hidden inside the cube",
        "closed cube silhouette",
        "body contained in the wooden block with sides dominant",
        "small face only, cubical body dominant",
        "top fur is compact, sides stay wooden",
    ]
    material = [
        "pale carved wood texture",
        "peach beige wooden material",
        "matte balsa wood surface",
        "soft timber block texture",
        "warm light wood grain",
    ]
    priorities = [
        winner,
        "compact cubical wood-block hedgehog, warm peach beige 4 by 4 cube grid sides, tiny face mostly hidden below orange spiky fur, amber quill fur only on the top surface, realistic studio object photo",
        "small hedgehog with compact cubical wooden block body, body hidden inside the cube, warm peach beige 4 by 4 cube grid sides, tiny face mostly hidden below orange spiky fur, amber quill fur only on the top surface",
        "closed cube silhouette, small hedgehog with compact cubical wooden block body, visible 4 by 4 peach wood blocks on the front face and right face, tiny face mostly hidden below orange spiky fur, orange quills on top",
        "body hidden inside the cube, pale carved wood texture, tiny central muzzle barely visible beneath orange bristles, straight vertical sides divided into a pale wooden tile grid, warm brown macro photo",
    ]
    return [
        {
            "source": f"{SOURCE}_cube_winner_order",
            "limit": 180,
            "seed": 3001,
            "prompts": grid_prompts([subjects, sides, face, top, style], 180, 3001, priorities),
        },
        {
            "source": f"{SOURCE}_cube_structure_first",
            "limit": 180,
            "seed": 3002,
            "prompts": grid_prompts([sides, compactness, subjects, face, top, style], 180, 3002),
        },
        {
            "source": f"{SOURCE}_cube_face_micro",
            "limit": 140,
            "seed": 3003,
            "prompts": grid_prompts([face, subjects, sides, top, material, style], 140, 3003),
        },
        {
            "source": f"{SOURCE}_cube_material_top",
            "limit": 140,
            "seed": 3004,
            "prompts": grid_prompts([material, sides, compactness, top, face, style], 140, 3004),
        },
        {
            "source": f"{SOURCE}_cube_short_prompts",
            "limit": 80,
            "seed": 3005,
            "prompts": deterministic_sample([
                join_parts(subject, side, face_part, top_part)
                for subject, side, face_part, top_part in itertools.product(subjects, sides[:4], face[:4], top[:4])
            ], limit=80, seed=3005, head_size=40),
        },
    ]


def spiny_creature_blocks() -> list[dict[str, list[str] | int]]:
    winner = (
        "tiny clawed paws close to the torso, small upright orange spiny animal, pointed snout and dark eye, "
        "glowing teal oval belly, rainbow quills rising behind the back, painterly multicolor background"
    )
    subjects = [
        "small upright orange spiny animal",
        "small orange-faced quilled creature",
        "round upright echidna-like animal",
        "compact fantasy porcupine creature",
        "short vertical spiny creature",
        "tiny orange snouted quill animal",
    ]
    faces = [
        "pointed snout and dark eye",
        "orange snout and cheek with one dark bead eye",
        "small foxlike orange face",
        "warm orange animal face and tiny nose",
        "orange muzzle with alert dark eye",
    ]
    bellies = [
        "glowing teal oval belly",
        "large blue green oval belly patch",
        "bright cyan oval chest gem",
        "turquoise belly oval centered on the torso",
        "teal oval belly shield",
    ]
    paws = [
        "tiny clawed paws close to the torso",
        "small clawed forepaws beside the belly",
        "little claws held near the teal oval",
        "tiny paws tucked close to the chest",
        "small paws framing the glowing belly",
    ]
    quills = [
        "rainbow quills rising behind the back",
        "rainbow bristles framing the shoulders",
        "orange yellow blue quills along the back",
        "tall rainbow quill halo around the silhouette",
        "curved rainbow spines behind the body",
    ]
    style = [
        "painterly multicolor background",
        "dark teal orange fantasy painting",
        "vertical storybook illustration",
        "soft glowing brushwork",
        "moody orange green light streaks",
    ]
    animality = [
        "animal proportions, small body, short limbs",
        "soft creature portrait with natural fur",
        "rounded animal torso",
        "cute creature silhouette with natural paws",
        "small standing animal shape",
    ]
    priorities = [
        winner,
        "small upright orange spiny animal, pointed snout and dark eye, glowing teal oval belly, tiny clawed paws close to the torso, rainbow quills rising behind the back, painterly multicolor background",
        "small orange-faced quilled creature, orange snout and cheek with one dark bead eye, glowing teal oval belly, small clawed forepaws beside the belly, rainbow bristles framing the shoulders",
        "round upright echidna-like animal, warm orange animal face and tiny nose, large blue green oval belly patch, little claws held near the teal oval, curved rainbow spines behind the body",
    ]
    return [
        {
            "source": f"{SOURCE}_creature_winner_order",
            "limit": 120,
            "seed": 3031,
            "prompts": grid_prompts([subjects, faces, bellies, paws, quills, style], 120, 3031, priorities),
        },
        {
            "source": f"{SOURCE}_creature_animality",
            "limit": 100,
            "seed": 3032,
            "prompts": grid_prompts([animality, subjects, faces, bellies, paws, quills, style], 100, 3032),
        },
        {
            "source": f"{SOURCE}_creature_short_prompts",
            "limit": 80,
            "seed": 3033,
            "prompts": deterministic_sample([
                join_parts(subject, face, belly, paw, quill)
                for subject, face, belly, paw, quill in itertools.product(subjects, faces[:3], bellies[:3], paws[:3], quills[:3])
            ], limit=80, seed=3033, head_size=40),
        },
    ]


def build_round() -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {"1159_7.png": [], "9338.png": []}
    for block in cube_hedgehog_blocks():
        result["1159_7.png"].extend(add_entries("1159_7.png", block["prompts"], str(block["source"]), len(result["1159_7.png"]) + 1))
    for block in spiny_creature_blocks():
        result["9338.png"].extend(add_entries("9338.png", block["prompts"], str(block["source"]), len(result["9338.png"]) + 1))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 7 long design-of-experiments prompt bank.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_07_doe_long.json"))
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
