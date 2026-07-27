"""Date / datetime parsing helpers.

Event start / end times are ISO 8601 datetimes (``YYYY-MM-DDTHH:MM:SS``
with optional ``Z`` or ``±HH:MM`` offset). Stored as text and compared
lexicographically thanks to the ISO ordering property.
"""
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from .exceptions import BadDateError

DATE_FMT = "%Y-%m-%d"


def parse_date(s: str) -> date:
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except (TypeError, ValueError) as e:
        raise BadDateError(f"invalid date '{s}': {e}")


def fmt(d: date) -> str:
    return d.strftime(DATE_FMT)


def add_days(d: str, n: int) -> str:
    return fmt(parse_date(d) + timedelta(days=n))


def parse_datetime(s: str) -> datetime:
    """Parse an ISO 8601 datetime. Accepts trailing ``Z`` (treated as UTC)
    and ``±HH:MM`` offsets. Naive datetimes are returned as-is."""
    if not isinstance(s, str) or not s:
        raise BadDateError(f"invalid datetime: {s!r}")
    txt = s.strip()
    if txt.endswith("Z"):
        txt = txt[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(txt)
    except ValueError as e:
        raise BadDateError(f"invalid datetime '{s}': {e}")


def datetime_to_iso(dt: datetime) -> str:
    """Format ``dt`` as ISO 8601. Aware datetimes use ``+HH:MM``; naive
    datetimes are written without an offset (caller's responsibility)."""
    return dt.isoformat(timespec="seconds")


def now_iso_z() -> str:
    """UTC ISO timestamp in Z form, used for created_at/updated_at audit fields."""
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def date_of(dt_str: str) -> str:
    """Return the YYYY-MM-DD portion of an ISO datetime string."""
    # The first 10 chars of any valid ISO 8601 form are the date.
    parse_datetime(dt_str)  # validates
    return dt_str[:10]


def assert_time_range(start: str, end: str) -> None:
    """Raise BadTimeRangeError if ``end`` is not strictly after ``start``."""
    from .exceptions import BadTimeRangeError
    s = parse_datetime(start)
    e = parse_datetime(end)
    # Both aware or both naive — normalise to comparable form.
    if (s.tzinfo is None) != (e.tzinfo is None):
        # Treat naive as UTC for the comparison only.
        if s.tzinfo is None:
            s = s.replace(tzinfo=timezone.utc)
        if e.tzinfo is None:
            e = e.replace(tzinfo=timezone.utc)
    if e <= s:
        raise BadTimeRangeError(
            f"end ({end}) must be strictly after start ({start})"
        )


def opt_parse_datetime(s: Optional[str]) -> Optional[datetime]:
    return parse_datetime(s) if s else None
