"""Minimal local test launcher for environments without the pytest package."""
from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path


def main() -> int:
    roots = [Path(arg) for arg in sys.argv[1:] if not arg.startswith("-")]
    roots = roots or [Path("tests")]
    files = []
    for root in roots:
        if root.is_file() and root.name.startswith("test_"):
            files.append(root)
        elif root.is_dir():
            files.extend(sorted(root.rglob("test_*.py")))
    failures = 0
    total = 0
    for path in files:
        spec = importlib.util.spec_from_file_location(f"local_test_{total}", path)
        if spec is None or spec.loader is None:
            failures += 1
            continue
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            failures += 1
            traceback.print_exc()
            continue
        for name in sorted(vars(module)):
            if not name.startswith("test_") or not callable(getattr(module, name)):
                continue
            total += 1
            try:
                getattr(module, name)()
            except Exception:
                failures += 1
                traceback.print_exc()
                if "-x" in sys.argv:
                    print(f"{total} tests collected, {failures} failed")
                    return 1
    print(f"{total} tests collected, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
