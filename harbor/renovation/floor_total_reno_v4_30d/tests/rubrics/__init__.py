"""Flooring renovation rubric package."""
import sys
from pathlib import Path

_REPO_ROOT = str(Path(__file__).resolve().parents[5])
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)
