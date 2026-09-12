"""Date / datetime parsing helpers.

Event start / end times are ISO 8601 datetimes (``YYYY-MM-DDTHH:MM:SS``
with optional ``Z`` or ``±HH:MM`` offset). Stored as text and compared
lexicographically thanks to the ISO ordering property.
"""
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from .exceptions import BadDateError
from .world_clock import now as _world_now, now_iso as _world_now_iso, now_iso_z as _world_now_iso_z, today_utc as _world_today_utc

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


# Datetime columns are TEXT and every ordering/range filter compares them as
# strings, so a single stored offset form is required for those comparisons to
# agree with real time. All seed data and every world-controller mutation write
# +08:00; emitting Z here would sort every server-written row against the seed
# purely on the offset character ('+' 0x2B < digits < 'Z' 0x5A) rather than on
# the instant, silently inverting "newest first" and window filters.
WRITE_TZ = timezone(timedelta(hours=8))


def now_iso_z() -> str:
    """Current time as an ISO 8601 string in the corpus offset (+08:00).

    Named for the historical Z form it replaced; the name is kept so the
    existing call sites stay untouched.
    """
    return _world_now_iso()


def to_storage_offset(s: str) -> str:
    """Rewrite an ISO datetime into the stored offset, preserving the instant.

    Window filters compare against TEXT columns, so the comparison is a byte
    comparison: the same instant written ``...T16:00:00Z`` and
    ``...T00:00:00+08:00`` compares differently even though both are legal
    inputs per SPEC.md ("ISO 8601 with an offset is the input/output form").
    Normalising the caller's bound to the offset the rows are stored in makes
    the string comparison agree with chronological order.

    A naive datetime carries no instant to convert, so it is passed through and
    compared as written.
    """
    dt = parse_datetime(s)
    if dt.tzinfo is None:
        return s
    return dt.astimezone(WRITE_TZ).isoformat(timespec="seconds")


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
