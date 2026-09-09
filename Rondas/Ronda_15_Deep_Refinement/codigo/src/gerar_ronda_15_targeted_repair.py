from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

from tp2_prompt_gen import make_entry, unique_keep_order


SOURCE = "round38_targeted_repair"


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def sample_prompts(prompts: list[str], limit: int, seed: int, head_size: int = 140) -> list[str]:
    prompts = unique_keep_order(prompts)
    if len(prompts) <= limit:
        return prompts
    rng = random.Random(seed)
    head = prompts[: min(head_size, limit)]
    tail = prompts[min(head_size, len(prompts)) :]
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


def reorder_cores(core: list[str], tails: list[str], max_orders: int = 32) -> list[str]:
    prompts: list[str] = []
    for order in list(itertools.permutations(core))[:max_orders]:
        prompts.append(join_parts(*order, *tails))
    return prompts


def entries_for(target: str, prompts: list[str], limit: int, seed: int, source: str) -> list[dict[str, str]]:
    prompts = sample_prompts(prompts, limit=limit, seed=seed)
    return [make_entry(target, prompt, index + 1, "", source) for index, prompt in enumerate(prompts)]


def quilled_hamster_prompts(limit: int = 560) -> list[dict[str, str]]:
    target = "9338.png"
    short_anchor = [
        "small quilled fantasy hamster creature",
        "orange snout",
        "teal oval belly",
        "rainbow scale quills",
        "vertical flame aura",
    ]
    color_anchor = [
        "compact rainbow quilled hamster",
        "warm orange face and dark glossy eyes",
        "turquoise chest oval",
        "tiny paws near belly",
        "dark teal orange glowing background",
    ]
    shape_anchor = [
        "upright spiny hamster creature",
        "round orange head and blue green belly patch",
        "painted rainbow bristles behind shoulders",
        "little paws tucked close",
        "storybook creature painting",
    ]
    anchors = [
        join_parts(*short_anchor),
        join_parts(*color_anchor),
        join_parts(*shape_anchor),
        "storybook quilled hamster, orange animal face, clear teal belly gem, rainbow back bristles, tiny forepaws, vertical orange teal flame aura",
        "small orange teal scale-quilled hamster, pointed muzzle, turquoise oval chest, colorful shoulder spines, soft fantasy portrait",
        "compact spiny fantasy pet, orange snout and glossy eye, teal oval belly, rainbow scale quills around the back, painterly glow",
        "round fantasy hamster with colored quills, orange muzzle, blue green belly patch, small paws, warm brushwork",
    ]
    subjects = [
        "small quilled fantasy hamster creature",
        "compact rainbow quilled hamster",
        "upright spiny hamster creature",
        "small orange teal scale-quilled hamster",
        "storybook quilled hamster",
        "round fantasy hamster with colored quills",
        "compact spiny fantasy pet",
        "small upright orange spiny animal",
    ]
    face = [
        "orange snout and dark glossy eyes",
        "warm orange animal face",
        "pointed orange muzzle",
        "small orange muzzle and whiskers",
        "round orange head with black eye",
    ]
    belly = [
        "teal oval belly",
        "turquoise chest oval",
        "blue green belly patch",
        "clear teal belly gem",
        "glowing teal oval chest",
    ]
    quills = [
        "rainbow scale quills",
        "painted rainbow bristles behind shoulders",
        "orange blue yellow shoulder quills",
        "colorful scale spines around the back",
        "rainbow back bristles",
    ]
    paws = [
        "tiny forepaws near the belly",
        "small clawed paws close to torso",
        "little paws tucked near chest",
        "tiny paws near belly",
    ]
    aura = [
        "vertical flame aura",
        "vertical orange teal flame aura",
        "soft rainbow flame shapes behind",
        "dark teal orange glowing background",
        "painted multicolor aura rising behind",
    ]
    style = [
        "vertical storybook illustration",
        "soft painterly fantasy portrait",
        "storybook creature painting",
        "warm brushwork",
    ]
    prompts = list(anchors)
    prompts.extend(ablate(short_anchor))
    prompts.extend(ablate(color_anchor))
    prompts.extend(ablate(shape_anchor))
    prompts.extend(reorder_cores(short_anchor[:4], [short_anchor[4]], max_orders=32))
    prompts.extend(reorder_cores([short_anchor[0], short_anchor[2], short_anchor[3], "tiny paws"], ["storybook painting"], max_orders=32))
    prompts.extend(
        join_parts(subject, face_part, belly_part, quill, paw, aura_part, style_part)
        for subject, face_part, belly_part, quill, paw, aura_part, style_part in itertools.product(
            subjects, face, belly, quills, paws, aura, style
        )
    )
    prompts.extend(
        join_parts(subject, "single central creature", belly_part, face_part, quill, aura_part)
        for subject, belly_part, face_part, quill, aura_part in itertools.product(
            subjects[:6], belly, face[:4], quills, aura[:4]
        )
    )
    return entries_for(target, prompts, limit=limit, seed=3838, source=f"{SOURCE}_9338_no_dragon_tokens")


def astronaut_prompts(limit: int = 360) -> list[dict[str, str]]:
    target = "7836.png"
    geometry_anchor = [
        "tiny astronaut at bottom center",
        "curved grey planet ridge",
        "wide diagonal pink white cosmic dust band",
        "deep blue black starfield",
        "cinematic sci fi digital painting",
    ]
    contrast_anchor = [
        "small space explorer on lower grey arc",
        "broad luminous diagonal galaxy dust lane",
        "dark empty space around the figure",
        "pink white nebula stripe crossing the sky",
        "high contrast space concept art",
    ]
    anchors = [
        join_parts(*geometry_anchor),
        join_parts(*contrast_anchor),
        "tiny rim lit astronaut, bottom center grey crescent ground, sloping pink white nebula stripe, deep starry blue sky, realistic sci fi painting",
        "small explorer near lower edge, curved moon surface, diagonal magenta white dust lane across dark space, moody cinematic art",
    ]
    subject = [
        "tiny astronaut at bottom center",
        "small space explorer on curved grey ground",
        "small rim lit explorer near lower edge",
        "tiny suited figure standing on moonlike ridge",
    ]
    stripe = [
        "wide diagonal pink white cosmic dust band",
        "sloping pink white nebula stripe across the sky",
        "broad luminous diagonal galaxy dust lane",
        "diagonal magenta white dust lane across dark space",
    ]
    sky = [
        "deep blue black starfield",
        "empty dark cosmic sky",
        "dark blue space background",
        "sparse stars in black blue sky",
    ]
    ground = [
        "curved grey planet ridge at bottom",
        "thin rim lit ground arc below figure",
        "small crescent ground under explorer",
        "lower grey moon surface curve",
    ]
    style = [
        "cinematic sci fi digital painting",
        "high contrast space concept art",
        "moody realistic sci fi landscape",
        "dramatic space illustration",
    ]
    prompts = list(anchors)
    prompts.extend(ablate(geometry_anchor))
    prompts.extend(ablate(contrast_anchor))
    prompts.extend(reorder_cores(geometry_anchor[:4], [geometry_anchor[4]], max_orders=32))
    prompts.extend(
        join_parts(subject_part, ground_part, stripe_part, sky_part, style_part)
        for subject_part, ground_part, stripe_part, sky_part, style_part in itertools.product(
            subject, ground, stripe, sky, style
        )
    )
    prompts.extend(
        join_parts(stripe_part, subject_part, ground_part, sky_part, "strong diagonal composition", style_part)
        for stripe_part, subject_part, ground_part, sky_part, style_part in itertools.product(
            stripe, subject[:3], ground[:3], sky[:3], style[:3]
        )
    )
    return entries_for(target, prompts, limit=limit, seed=37836, source=f"{SOURCE}_7836_diagonal_astronaut")


def warrior_prompts(limit: int = 260) -> list[dict[str, str]]:
    target = "1159_3.png"
    anchor = [
        "armored fantasy warrior",
        "large curved blade held across the body",
        "dark red and steel armor",
        "glowing warm background",
        "vertical character illustration",
    ]
    compact_anchor = [
        "central warrior figure",
        "helmet and shoulder armor",
        "broad weapon silhouette",
        "orange backlight",
        "painterly game art",
    ]
    anchors = [
        join_parts(*anchor),
        join_parts(*compact_anchor),
        "armored fighter in dark red metal, curved blade crossing front, warm golden glow behind, centered fantasy character art",
        "single heroic warrior, heavy shoulder plates, long blade, smoky orange background, vertical digital painting",
    ]
    subject = [
        "armored fantasy warrior",
        "central warrior figure",
        "single heroic warrior",
        "armored fighter in dark red metal",
    ]
    armor = [
        "dark red and steel armor",
        "helmet and shoulder armor",
        "heavy shoulder plates",
        "ornate metal chest armor",
    ]
    weapon = [
        "large curved blade held across the body",
        "broad weapon silhouette",
        "long blade crossing the front",
        "curved sword angled through the composition",
    ]
    background = [
        "glowing warm background",
        "orange backlight",
        "smoky orange background",
        "golden firelit atmosphere",
    ]
    style = [
        "vertical character illustration",
        "painterly game art",
        "fantasy concept art portrait",
        "dramatic digital painting",
    ]
    prompts = list(anchors)
    prompts.extend(ablate(anchor))
    prompts.extend(ablate(compact_anchor))
    prompts.extend(reorder_cores(anchor[:4], [anchor[4]], max_orders=32))
    prompts.extend(
        join_parts(subject_part, armor_part, weapon_part, background_part, style_part)
        for subject_part, armor_part, weapon_part, background_part, style_part in itertools.product(
            subject, armor, weapon, background, style
        )
    )
    prompts.extend(
        join_parts(weapon_part, subject_part, armor_part, "centered cropped body", background_part, style_part)
        for weapon_part, subject_part, armor_part, background_part, style_part in itertools.product(
            weapon, subject[:3], armor[:3], background[:3], style[:3]
        )
    )
    return entries_for(target, prompts, limit=limit, seed=31159, source=f"{SOURCE}_1159_3_warrior_structure")


def cube_hedgehog_prompts(limit: int = 220) -> list[dict[str, str]]:
    target = "1159_7.png"
    anchor = [
        "small cubical hedgehog object",
        "peach 4 by 4 grid cube sides",
        "tiny hidden face under front quills",
        "fine amber top spines only",
        "warm brown macro photo",
    ]
    locked_anchor = [
        "compact block hedgehog",
        "visible square cell front and right sides",
        "orange quill crown on top",
        "tiny dark nose at upper front edge",
        "realistic studio crop",
    ]
    anchors = [
        join_parts(*anchor),
        join_parts(*locked_anchor),
        "cube shaped hedgehog, peach square lattice sides, top orange quills, tiny buried face, centered warm studio object photo",
        "small block animal, regular peach grid sides, amber hairlike top surface, hidden eyes and nose, brown macro lighting",
    ]
    subject = [
        "small cubical hedgehog object",
        "compact block hedgehog",
        "cube shaped hedgehog",
        "tiny hedgehog cube sculpture",
    ]
    sides = [
        "peach 4 by 4 grid cube sides",
        "visible square cell front and right sides",
        "regular peach grid sides",
        "front and right faces made of small square blocks",
    ]
    face = [
        "tiny hidden face under front quills",
        "tiny dark nose at upper front edge",
        "hidden eyes and nose below top fur",
        "small centered face partly buried",
    ]
    top = [
        "fine amber top spines only",
        "orange quill crown on top",
        "amber hairlike top surface",
        "compact orange top tuft",
    ]
    style = [
        "warm brown macro photo",
        "realistic studio crop",
        "centered product photo",
        "soft brown studio lighting",
    ]
    prompts = list(anchors)
    prompts.extend(ablate(anchor))
    prompts.extend(ablate(locked_anchor))
    prompts.extend(reorder_cores(anchor[:4], [anchor[4]], max_orders=24))
    prompts.extend(
        join_parts(subject_part, sides_part, face_part, top_part, style_part)
        for subject_part, sides_part, face_part, top_part, style_part in itertools.product(
            subject, sides, face, top, style
        )
    )
    return entries_for(target, prompts, limit=limit, seed=31197, source=f"{SOURCE}_1159_7_locked_cube")


def build_round() -> dict[str, list[dict[str, str]]]:
    return {
        "9338.png": quilled_hamster_prompts(),
        "7836.png": astronaut_prompts(),
        "1159_3.png": warrior_prompts(),
        "1159_7.png": cube_hedgehog_prompts(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 round-38 targeted repair prompt bank.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_round38_targeted_repair.json"))
    args = parser.parse_args()

    data = build_round()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    total = sum(len(entries) for entries in data.values())
    print(f"Wrote {total} prompts to {args.output}")


if __name__ == "__main__":
    main()
