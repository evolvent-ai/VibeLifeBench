"""Fail-closed reader for the Harbor world clock."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

WORLD_CLOCK_FILE = "WORLD_CLOCK_FILE"


def now() -> datetime:
    path = os.environ.get(WORLD_CLOCK_FILE)
    if not path:
        raise RuntimeError(f"{WORLD_CLOCK_FILE} is required")
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot read world clock: {path}") from exc
    if set(payload) != {"world_now"}:
        raise RuntimeError("world clock must contain exactly {world_now}")
    value = payload["world_now"]
    if not isinstance(value, str):
        raise RuntimeError("world_now must be an ISO string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise RuntimeError("world_now must include a timezone")
    return parsed
