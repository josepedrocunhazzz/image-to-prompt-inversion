from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_09_targeted_corrections import build_round


def test_ronda_09_targets_and_counts():
    data = build_round()

    assert set(data) == {"1159_7.png", "9338.png"}
    assert len(data["1159_7.png"]) == 257
    assert len(data["9338.png"]) == 293
    assert sum(len(entries) for entries in data.values()) == 550


def test_ronda_09_plain_positive_prompts():
    data = build_round()
    blocked = [" no ", " not ", " without ", " negative prompt", "avoid"]

    for entries in data.values():
        for entry in entries:
            prompt = f" {entry['prompt'].lower()} "
            assert entry["negative_prompt"] == ""
            assert entry["source"].startswith("ronda_09_targeted_corrections")
            for token in blocked:
                assert token not in prompt


def test_ronda_09_cube_uses_material_reset_language():
    entries = build_round()["1159_7.png"]
    prompts = [entry["prompt"].lower() for entry in entries]

    assert prompts[0] == "pale peach foam cube hedgehog"
    assert any("4 by 4 block grid" in prompt for prompt in prompts)
    assert any("square cell" in prompt for prompt in prompts)
    assert any("hairlike quills" in prompt for prompt in prompts)


def test_ronda_09_dragon_uses_quill_creature_language():
    entries = build_round()["9338.png"]
    prompts = [entry["prompt"].lower() for entry in entries]

    assert prompts[0] == "colorful spiky hamster creature"
    assert any("teal blue belly patch" in prompt for prompt in prompts)
    assert any("short rainbow quills along the back" in prompt for prompt in prompts)
    assert any("dark teal fantasy background with yellow flame arcs" in prompt for prompt in prompts)
