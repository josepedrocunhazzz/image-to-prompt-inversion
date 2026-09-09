from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_07_long_doe import build_round


def test_ronda_07_targets_and_counts():
    data = build_round()

    assert set(data) == {"1159_7.png", "9338.png"}
    assert len(data["1159_7.png"]) == 720
    assert len(data["9338.png"]) == 300
    assert sum(len(entries) for entries in data.values()) == 1020


def test_ronda_07_plain_positive_prompts():
    data = build_round()
    blocked = [" no ", " not ", " without ", " negative prompt", "avoid"]

    for entries in data.values():
        for entry in entries:
            prompt = f" {entry['prompt'].lower()} "
            assert entry["negative_prompt"] == ""
            assert entry["source"].startswith("ronda_07_doe_long")
            for token in blocked:
                assert token not in prompt


def test_ronda_07_cube_has_multiple_controlled_blocks():
    entries = build_round()["1159_7.png"]
    sources = {entry["source"] for entry in entries}
    prompts = " ".join(entry["prompt"].lower() for entry in entries[:120])

    assert len(sources) == 5
    assert "4 by 4" in prompts
    assert "hidden" in prompts or "buried" in prompts
    assert "top" in prompts
    assert "wood" in prompts


def test_ronda_07_creature_has_animality_and_winner_blocks():
    entries = build_round()["9338.png"]
    sources = {entry["source"] for entry in entries}
    prompts = " ".join(entry["prompt"].lower() for entry in entries[:120])

    assert len(sources) == 3
    assert "orange" in prompts
    assert "teal" in prompts or "cyan" in prompts or "turquoise" in prompts
    assert "rainbow" in prompts
    assert "animal" in prompts
