#!/usr/bin/env python3
import json
import sys
from pathlib import Path

spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(f"{spec['step']}: self-check deferred to Harbor verifier")
