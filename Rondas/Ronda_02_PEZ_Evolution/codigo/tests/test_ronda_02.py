from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_02_pez_evolution import (
    build_evolutionary_round,
    build_pez_configs,
    clean_phrase,
    merge_rounds,
)


def test_ronda_02_evolutionary_targets_and_counts():
    data = build_evolutionary_round(evolution_limit=12)

    assert set(data) == {"1159_7.png", "9338.png"}
    assert len(data["1159_7.png"]) == 12
    assert len(data["9338.png"]) == 12
    assert all(entry["negative_prompt"] == "" for entries in data.values() for entry in entries)


def test_ronda_02_prompts_focus_on_known_failure_modes():
    data = build_evolutionary_round(evolution_limit=20)

    cube_prompts = " ".join(entry["prompt"].lower() for entry in data["1159_7.png"])
    creature_prompts = " ".join(entry["prompt"].lower() for entry in data["9338.png"])

    assert "cube" in cube_prompts
    assert "front" in cube_prompts
    assert "top" in cube_prompts
    assert "orange" in creature_prompts
    assert "teal" in creature_prompts or "turquoise" in creature_prompts
    assert "rainbow" in creature_prompts
    assert "dragon" not in creature_prompts


def test_pez_configs_are_discrete_prompt_templates():
    configs = build_pez_configs(restarts=1, steps=1, phrase_limit=3)

    assert set(configs) == {"1159_7.png", "9338.png"}
    for config in configs.values():
        assert "{phrase}" in " ".join(config.base_templates)
        assert config.slot_count > 0
        assert config.seed_words
        assert config.banned_terms


def test_clean_phrase_filters_banned_and_duplicates():
    phrase = clean_phrase(["cube", "cube", "dragon", "tiles"], {"dragon"})

    assert phrase == "cube tiles"


def test_merge_rounds_reindexes_plain_text_entries():
    evolution = build_evolutionary_round(evolution_limit=3)
    merged = merge_rounds(evolution, {}, final_limit_per_target=2)

    assert len(merged["1159_7.png"]) == 2
    assert merged["1159_7.png"][0]["id"].startswith("1159_7_ronda_02_pez_evolution_")
    assert merged["1159_7.png"][0]["negative_prompt"] == ""
