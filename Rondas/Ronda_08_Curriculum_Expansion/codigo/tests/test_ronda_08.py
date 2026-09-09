from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_08_curriculum_expansion import build_round


def test_ronda_08_targets_and_counts():
    data = build_round()

    assert set(data) == {"1159_7.png", "9338.png"}
    assert len(data["1159_7.png"]) == 241
    assert len(data["9338.png"]) == 283
    assert sum(len(entries) for entries in data.values()) == 524


def test_ronda_08_plain_positive_prompts():
    data = build_round()
    blocked = [" no ", " not ", " without ", " negative prompt", "avoid"]

    for entries in data.values():
        for entry in entries:
            prompt = f" {entry['prompt'].lower()} "
            assert entry["negative_prompt"] == ""
            assert entry["source"].startswith("ronda_08_curriculum_expansion")
            for token in blocked:
                assert token not in prompt


def test_ronda_08_dragon_hamster_curriculum_starts_simple():
    entries = build_round()["9338.png"]
    first_prompts = [entry["prompt"].lower() for entry in entries[:10]]
    sources = {entry["source"] for entry in entries}

    assert "colorful dragon hamster" in first_prompts
    assert "orange teal dragon hamster" in first_prompts
    assert any("dragon_tier5" in source for source in sources)


def test_ronda_08_cube_curriculum_starts_simple():
    entries = build_round()["1159_7.png"]
    first_prompts = [entry["prompt"].lower() for entry in entries[:8]]
    sources = {entry["source"] for entry in entries}

    assert "wooden hedgehog cube" in first_prompts
    assert "wooden cube with hedgehog face" in first_prompts
    assert any("cube_tier5" in source for source in sources)
