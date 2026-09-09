from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_12_maxstack import build_round


def test_ronda_12_targets_and_counts():
    data = build_round()

    assert set(data) == {"1159_7.png", "9338.png"}
    assert len(data["1159_7.png"]) == 420
    assert len(data["9338.png"]) == 440
    assert sum(len(entries) for entries in data.values()) == 860


def test_ronda_12_plain_positive_prompts():
    data = build_round()
    blocked = [" no ", " not ", " without ", " negative prompt", "avoid"]

    for entries in data.values():
        for entry in entries:
            prompt = f" {entry['prompt'].lower()} "
            assert entry["negative_prompt"] == ""
            assert entry["source"].startswith("ronda_12_maxstack")
            for token in blocked:
                assert token not in prompt


def test_ronda_12_cube_uses_all_strategy_terms():
    prompts = [entry["prompt"].lower() for entry in build_round()["1159_7.png"]]

    assert any("4 by 4 cube grid sides" in prompt for prompt in prompts)
    assert any("peach 4x4 grid sides" in prompt for prompt in prompts)
    assert any("sides stay visible" in prompt for prompt in prompts)
    assert any("fine orange quills" in prompt for prompt in prompts)


def test_ronda_12_dragon_uses_all_strategy_terms():
    prompts = [entry["prompt"].lower() for entry in build_round()["9338.png"]]

    assert any("colorful dragon hamster" in prompt for prompt in prompts)
    assert any("single central creature" in prompt for prompt in prompts)
    assert any("dark teal orange flame aura" in prompt for prompt in prompts)
    assert any("painted rainbow scale spines" in prompt for prompt in prompts)
