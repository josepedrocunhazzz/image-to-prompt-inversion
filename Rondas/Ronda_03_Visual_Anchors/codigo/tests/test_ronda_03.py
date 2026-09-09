from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_03_visual_anchors import build_round


def test_ronda_03_targets_and_counts():
    data = build_round()

    assert set(data) == {
        "1159_25.png",
        "1159_29.png",
        "1159_3.png",
        "1159_7.png",
        "7836.png",
        "9338.png",
    }
    assert len(data["1159_7.png"]) == 150
    assert len(data["9338.png"]) == 115
    assert sum(len(entries) for entries in data.values()) == 495


def test_ronda_03_plain_positive_prompts():
    data = build_round()
    blocked = [" no ", " not ", " without ", " negative prompt", "avoid"]

    for entries in data.values():
        for entry in entries:
            prompt = f" {entry['prompt'].lower()} "
            assert entry["negative_prompt"] == ""
            assert entry["source"].startswith("ronda_03_visual_anchor")
            for token in blocked:
                assert token not in prompt


def test_ronda_03_cube_anchor_keeps_cand66_direction():
    prompts = " ".join(entry["prompt"].lower() for entry in build_round()["1159_7.png"][:20])

    assert "cubical wooden block body" in prompts
    assert "4 by 4" in prompts
    assert "orange" in prompts
    assert "top plane" in prompts or "top surface" in prompts


def test_ronda_03_creature_anchor_keeps_round_orange_teal_identity():
    prompts = " ".join(entry["prompt"].lower() for entry in build_round()["9338.png"][:20])

    assert "orange" in prompts
    assert "teal" in prompts or "turquoise" in prompts
    assert "rainbow" in prompts
    assert "quill" in prompts or "bristle" in prompts
