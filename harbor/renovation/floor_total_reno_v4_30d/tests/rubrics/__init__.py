"""Flooring renovation rubric package."""
import sys
from pathlib import Path

_here = Path(__file__).resolve()
# The delivered tree is mounted shallow (the verifier runs /tests/run_verifier.py),
# so the historical repo-root ancestor five levels up may not exist; indexing it
# unconditionally raised IndexError inside the package import and failed every
# rubric bucket. The tests/ directory itself is what the rubrics import from
# (harbor_evidence); guarantee it, and keep the deep repo root best-effort.
_tests_dir = str(_here.parents[1])
if _tests_dir not in sys.path:
    sys.path.insert(0, _tests_dir)
if len(_here.parents) > 5 and str(_here.parents[5]) not in sys.path:
    sys.path.insert(0, str(_here.parents[5]))
