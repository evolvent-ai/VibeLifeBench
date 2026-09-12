#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def main() -> int:
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(f"{spec['step']}: deferred to Harbor verifier (stage {spec['virtual_stage']})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
