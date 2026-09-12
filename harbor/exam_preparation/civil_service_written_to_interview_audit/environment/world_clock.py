"""Fail-closed reader for the Harbor world clock.

The controller is the sole writer. Mock services and local checks must never
silently substitute host time when the file is absent or malformed.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


class WorldClockError(RuntimeError):
    """The configured clock is missing, malformed, or lacks a timezone."""


def now() -> datetime:
    path = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
    try:
        payload: Any = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WorldClockError(f"cannot read world clock: {path}") from exc
    if not isinstance(payload, dict) or set(payload) != {"world_now"}:
        raise WorldClockError("world clock must contain exactly the world_now key")
    raw = payload.get("world_now")
    if not isinstance(raw, str) or not raw.strip():
        raise WorldClockError("world_now must be a non-empty ISO timestamp")
    try:
        value = datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise WorldClockError("world_now is not a valid ISO timestamp") from exc
    if value.tzinfo is None or value.utcoffset() is None:
        raise WorldClockError("world_now must include an explicit timezone offset")
    return value


def now_iso() -> str:
    return now().isoformat()
