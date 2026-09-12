#!/usr/bin/env python3
"""Minimal boundary self-check hook; Harbor performs the authoritative check."""
import json
import sys


def main() -> int:
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    expected = spec.get("expected_checks") or []
    print(f"{spec['step']}: declared {len(expected)} checks for stage {spec['virtual_stage']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
