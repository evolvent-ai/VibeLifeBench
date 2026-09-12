"""Small local fallback for the gate's standard pytest invocation.

The delivery tests use unittest APIs.  This entry point keeps the task
self-contained in verifier images that do not ship the optional pytest package.
"""
from __future__ import annotations

import sys
import unittest


def main() -> int:
    start_dir = "tests"
    for arg in sys.argv[1:]:
        if not arg.startswith("-") and arg != "no:cacheprovider":
            start_dir = arg
            break
    suite = unittest.defaultTestLoader.discover(start_dir, pattern="test_*.py")
    quiet = "-q" in sys.argv[1:]
    result = unittest.TextTestRunner(verbosity=1 if quiet else 2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
