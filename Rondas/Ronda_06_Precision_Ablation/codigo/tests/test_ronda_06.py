from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_06_precision_ablation import build_round


def test_ronda_06_targets_and_counts():
    data = build_round()

    assert set(data) == {"1159_7.png", "9338.png"}
    assert len(data["1159_7.png"]) == 160
    assert len(data["9338.png"]) == 120
    assert sum(len(entries) for entries in data.values()) == 280


def test_ronda_06_plain_positive_prompts():
    data = build_round()
    blocked = [" no ", " not ", " without ", " negative prompt", "avoid"]

    for entries in data.values():
        for entry in entries:
            prompt = f" {entry['prompt'].lower()} "
            assert entry["negative_prompt"] == ""
            assert entry["source"].startswith("ronda_06_precision_ablation")
            for token in blocked:
                assert token not in prompt


def test_ronda_06_cube_ablation_keeps_best_ronda_03_identity():
    prompts = " ".join(entry["prompt"].lower() for entry in build_round()["1159_7.png"][:30])

    assert "4 by 4" in prompts
    assert "hidden" in prompts or "buried" in prompts
    assert "orange" in prompts
    assert "top" in prompts
    assert "wood" in prompts


def test_ronda_06_creature_ablation_keeps_ronda_05_silhouette_but_softens_subject():
    prompts = " ".join(entry["prompt"].lower() for entry in build_round()["9338.png"][:30])

    assert "upright" in prompts
    assert "orange" in prompts
    assert "teal" in prompts or "cyan" in prompts or "turquoise" in prompts
    assert "rainbow" in prompts
    assert "animal" in prompts or "creature" in prompts
