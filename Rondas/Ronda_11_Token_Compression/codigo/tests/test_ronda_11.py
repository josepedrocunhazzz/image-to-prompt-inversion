from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_11_token_compression import build_round


def test_ronda_11_targets_and_counts():
    data = build_round()

    assert set(data) == {"1159_7.png", "9338.png"}
    assert len(data["1159_7.png"]) == 260
    assert len(data["9338.png"]) == 280
    assert sum(len(entries) for entries in data.values()) == 540


def test_ronda_11_plain_positive_short_prompts():
    data = build_round()
    blocked = [" no ", " not ", " without ", " negative prompt", "avoid"]

    for entries in data.values():
        for entry in entries:
            prompt = f" {entry['prompt'].lower()} "
            assert entry["negative_prompt"] == ""
            assert entry["source"].startswith("ronda_11_token_compression")
            assert len(entry["prompt"].split()) <= 36
            for token in blocked:
                assert token not in prompt


def test_ronda_11_cube_core_terms_first():
    prompts = [entry["prompt"].lower() for entry in build_round()["1159_7.png"]]

    assert prompts[0].startswith("cube hedgehog")
    assert any("4x4 grid sides" in prompt for prompt in prompts)
    assert any("tiny hidden face" in prompt for prompt in prompts)
    assert any("orange top quills" in prompt for prompt in prompts)


def test_ronda_11_dragon_core_terms_first():
    prompts = [entry["prompt"].lower() for entry in build_round()["9338.png"]]

    assert prompts[0].startswith("dragon hamster")
    assert any("orange face" in prompt for prompt in prompts)
    assert any("teal belly" in prompt for prompt in prompts)
    assert any("rainbow quills" in prompt for prompt in prompts)
