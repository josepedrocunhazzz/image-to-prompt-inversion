from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_10_hybrid_multiseed import build_round


def test_ronda_10_targets_and_counts():
    data = build_round()

    assert set(data) == {"1159_7.png", "9338.png"}
    assert len(data["1159_7.png"]) == 340
    assert len(data["9338.png"]) == 360
    assert sum(len(entries) for entries in data.values()) == 700


def test_ronda_10_plain_positive_prompts():
    data = build_round()
    blocked = [" no ", " not ", " without ", " negative prompt", "avoid"]

    for entries in data.values():
        for entry in entries:
            prompt = f" {entry['prompt'].lower()} "
            assert entry["negative_prompt"] == ""
            assert entry["source"].startswith("ronda_10_hybrid_repair")
            for token in blocked:
                assert token not in prompt


def test_ronda_10_cube_contains_hybrid_repair_terms():
    prompts = [entry["prompt"].lower() for entry in build_round()["1159_7.png"]]

    assert any("4 by 4 cube grid sides" in prompt for prompt in prompts)
    assert any("front and right sides built from small square cells" in prompt for prompt in prompts)
    assert any("tiny nose barely visible below orange quills" in prompt for prompt in prompts)
    assert any("top fur compact" in prompt for prompt in prompts)


def test_ronda_10_dragon_contains_hybrid_repair_terms():
    prompts = [entry["prompt"].lower() for entry in build_round()["9338.png"]]

    assert any("colorful dragon hamster" in prompt for prompt in prompts)
    assert any("orange teal spiky hamster creature" in prompt for prompt in prompts)
    assert any("side profile creature portrait" in prompt for prompt in prompts)
    assert any("dark teal fantasy background with yellow flame arcs" in prompt for prompt in prompts)
