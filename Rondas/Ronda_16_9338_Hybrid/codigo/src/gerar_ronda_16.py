from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

from tp2_prompt_gen import make_entry, unique_keep_order


SOURCE = "round39_9338_hybrid"
TARGET = "9338.png"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def sample_prompts(prompts: list[str], limit: int, seed: int, head_size: int = 180) -> list[str]:
    prompts = unique_keep_order(prompts)
    if len(prompts) <= limit:
        return prompts
    rng = random.Random(seed)
    head = prompts[: min(head_size, limit)]
    tail = prompts[min(head_size, len(prompts)) :]
    rng.shuffle(tail)
    return head + tail[: limit - len(head)]


def ablate(parts: list[str], min_parts: int = 4) -> list[str]:
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


def reorder_cores(core: list[str], tails: list[str], max_orders: int = 36) -> list[str]:
    prompts: list[str] = []
    for order in list(itertools.permutations(core))[:max_orders]:
        prompts.append(join_parts(*order, *tails))
    return prompts


def entries_for(prompts: list[str], limit: int, seed: int, source: str) -> list[dict[str, str]]:
    prompts = sample_prompts(prompts, limit=limit, seed=seed)
    return [make_entry(TARGET, prompt, index + 1, "", source) for index, prompt in enumerate(prompts)]


def build_9338_prompts(limit: int = 720) -> list[dict[str, str]]:
    # Round38 became too frontal and cute. Round39 restores the stronger target cues:
    # side-facing orange snout, scaled shoulder/back, teal jewel belly, compact small ears.
    anchor_profile = [
        "left facing spiny fantasy rodent",
        "orange pointed snout and small ears",
        "teal spiral jewel belly",
        "rainbow scale armor on shoulder and back",
        "vertical orange yellow flame aura",
        "painterly creature portrait",
    ]
    anchor_target_shape = [
        "small side profile jewel-bellied creature",
        "warm orange muzzle with glossy black eye",
        "blue teal chest medallion",
        "colored scale plates along the back",
        "compact paws close to body",
        "dark teal rainbow fire background",
    ]
    anchor_texture = [
        "compact spiny rodent creature",
        "orange face turned left",
        "turquoise oval belly gem",
        "dense rainbow scales and thorny quills",
        "small clawed forepaws",
        "storybook fantasy painting",
    ]
    anchors = [
        join_parts(*anchor_profile),
        join_parts(*anchor_target_shape),
        join_parts(*anchor_texture),
        "left facing orange spiny rodent, glossy black eye, turquoise spiral belly jewel, rainbow scale plates on the back, tiny paws, vertical flame aura",
        "small fantasy creature in side view, orange muzzle, teal oval chest gem, multicolor scales on shoulder, thorny back quills, dark teal orange glow",
        "profile view jewel-bellied spiny pet, short ears, orange snout, blue green belly medallion, rainbow armor scales, painterly fire ribbons",
        "compact left-facing quilled creature, orange head, small rounded ears, turquoise chest oval, colorful scale armor, yellow orange aura",
        "storybook spiny rodent portrait, side profile face, teal belly jewel, rainbow scales down the back, tiny claws, smoky multicolor background",
    ]
    subjects = [
        "left facing spiny fantasy rodent",
        "small side profile jewel-bellied creature",
        "compact spiny rodent creature",
        "profile view jewel-bellied spiny pet",
        "compact left-facing quilled creature",
        "storybook spiny rodent portrait",
        "small scaled fantasy rodent",
        "orange teal quilled creature in side view",
    ]
    face = [
        "orange pointed snout and small ears",
        "warm orange muzzle with glossy black eye",
        "orange face turned left",
        "side profile face with black eye",
        "short ears and orange snout",
    ]
    belly = [
        "teal spiral jewel belly",
        "blue teal chest medallion",
        "turquoise oval belly gem",
        "teal oval chest jewel",
        "blue green glowing belly medallion",
    ]
    texture = [
        "rainbow scale armor on shoulder and back",
        "colored scale plates along the back",
        "dense rainbow scales and thorny quills",
        "multicolor scales on shoulder",
        "rainbow scales down the back",
        "colorful scale armor and short quills",
    ]
    pose = [
        "three quarter left profile",
        "compact body turned left",
        "asymmetric side view silhouette",
        "single small creature facing left",
        "head looking left over rounded body",
    ]
    paws = [
        "compact paws close to body",
        "small clawed forepaws",
        "tiny paws held near the belly",
        "small pale claws near torso",
    ]
    aura = [
        "vertical orange yellow flame aura",
        "dark teal rainbow fire background",
        "painterly fire ribbons behind",
        "yellow orange aura around the body",
        "soft multicolor flames rising behind",
    ]
    style = [
        "painterly creature portrait",
        "storybook fantasy painting",
        "soft brushwork fantasy illustration",
        "vertical digital painting",
    ]

    prompts = list(anchors)
    prompts.extend(ablate(anchor_profile))
    prompts.extend(ablate(anchor_target_shape))
    prompts.extend(ablate(anchor_texture))
    prompts.extend(reorder_cores(anchor_profile[:5], [anchor_profile[5]], max_orders=36))
    prompts.extend(reorder_cores([anchor_profile[0], anchor_profile[2], anchor_profile[3], anchor_profile[4]], ["side profile", "storybook painting"], max_orders=36))
    prompts.extend(
        join_parts(subject, pose_part, face_part, belly_part, texture_part, paw, aura_part, style_part)
        for subject, pose_part, face_part, belly_part, texture_part, paw, aura_part, style_part in itertools.product(
            subjects, pose, face, belly, texture, paws, aura, style
        )
    )
    prompts.extend(
        join_parts(subject, face_part, "short ears", belly_part, texture_part, "single asymmetric silhouette", aura_part)
        for subject, face_part, belly_part, texture_part, aura_part in itertools.product(
            subjects[:6], face, belly, texture, aura[:4]
        )
    )
    prompts.extend(
        join_parts("side profile", texture_part, subject, belly_part, face_part, "compact paws", style_part)
        for texture_part, subject, belly_part, face_part, style_part in itertools.product(
            texture, subjects[:5], belly, face[:4], style[:3]
        )
    )
    return entries_for(prompts, limit=limit, seed=3938, source=f"{SOURCE}_side_scales")


def build_round() -> dict[str, list[dict[str, str]]]:
    return {TARGET: build_9338_prompts()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 round-39 9338 hybrid repair prompt bank.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_round39_9338_hybrid.json"))
    args = parser.parse_args()

    data = build_round()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {sum(len(entries) for entries in data.values())} prompts to {args.output}")


if __name__ == "__main__":
    main()
