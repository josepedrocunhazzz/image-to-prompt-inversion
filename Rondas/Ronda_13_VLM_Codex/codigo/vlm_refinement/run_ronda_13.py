from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tp2_common import DEFAULT_OUTPUT_DIR
from run_vlm_refinement_ronda_13 import main
from vlm_refinement.tools.friendly_view import make_friendly_view


DEFAULT_TARGETS = [
    "1159_25.png",
    "1159_29.png",
    "1159_3.png",
    "1159_7.png",
    "7836.png",
    "9338.png",
]


def parse_mode(argv: list[str]) -> tuple[str, list[str]]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--mode",
        choices=["interactive", "file", "schedule"],
        default="interactive",
        help="interactive waits for JSON on stdin; file waits for codex_response.json; schedule uses the bundled prompt plan.",
    )
    known, remaining = parser.parse_known_args(argv[1:])
    return known.mode, [argv[0], *remaining]


def inject_defaults(argv: list[str], mode: str) -> list[str]:
    provider = {
        "interactive": "stdin",
        "file": "file",
        "schedule": "schedule",
    }[mode]
    defaults = [
        "--vlm-provider",
        provider,
        "--output-dir",
        str(DEFAULT_OUTPUT_DIR / "vlm_refinement" / "runs"),
        "--source-output-dir",
        str(DEFAULT_OUTPUT_DIR),
        "--identity",
        f"ronda_13_codex_{mode}",
        "--top-anchors",
        "1",
        "--iterations",
        "20",
        "--variants-per-call",
        "1",
        "--disable-progress-bar",
        "--maxstack-scoring",
        "--only",
        *DEFAULT_TARGETS,
    ]
    return [argv[0], *defaults, *argv[1:]]


if __name__ == "__main__":
    mode, remaining_argv = parse_mode(sys.argv)
    sys.argv = inject_defaults(remaining_argv, mode)
    run_dir = main()
    review_dir = make_friendly_view(run_dir)
    print(f"Clean review folder: {review_dir}")
