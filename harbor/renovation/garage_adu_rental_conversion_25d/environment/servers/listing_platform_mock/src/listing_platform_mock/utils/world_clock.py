"""Shared virtual world-clock contract for mock server audit timestamps.

The Harbor world-controller owns ``WORLD_CLOCK_FILE`` and updates it at step
boundaries. ``WORLD_NOW`` is intentionally a secondary static override for
unit tests and local debugging. When neither is configured, reads fail closed.
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

WRITE_TZ = timezone(timedelta(hours=8))
WORLD_CLOCK_FILE_ENV = "WORLD_CLOCK_FILE"
WORLD_NOW_ENV = "WORLD_NOW"


class WorldClockError(RuntimeError):
    """Raised when a configured virtual clock cannot be read safely."""


def _parse_timestamp(raw: Any, source: str) -> datetime:
    if not isinstance(raw, str) or not raw.strip():
        raise WorldClockError(f"{source} must contain a non-empty ISO timestamp")
    try:
        parsed = datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise WorldClockError(f"{source} is not a valid ISO timestamp: {raw!r}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise WorldClockError(f"{source} must include an explicit timezone offset")
    return parsed.astimezone(WRITE_TZ).replace(microsecond=0)


def _read_clock_file(path: Path) -> datetime:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorldClockError(f"configured world clock file is missing: {path}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WorldClockError(f"configured world clock file is unreadable: {path}: {exc}") from exc
    if not isinstance(payload, dict) or not payload.get("world_now"):
        raise WorldClockError(f"configured world clock file must contain a JSON object: {path}")
    return _parse_timestamp(payload.get("world_now"), f"world_now in {path}")


def is_configured() -> bool:
    """Whether Harbor or a caller supplied a virtual clock source."""
    return bool(os.environ.get(WORLD_CLOCK_FILE_ENV) or os.environ.get(WORLD_NOW_ENV))


def now() -> datetime:
    """Return the current world time as an aware datetime in ``+08:00``."""
    clock_file = os.environ.get(WORLD_CLOCK_FILE_ENV)
    if clock_file:
        return _read_clock_file(Path(clock_file))

    static_now = os.environ.get(WORLD_NOW_ENV)
    if static_now:
        return _parse_timestamp(static_now, WORLD_NOW_ENV)

    raise WorldClockError(
        "world clock not configured: set WORLD_CLOCK_FILE (world-controller) "
        "or WORLD_NOW (tests); refusing to fall back to host wall clock")


def now_iso() -> str:
    """Return the current world time in the corpus offset form."""
    return now().isoformat()


def now_iso_z() -> str:
    """Return the current world time as a UTC ``Z`` timestamp."""
    return now().astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today_utc() -> str:
    """Return the current world date in UTC as ``YYYY-MM-DD``."""
    return now().astimezone(timezone.utc).date().isoformat()


def today_local() -> date:
    """Return the current world date in the corpus offset."""
    return now().date()
