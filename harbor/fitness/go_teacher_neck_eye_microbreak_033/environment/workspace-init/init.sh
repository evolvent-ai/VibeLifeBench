#!/bin/sh
set -eu
mkdir -p /target
cp -a /workspace-seed/. /target/
chmod -R a+rwX /target
mkdir -p /scenario-clock
python - <<'PY'
import json
import os
from pathlib import Path

step_map = json.loads(Path("/step-release-map.json").read_text(encoding="utf-8"))
initial = step_map["steps"]["event-000"]
payload = {
    "now": initial["scenario_time"],
    "step": "event-000",
    "timezone": "Asia/Shanghai",
}
target = Path("/scenario-clock/current.json")
temporary = target.with_suffix(".tmp")
temporary.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
os.replace(temporary, target)
PY
