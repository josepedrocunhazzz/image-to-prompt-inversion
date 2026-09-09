from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_04_final_focus import build_round


def test_ronda_04_targets_and_counts():
    data = build_round()

    assert set(data) == {"1159_7.png", "9338.png"}
    assert len(data["1159_7.png"]) == 130
    assert len(data["9338.png"]) == 110
    assert sum(len(entries) for entries in data.values()) == 240


def test_ronda_04_plain_positive_prompts():
    data = build_round()
    blocked = [" no ", " not ", " without ", " negative prompt", "avoid"]

    for entries in data.values():
        for entry in entries:
            prompt = f" {entry['prompt'].lower()} "
            assert entry["negative_prompt"] == ""
            assert entry["source"].startswith("ronda_04_final_focus")
            for token in blocked:
                assert token not in prompt


def test_ronda_04_cube_focuses_on_wooden_side_grid_and_top_quills():
    prompts = " ".join(entry["prompt"].lower() for entry in build_round()["1159_7.png"][:25])

    assert "wood" in prompts
    assert "4 by 4" in prompts
    assert "tile" in prompts or "grid" in prompts
    assert "top" in prompts
    assert "orange" in prompts


def test_ronda_04_creature_focuses_on_orange_face_teal_belly_rainbow_quills():
    prompts = " ".join(entry["prompt"].lower() for entry in build_round()["9338.png"][:25])

    assert "orange" in prompts
    assert "teal" in prompts or "turquoise" in prompts
    assert "rainbow" in prompts
    assert "quill" in prompts or "bristle" in prompts
