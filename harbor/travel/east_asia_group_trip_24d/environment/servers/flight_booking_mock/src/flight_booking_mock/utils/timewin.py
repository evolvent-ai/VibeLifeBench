"""Date/time helpers with IANA-compatible fixed offsets for our 3 airports."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

# Airport timezones (fixed offsets sufficient for the mock).
AIRPORT_TZ = {
    "PVG": timezone(timedelta(hours=8)),  # Shanghai Pudong
    "NRT": timezone(timedelta(hours=9)),  # Tokyo Narita
    "KIX": timezone(timedelta(hours=9)),  # Osaka Kansai
}


def airport_tz(iata: str) -> timezone:
    return AIRPORT_TZ.get(iata, timezone(timedelta(hours=8)))


def parse_iso(dt_str: str) -> datetime:
    """Parse an ISO-8601 timestamp possibly ending with Z."""
    if dt_str.endswith("Z"):
        dt_str = dt_str[:-1] + "+00:00"
    return datetime.fromisoformat(dt_str)


def format_iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def parse_date(date_str: str) -> datetime:
    """Parse YYYY-MM-DD as a naive date-midnight datetime."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def combine_date_time(date_str: str, hhmm: str, iata: str) -> datetime:
    """Build an aware datetime at an airport's local tz."""
    d = parse_date(date_str)
    hh, mm = hhmm.split(":")
    return d.replace(hour=int(hh), minute=int(mm), tzinfo=airport_tz(iata))


def to_utc(dt: datetime) -> datetime:
    return dt.astimezone(timezone.utc)


def add_minutes(dt_str: str, minutes: int) -> str:
    return format_iso(parse_iso(dt_str) + timedelta(minutes=minutes))


def duration_minutes(start_iso: str, end_iso: str) -> int:
    return int((parse_iso(end_iso) - parse_iso(start_iso)).total_seconds() // 60)


def is_weekend(date_str: str) -> bool:
    d = parse_date(date_str)
    return d.weekday() >= 5  # Sat/Sun


def dt_date(dt_str: str) -> str:
    """Extract YYYY-MM-DD from an ISO timestamp string (prefix only)."""
    return dt_str[:10]
