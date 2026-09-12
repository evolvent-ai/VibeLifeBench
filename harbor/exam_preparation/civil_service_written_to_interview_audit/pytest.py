"""Minimal local ``python -m pytest`` fallback for the gate runner.

The task's contract tests use the standard-library unittest API.  The Harbor
image normally provides pytest, while the offline gate image used for local
validation does not, so this module preserves the gate command's exit-code
contract without adding a runtime dependency.
"""
from __future__ import annotations

import sys
import unittest


def main() -> int:
    paths = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    start = paths[0] if paths else "tests"
    suite = unittest.defaultTestLoader.discover(start, pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
