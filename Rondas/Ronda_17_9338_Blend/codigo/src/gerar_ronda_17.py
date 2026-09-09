from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

from tp2_prompt_gen import make_entry, unique_keep_order


SOURCE = "round40_9338_blend"
TARGET = "9338.png"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def sample_prompts(prompts: list[str], limit: int, seed: int, head_size: int = 200) -> list[str]:
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


def reorder_cores(core: list[str], tails: list[str], max_orders: int = 42) -> list[str]:
    prompts: list[str] = []
    for order in list(itertools.permutations(core))[:max_orders]:
        prompts.append(join_parts(*order, *tails))
    return prompts


def entries_for(prompts: list[str], limit: int, seed: int, source: str) -> list[dict[str, str]]:
    prompts = sample_prompts(prompts, limit=limit, seed=seed)
    return [make_entry(TARGET, prompt, index + 1, "", source) for index, prompt in enumerate(prompts)]


def build_9338_prompts(limit: int = 760) -> list[dict[str, str]]:
    # Round40 blends Round38 color/hamster semantics with Round39 side-profile cues.
    # It avoids terms that pulled the model to large reptile bodies or realistic rodents.
    anchor_balanced = [
        "colorful fantasy hamster creature",
        "three quarter left profile",
        "orange rounded snout and small ears",
        "teal spiral belly jewel",
        "rainbow scale quills on shoulder and back",
        "orange yellow flame aura",
        "storybook painterly illustration",
    ]
    anchor_compact = [
        "compact orange teal quilled hamster",
        "head turned left with glossy black eye",
        "blue green oval belly medallion",
        "short colorful scales around the back",
        "tiny paws close to the belly",
        "dark teal multicolor fire background",
    ]
    anchor_soft = [
        "small magical spiny hamster",
        "side facing orange face",
        "clear turquoise chest gem",
        "painted rainbow bristles behind the shoulders",
        "rounded compact cute body",
        "soft fantasy creature portrait",
    ]
    anchors = [
        join_parts(*anchor_balanced),
        join_parts(*anchor_compact),
        join_parts(*anchor_soft),
        "orange colorful fantasy hamster, three quarter left profile, teal belly jewel, rainbow scale quills, compact cute body, painterly flame aura",
        "storybook orange teal hamster creature, head turned left, small ears, turquoise belly medallion, multicolor scales on shoulder, tiny claws, warm fire ribbons",
        "compact jewel-bellied fantasy hamster, side facing orange snout, black glossy eye, rainbow quilled back, blue green belly gem, dark teal orange aura",
        "small magical hamster in left profile, rounded body, clear teal chest jewel, colored scale armor, short quills, vertical storybook painting",
        "cute spiny fantasy hamster, orange face turned left, turquoise oval belly, rainbow shoulder scales, tiny paws, yellow orange flame background",
    ]
    subjects = [
        "colorful fantasy hamster creature",
        "compact orange teal quilled hamster",
        "small magical spiny hamster",
        "storybook orange teal hamster creature",
        "compact jewel-bellied fantasy hamster",
        "cute spiny fantasy hamster",
        "small rainbow quilled hamster creature",
        "orange teal fantasy hamster with scales",
    ]
    pose = [
        "three quarter left profile",
        "head turned left with compact body",
        "side facing orange face",
        "soft left profile pose",
        "slightly turned left silhouette",
        "single creature looking left",
    ]
    face = [
        "orange rounded snout and small ears",
        "head turned left with glossy black eye",
        "side facing orange face",
        "small orange muzzle and black eye",
        "short ears with warm orange snout",
    ]
    belly = [
        "teal spiral belly jewel",
        "blue green oval belly medallion",
        "clear turquoise chest gem",
        "turquoise oval belly",
        "blue green glowing belly patch",
    ]
    texture = [
        "rainbow scale quills on shoulder and back",
        "short colorful scales around the back",
        "painted rainbow bristles behind the shoulders",
        "multicolor scales on shoulder",
        "rainbow quilled back",
        "colored scale armor and short quills",
    ]
    body = [
        "rounded compact cute body",
        "compact cute body",
        "small body with tiny paws",
        "tiny paws close to the belly",
        "small clawed paws near torso",
    ]
    aura = [
        "orange yellow flame aura",
        "dark teal multicolor fire background",
        "warm fire ribbons behind",
        "yellow orange painterly aura",
        "soft rainbow flame shapes behind",
    ]
    style = [
        "storybook painterly illustration",
        "soft fantasy creature portrait",
        "vertical storybook painting",
        "warm brushwork fantasy portrait",
    ]

    prompts = list(anchors)
    prompts.extend(ablate(anchor_balanced))
    prompts.extend(ablate(anchor_compact))
    prompts.extend(ablate(anchor_soft))
    prompts.extend(reorder_cores(anchor_balanced[:6], [anchor_balanced[6]], max_orders=42))
    prompts.extend(reorder_cores([anchor_balanced[0], anchor_balanced[1], anchor_balanced[3], anchor_balanced[4]], ["compact cute body", "storybook painting"], max_orders=42))
    prompts.extend(
        join_parts(subject, pose_part, face_part, belly_part, texture_part, body_part, aura_part, style_part)
        for subject, pose_part, face_part, belly_part, texture_part, body_part, aura_part, style_part in itertools.product(
            subjects, pose, face, belly, texture, body, aura, style
        )
    )
    prompts.extend(
        join_parts(subject, face_part, belly_part, texture_part, "compact left profile", aura_part, style_part)
        for subject, face_part, belly_part, texture_part, aura_part, style_part in itertools.product(
            subjects[:6], face, belly, texture, aura[:4], style[:3]
        )
    )
    prompts.extend(
        join_parts("three quarter left profile", subject, "small ears", belly_part, texture_part, body_part, "orange teal color harmony", style_part)
        for subject, belly_part, texture_part, body_part, style_part in itertools.product(
            subjects[:6], belly, texture, body[:4], style[:3]
        )
    )
    return entries_for(prompts, limit=limit, seed=409338, source=f"{SOURCE}_round38_round39_mix")


def build_round() -> dict[str, list[dict[str, str]]]:
    return {TARGET: build_9338_prompts()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 round-40 9338 blended prompt bank.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_round40_9338_blend.json"))
    args = parser.parse_args()

    data = build_round()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {sum(len(entries) for entries in data.values())} prompts to {args.output}")


if __name__ == "__main__":
    main()
