from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gerar_ronda_01_clip_guided import append_part, build_prompt_specs


def test_ronda_01_specs_targets_and_limits():
    specs = build_prompt_specs()

    assert set(specs) == {
        "1159_25.png",
        "1159_29.png",
        "1159_3.png",
        "1159_7.png",
        "7836.png",
        "9338.png",
    }
    assert sum(spec.limit for spec in specs.values()) == 400
    assert specs["1159_7.png"].limit == 90
    assert specs["9338.png"].limit == 90


def test_ronda_01_specs_are_discrete_prompt_components():
    for spec in build_prompt_specs().values():
        assert spec.anchors
        assert spec.stages
        assert spec.limit > 0
        for prompt in spec.anchors:
            assert isinstance(prompt, str)
            assert prompt.strip()
            assert " no " not in f" {prompt.lower()} "
            assert " not " not in f" {prompt.lower()} "
        for stage in spec.stages:
            assert stage
            for part in stage:
                assert isinstance(part, str)
                assert part.strip()


def test_append_part_keeps_plain_text_prompt():
    assert append_part("", "a") == "a"
    assert append_part("a", "") == "a"
    assert append_part("a", "b") == "a, b"
