from __future__ import annotations

import runpy
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--mode", "schedule", *sys.argv[1:]]
    runpy.run_module("vlm_refinement.run_ronda_13", run_name="__main__")
