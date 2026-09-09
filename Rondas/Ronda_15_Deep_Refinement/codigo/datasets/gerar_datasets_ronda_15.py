#!/usr/bin/env python3
from __future__ import annotations

import csv
import heapq
import itertools
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[4]
BEST_CSV = ROOT.parent.parent / "best_of_runs" / "best_of_runs.csv"
PT_DIR = ROOT / "pt"
PT_COUNT = 10_000
CATEGORIES = ["1159_7", "9338"]
TOKENIZER_MODEL = "SimianLuo/LCM_Dreamshaper_v7"
MAX_CLIP_TOKENS = 77


def read_top_prompts() -> dict[str, dict[str, object]]:
    rows_by_target: dict[str, list[dict[str, str]]] = {}
    with BEST_CSV.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            target = row["target_name"]
            rows_by_target.setdefault(target, []).append(row)

    result: dict[str, dict[str, object]] = {}
    for target_name, rows in rows_by_target.items():
        sorted_rows = sorted(rows, key=lambda r: float(r.get("cross_run_score") or 0.0), reverse=True)
        prompts_raw = [r["prompt"].strip() for r in sorted_rows]
        unique_prompts: list[str] = []
        seen: set[str] = set()
        for prompt in prompts_raw:
            if prompt in seen:
                continue
            seen.add(prompt)
            unique_prompts.append(prompt)
        category = target_name.replace(".png", "")
        result[category] = {
            "target_name": target_name,
            "top_rows_prompts": prompts_raw[:5],
            "top_unique_prompts": unique_prompts[:5],
        }
    return result


PT_BLOCKS: dict[str, list[dict[str, object]]] = {
    "1159_7": [
        {
            "name": "subject",
            "base": 0,
            "options": [
                "small hedgehog in wooden cube",
                "tiny hedgehog in cube body",
                "cube bodied hedgehog",
                "studio hedgehog wood cube",
                "small animal in cubical block",
                "hedgehog face in wood cube",
                "mini hedgehog carved cube",
            ],
        },
        {
            "name": "cube_structure",
            "base": 0,
            "options": [
                "peach beige square tile sides",
                "pale wood 4x4 cube grid",
                "raised square block sides",
                "stacked wooden cube tiles",
                "balsa cube vertical ridges",
                "modular pale timber sides",
                "crisp sandy cube blocks",
            ],
        },
        {
            "name": "face",
            "base": 0,
            "options": [
                "tiny hidden face front top",
                "small dark eyes tiny nose",
                "face buried under amber fur",
                "muzzle peeking through bristles",
                "black eyes soft nose",
                "low front face in fur",
                "subtle face under quills",
            ],
        },
        {
            "name": "quills",
            "base": 0,
            "options": [
                "long amber top spikes",
                "tall orange radial quills",
                "dense golden top bristles",
                "sharp tan upward fur",
                "copper quills on cube top",
                "square cap of amber bristles",
                "orange fur tall central peaks",
            ],
        },
        {
            "name": "top_surface",
            "base": 0,
            "options": [
                "flat pale top rim visible",
                "square wooden top plane",
                "fur from recessed top opening",
                "clean square top edges",
                "visible timber top face",
                "shallow top square opening",
                "flat cube top around face",
            ],
        },
        {
            "name": "material",
            "base": 0,
            "options": [
                "soft balsa wood grain",
                "matte pale timber texture",
                "warm carved wood ridges",
                "fibrous wooden block texture",
                "natural wood gentle bevels",
                "clean timber tile shadows",
                "slightly fuzzy carved wood",
            ],
        },
        {
            "name": "lighting",
            "base": 0,
            "options": [
                "warm brown studio background",
                "brown tabletop shallow depth",
                "soft product photo lighting",
                "warm macro studio shadows",
                "muted brown creamy highlights",
                "realistic close-up soft shadows",
                "warm low contrast lighting",
            ],
        },
        {
            "name": "composition",
            "base": 0,
            "options": [
                "centered square three quarter view",
                "tight square crop",
                "front three quarter cube view",
                "centered realistic square photo",
                "slightly above close product shot",
                "balanced square crop corners visible",
                "macro focus on face texture",
            ],
        },
    ],
    "9338": [
        {
            "name": "subject",
            "base": 0,
            "options": [
                "rainbow dragon hamster profile",
                "colorful fantasy hamster dragon",
                "small dragon hamster teal belly",
                "bright rainbow hamster creature",
                "storybook dragon hamster scales",
                "round rodent dragon portrait",
                "cute dragon hamster curled tail",
            ],
        },
        {
            "name": "head",
            "base": 0,
            "options": [
                "orange snout glossy black eye",
                "warm orange face tiny muzzle",
                "left-facing head fine whiskers",
                "black eye peach nose",
                "mouse-like orange face whiskers",
                "orange snout looking left",
                "soft peach hamster muzzle",
            ],
        },
        {
            "name": "belly",
            "base": 0,
            "options": [
                "cream chest teal oval belly",
                "pale cream fur blue belly",
                "cyan teal belly scales",
                "rounded blue green belly",
                "cream body bright teal center",
                "beige chest turquoise belly",
                "aqua belly patch near paws",
            ],
        },
        {
            "name": "led_scales",
            "base": 0,
            "options": [
                "tiny LED bead scales",
                "iridescent multicolor dot scales",
                "luminous mosaic scale spots",
                "bright bead scales on body",
                "dense glossy colored dots",
                "jewel-like soft LED scales",
                "painted glowing color dabs",
            ],
        },
        {
            "name": "spines",
            "base": 0,
            "options": [
                "pink horn blue magenta spines",
                "small horn colorful shoulder quills",
                "rainbow back spines blue tail",
                "pink horn pointed ear blue tail",
                "orange yellow blue back spines",
                "turquoise pink dragon ridges",
                "colorful bristles curved tail",
            ],
        },
        {
            "name": "paws",
            "base": 0,
            "options": [
                "small clawed forepaws",
                "tiny paws near teal belly",
                "delicate pale claws",
                "little paws tucked chest",
                "visible small front claws",
                "one rear paw slim claws",
                "mini paws target pose",
            ],
        },
        {
            "name": "background",
            "base": 0,
            "options": [
                "dark background yellow green arcs",
                "blurred yellow teal light trails",
                "dark rainbow aurora strokes",
                "warm yellow green arcs",
                "orange yellow painterly glow",
                "deep teal purple rainbow arcs",
                "soft fantasy curved color bands",
            ],
        },
        {
            "name": "style",
            "base": 0,
            "options": [
                "painterly fantasy square portrait",
                "storybook digital paint texture",
                "detailed fantasy character painting",
                "vertical creature square crop",
                "rich painterly color dabs",
                "whimsical warm rim light",
                "soft concept art portrait",
            ],
        },
    ],
}


def join_prompt(parts: list[str]) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def load_clip_tokenizer():
    try:
        from transformers import AutoTokenizer

        os.environ.setdefault("HF_HOME", str(PROJECT_ROOT / ".hf_cache"))
        return AutoTokenizer.from_pretrained(
            TOKENIZER_MODEL,
            subfolder="tokenizer",
            local_files_only=True,
            use_fast=True,
        )
    except Exception as exc:
        print(f"[Aviso] Tokenizer CLIP local indisponivel; validacao de tokens desativada: {exc}")
        return None


def clip_token_count(prompt: str, tokenizer) -> int | None:
    if tokenizer is None:
        return None
    return len(tokenizer(prompt, truncation=False)["input_ids"])


def combo_distance(combo: tuple[int, ...], blocks: list[dict[str, object]]) -> int:
    score = 0
    for idx, block in zip(combo, blocks):
        score += abs(idx - int(block["base"]))
    return score


def generate_from_blocks(
    blocks: list[dict[str, object]],
    target_count: int,
    tokenizer=None,
) -> tuple[list[dict[str, object]], int]:
    ranges = [range(len(block["options"])) for block in blocks]
    total_space = 1
    for block in blocks:
        total_space *= len(block["options"])

    ranked_combos = heapq.nsmallest(
        target_count,
        ((combo_distance(combo, blocks), combo) for combo in itertools.product(*ranges)),
        key=lambda item: (item[0], item[1]),
    )

    output: list[dict[str, object]] = []
    seen: set[str] = set()
    for rank, (_, combo) in enumerate(ranked_combos, start=1):
        fragments = [str(block["options"][opt_idx]) for block, opt_idx in zip(blocks, combo)]
        prompt = join_prompt(fragments)
        token_count = clip_token_count(prompt, tokenizer)
        if token_count is not None and token_count > MAX_CLIP_TOKENS:
            raise RuntimeError(
                f"Prompt exceeds CLIP limit ({token_count}>{MAX_CLIP_TOKENS}): {prompt}"
            )
        if prompt in seen:
            continue
        seen.add(prompt)
        output.append(
            {
                "id": f"{rank:05d}",
                "seed_index": 1,
                "combo": list(combo),
                "clip_token_count": token_count,
                "prompt": prompt,
            }
        )
        if len(output) >= target_count:
            break

    if len(output) < target_count:
        raise RuntimeError(f"Generated only {len(output)} prompts, expected {target_count}")

    return output, total_space


def build_dataset() -> None:
    top_map = read_top_prompts()
    tokenizer = load_clip_tokenizer()
    PT_DIR.mkdir(parents=True, exist_ok=True)

    manifest_pt: list[dict[str, object]] = []
    for category in CATEGORIES:
        if category not in top_map:
            raise KeyError(f"Category {category} missing in best_of_runs.csv")

        target_name = str(top_map[category]["target_name"])
        top_rows = list(top_map[category]["top_rows_prompts"])
        top_unique = list(top_map[category]["top_unique_prompts"])

        seeds_pt = top_rows[:5]
        if len(seeds_pt) < 5 and top_unique:
            seeds_pt.extend(top_unique[: 5 - len(seeds_pt)])
        if len(seeds_pt) < 5 and top_unique:
            seeds_pt.extend([top_unique[0]] * (5 - len(seeds_pt)))

        prompts_pt, space_pt = generate_from_blocks(
            blocks=PT_BLOCKS[category],
            target_count=PT_COUNT,
            tokenizer=tokenizer,
        )
        max_clip_tokens = max(
            prompt.get("clip_token_count") or 0
            for prompt in prompts_pt
        )
        pt_payload = {
            "category": category,
            "target_name": target_name,
            "language": "pt",
            "prompt_count": PT_COUNT,
            "max_clip_tokens": max_clip_tokens or None,
            "top5_seed_prompts": seeds_pt,
            "variation_blocks": PT_BLOCKS[category],
            "variation_space": space_pt,
            "prompts": prompts_pt,
        }
        pt_path = PT_DIR / f"{category}.json"
        pt_path.write_text(json.dumps(pt_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest_pt.append(
            {
                "category": category,
                "target_name": target_name,
                "path": str(pt_path),
                "prompt_count": PT_COUNT,
                "variation_space": space_pt,
                "max_clip_tokens": max_clip_tokens or None,
            }
        )

    (PT_DIR / "manifest.json").write_text(json.dumps(manifest_pt, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {
        "source_csv": str(BEST_CSV),
        "pt_dir": str(PT_DIR),
        "pt_prompts_per_category": PT_COUNT,
        "max_clip_tokens": MAX_CLIP_TOKENS,
        "categories": CATEGORIES,
        "notes": "Ronda_15 focuses on the cube hedgehog/hamster target 1159_7 and the LED-like rainbow dragon hamster target 9338.",
    }
    (ROOT / "manifest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    build_dataset()
