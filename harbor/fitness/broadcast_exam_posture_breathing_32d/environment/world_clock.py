"""Fail-closed reader for the task's isolated world clock."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path


def read_world_now() -> datetime:
    path = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
    payload = json.loads(path.read_text(encoding="utf-8"))
    if set(payload) != {"world_now"}:
        raise ValueError("world clock must contain exactly world_now")
    value = payload["world_now"]
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("world clock must include a timezone offset")
    return parsed
