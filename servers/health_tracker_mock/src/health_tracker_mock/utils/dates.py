from datetime import date, datetime, timedelta

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


def days_between(a: str, b: str) -> int:
    return (parse_date(b) - parse_date(a)).days


def parse_ts(s: str) -> datetime:
    """Parse an ISO-8601 timestamp, tolerating a trailing ``Z``.

    Used to validate ``recorded_at`` / ``started_at`` inputs. Raises
    ``BadDateError`` on malformed input.
    """
    if not isinstance(s, str) or not s:
        raise BadDateError(f"invalid timestamp '{s}'")
    raw = s.strip()
    candidate = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        return datetime.fromisoformat(candidate)
    except ValueError as e:
        raise BadDateError(f"invalid timestamp '{s}': {e}")


def date_of(ts: str) -> str:
    """Return the ``YYYY-MM-DD`` date portion of an ISO timestamp."""
    return ts[:10]


def now_iso_z() -> str:
    """UTC ISO timestamp in Z form. Reserved for audit fields (not used for
    issued data — all timestamps come from caller-supplied inputs)."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
