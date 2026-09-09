from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

from tp2_prompt_gen import make_entry, unique_keep_order


SOURCE = "ronda_12_maxstack"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def sample_prompts(prompts: list[str], limit: int, seed: int, head_size: int = 120) -> list[str]:
    prompts = unique_keep_order(prompts)
    if len(prompts) <= limit:
        return prompts
    rng = random.Random(seed)
    head = prompts[: min(head_size, limit)]
    tail = prompts[min(head_size, len(prompts)):]
    rng.shuffle(tail)
    return head + tail[: limit - len(head)]


def ablate(parts: list[str], min_parts: int = 3) -> list[str]:
    prompts = [join_parts(*parts)]
    for index in range(len(parts)):
        kept = [part for i, part in enumerate(parts) if i != index]
        if len(kept) >= min_parts:
            prompts.append(join_parts(*kept))
    for i, j in itertools.combinations(range(len(parts)), 2):
        kept = [part for k, part in enumerate(parts) if k not in {i, j}]
        if len(kept) >= min_parts:
            prompts.append(join_parts(*kept))
    return prompts


def reorder_cores(core: list[str], tails: list[str], max_orders: int = 24) -> list[str]:
    prompts: list[str] = []
    for order in list(itertools.permutations(core))[:max_orders]:
        prompts.append(join_parts(*order, *tails))
    return prompts


def entries_for(target: str, prompts: list[str], limit: int, seed: int, source: str) -> list[dict[str, str]]:
    prompts = sample_prompts(prompts, limit=limit, seed=seed)
    return [make_entry(target, prompt, index + 1, "", source) for index, prompt in enumerate(prompts)]


def cube_prompts(limit: int = 420) -> list[dict[str, str]]:
    target = "1159_7.png"
    best_long = [
        "small hedgehog with compact cubical wooden block body",
        "warm peach beige 4 by 4 cube grid sides",
        "tiny face mostly hidden below orange spiky fur",
        "amber quill fur only on the top surface",
        "realistic studio object photo",
    ]
    best_short = [
        "cube hedgehog",
        "peach 4x4 grid sides",
        "tiny hidden face",
        "orange top quills",
        "brown studio",
    ]
    structure = [
        "compact cubical hedgehog object",
        "visible 4 by 4 peach block sides",
        "small centered face under top quills",
        "fine amber hairlike quills on top only",
        "warm macro product photo",
    ]
    anchors = [
        join_parts(*best_long),
        join_parts(*best_short),
        join_parts(*structure),
        "cube hedgehog, visible 4 by 4 peach block sides, tiny dark nose at top front, fine orange quills on top only, warm brown macro photo",
        "compact cubical hedgehog, peach square grid sides, hidden tiny face, thin amber quill crown, realistic studio photo",
        "small block hedgehog, 4x4 cubical sides, tiny buried face, orange hairlike top quills, centered brown studio crop",
    ]
    subjects = [
        "cube hedgehog",
        "compact cubical hedgehog",
        "small block hedgehog",
        "cubical hedgehog object",
        "hedgehog cube sculpture",
        "tiny hedgehog in peach block cube",
    ]
    sides = [
        "peach 4x4 grid sides",
        "visible 4 by 4 peach block sides",
        "square cell cube sides",
        "straight vertical block grid sides",
        "front and right faces made of small peach cubes",
        "regular peach square lattice sides",
    ]
    face = [
        "tiny hidden face",
        "tiny dark nose at top front",
        "small centered face under top quills",
        "pinpoint eyes and nose in top front edge",
        "buried hedgehog face below orange fur",
    ]
    top = [
        "orange top quills",
        "fine orange quills on top only",
        "amber hairlike top spines",
        "thin amber quill crown",
        "compact messy orange top tuft",
    ]
    style = [
        "warm brown macro photo",
        "realistic studio photo",
        "soft product render",
        "centered brown studio crop",
    ]
    prompts = list(anchors)
    prompts.extend(ablate(best_long))
    prompts.extend(ablate(best_short))
    prompts.extend(ablate(structure))
    prompts.extend(reorder_cores(best_short[:4], [best_short[4]], max_orders=24))
    prompts.extend(reorder_cores([best_short[0], best_short[1], best_short[2], "fine orange quills"], ["warm macro"], max_orders=24))
    prompts.extend(
        join_parts(subject, side, face_part, top_part, style_part)
        for subject, side, face_part, top_part, style_part in itertools.product(subjects, sides, face, top, style)
    )
    prompts.extend(
        join_parts(side, subject, face_part, top_part, style_part)
        for side, subject, face_part, top_part, style_part in itertools.product(
            sides[:5], subjects[:5], face[:4], top[:4], style[:3]
        )
    )
    prompts.extend(
        join_parts(subject, "closed cube silhouette", side, "sides stay visible", face_part, top_part)
        for subject, side, face_part, top_part in itertools.product(subjects[:4], sides[:4], face[:4], top[:4])
    )
    return entries_for(target, prompts, limit=limit, seed=3507, source=f"{SOURCE}_cube_all_techniques")


def dragon_prompts(limit: int = 440) -> list[dict[str, str]]:
    target = "9338.png"
    best_ronda_08 = [
        "colorful dragon hamster with orange face and teal belly",
        "rainbow quills behind the back",
        "tiny clawed paws",
        "vertical storybook illustration",
    ]
    balanced = [
        "dragon hamster",
        "orange face and teal oval belly",
        "rainbow back quills",
        "tiny clawed paws",
        "dark teal orange flame aura",
    ]
    spiny = [
        "compact fantasy quilled hamster creature",
        "pointed orange snout and dark eye",
        "turquoise oval belly",
        "painted rainbow scale spines",
        "vertical storybook painting",
    ]
    anchors = [
        join_parts(*best_ronda_08),
        join_parts(*balanced),
        join_parts(*spiny),
        "dragon hamster, orange face, teal oval belly, rainbow quills, tiny clawed paws, dark teal orange flame aura, storybook painting",
        "orange teal dragon hamster, compact upright body, pointed orange snout, turquoise belly, rainbow back quills, small paws, vertical storybook illustration",
        "spiky hamster dragon, side profile orange face, blue green belly, painted rainbow spines, tiny claws, dark fantasy glow",
    ]
    subjects = [
        "dragon hamster",
        "orange teal dragon hamster",
        "spiky hamster dragon",
        "quilled dragon hamster",
        "compact fantasy quilled hamster creature",
        "small upright orange spiny animal",
    ]
    pose = [
        "compact upright body",
        "round vertical body",
        "side profile orange face",
        "small standing animal shape",
    ]
    face = [
        "orange face",
        "pointed orange snout and dark eye",
        "small orange muzzle",
        "warm orange animal face",
    ]
    belly = [
        "teal oval belly",
        "turquoise belly",
        "blue green chest oval",
        "glowing teal belly patch",
    ]
    quills = [
        "rainbow back quills",
        "painted rainbow scale spines",
        "orange teal quills",
        "rainbow bristles behind the shoulders",
    ]
    paws = [
        "tiny clawed paws",
        "small paws near belly",
        "little claws close to torso",
    ]
    style = [
        "vertical storybook illustration",
        "dark teal orange flame aura",
        "painterly multicolor background",
        "soft glowing brushwork",
    ]
    prompts = list(anchors)
    prompts.extend(ablate(best_ronda_08, min_parts=3))
    prompts.extend(ablate(balanced, min_parts=3))
    prompts.extend(ablate(spiny, min_parts=3))
    prompts.extend(reorder_cores(balanced[:4], [balanced[4]], max_orders=24))
    prompts.extend(reorder_cores([balanced[0], balanced[1], "painted rainbow spines", balanced[3]], ["storybook painting"], max_orders=24))
    prompts.extend(
        join_parts(subject, face_part, belly_part, quill, paw, style_part)
        for subject, face_part, belly_part, quill, paw, style_part in itertools.product(
            subjects, face, belly, quills, paws, style
        )
    )
    prompts.extend(
        join_parts(subject, pose_part, face_part, belly_part, quill, paw, style_part)
        for subject, pose_part, face_part, belly_part, quill, paw, style_part in itertools.product(
            subjects[:5], pose, face, belly, quills, paws[:2], style[:3]
        )
    )
    prompts.extend(
        join_parts(subject, "single central creature", pose_part, face_part, belly_part, quill, style_part)
        for subject, pose_part, face_part, belly_part, quill, style_part in itertools.product(
            subjects[:5], pose[:3], face[:3], belly[:3], quills[:3], style[:3]
        )
    )
    return entries_for(target, prompts, limit=limit, seed=3538, source=f"{SOURCE}_dragon_all_techniques")


def build_round() -> dict[str, list[dict[str, str]]]:
    return {
        "1159_7.png": cube_prompts(),
        "9338.png": dragon_prompts(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 12 max-stack prompt bank.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_12_maxstack.json"))
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
