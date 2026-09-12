"""Small local fallback for environments without the pytest package."""
from __future__ import annotations

import sys
import unittest


def main() -> int:
    target = next((arg for arg in sys.argv[1:] if not arg.startswith("-")), "tests")
    suite = unittest.defaultTestLoader.discover(target, pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
