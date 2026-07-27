from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def parse_iso(s: str) -> datetime:
    """Parse an ISO-8601 string (with or without tz) into aware datetime.

    Naive strings are treated as UTC. Python 3.11+ ``datetime.fromisoformat``
    handles offsets like ``+09:00`` natively — we just tidy up a trailing ``Z``.
    """
    s2 = s.strip()
    if s2.endswith("Z"):
        s2 = s2[:-1] + "+00:00"
    dt = datetime.fromisoformat(s2)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def day_index_to_date(start_date: str, day_index: int, tz: str = "Asia/Tokyo") -> str:
    """Return YYYY-MM-DD for (start_date + day_index) in the given tz."""
    base = datetime.strptime(start_date, "%Y-%m-%d").date()
    d = base + timedelta(days=day_index)
    return d.isoformat()


def day_index_to_sim_now(
    start_date: str, day_index: int, tz: str = "Asia/Tokyo", hour: int = 9
) -> datetime:
    """Return an aware datetime representing sim-now as ``hour:00`` on that day."""
    base = datetime.strptime(start_date, "%Y-%m-%d").date()
    d = base + timedelta(days=day_index)
    return datetime(d.year, d.month, d.day, hour, 0, 0, tzinfo=ZoneInfo(tz))


def iso(dt: datetime) -> str:
    """Canonical ISO-8601 string with offset (seconds precision)."""
    return dt.replace(microsecond=0).isoformat()


def local_date_str(dt: datetime, tz: str) -> str:
    return dt.astimezone(ZoneInfo(tz)).date().isoformat()
