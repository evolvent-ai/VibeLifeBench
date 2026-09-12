"""Fail-closed reader for the Harbor world clock."""
from __future__ import annotations
import json, os
from datetime import datetime, timezone, timedelta
from pathlib import Path

EXPECTED = "/world-clock/current.json"
class WorldClockError(RuntimeError): pass

def read_clock(expected_step=None):
    if os.environ.get("WORLD_CLOCK_FILE") != EXPECTED:
        raise WorldClockError("WORLD_CLOCK_FILE must be exactly /world-clock/current.json")
    try:
        payload = json.loads(Path(EXPECTED).read_text(encoding="utf-8"))
    except Exception as exc:
        raise WorldClockError(f"unreadable world clock: {exc}") from exc
    if not isinstance(payload, dict) or set(payload) != {"world_now"} or not isinstance(payload.get("world_now"), str):
        raise WorldClockError("clock must contain exactly world_now")
    try:
        dt = datetime.fromisoformat(payload["world_now"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise WorldClockError("world_now must be ISO timestamp") from exc
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise WorldClockError("world_now must include timezone")
    return {"world_now": payload["world_now"]}

def now():
    return datetime.fromisoformat(read_clock()["world_now"].replace("Z", "+00:00")).astimezone(timezone(timedelta(hours=8)))
