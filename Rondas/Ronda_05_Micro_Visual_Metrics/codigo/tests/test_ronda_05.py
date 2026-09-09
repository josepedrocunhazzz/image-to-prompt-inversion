from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_05_micro_visual_metrics import build_round


def test_ronda_05_targets_and_counts():
    data = build_round()

    assert set(data) == {"1159_7.png", "9338.png"}
    assert len(data["1159_7.png"]) == 72
    assert len(data["9338.png"]) == 72
    assert sum(len(entries) for entries in data.values()) == 144


def test_ronda_05_plain_positive_prompts():
    data = build_round()
    blocked = [" no ", " not ", " without ", " negative prompt", "avoid"]

    for entries in data.values():
        for entry in entries:
            prompt = f" {entry['prompt'].lower()} "
            assert entry["negative_prompt"] == ""
            assert entry["source"].startswith("ronda_05_visual_metric_micro")
            for token in blocked:
                assert token not in prompt


def test_ronda_05_cube_micro_keeps_face_grid_and_top_spines():
    prompts = " ".join(entry["prompt"].lower() for entry in build_round()["1159_7.png"][:20])

    assert "4 by 4" in prompts
    assert "face" in prompts
    assert "top" in prompts
    assert "orange" in prompts
    assert "wood" in prompts


def test_ronda_05_creature_micro_keeps_target_colours_and_quills():
    prompts = " ".join(entry["prompt"].lower() for entry in build_round()["9338.png"][:20])

    assert "orange" in prompts
    assert "teal" in prompts or "turquoise" in prompts
    assert "rainbow" in prompts
    assert "quill" in prompts or "bristle" in prompts
    assert "claw" in prompts
