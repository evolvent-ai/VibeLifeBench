from datetime import date, datetime, timedelta, timezone

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


def days_between(a: str, b: str) -> int:
    return (parse_date(b) - parse_date(a)).days


# Datetime columns are TEXT and orderings compare them as strings, so a single
# stored offset form is required for those comparisons to agree with real time.
# All seed rows and every world-controller mutation write +08:00; emitting Z
# here would sort server-written rows against the seed purely on the offset
# character ('+' 0x2B < digits < 'Z' 0x5A) rather than on the instant.
WRITE_TZ = timezone(timedelta(hours=8))


def now_iso_z() -> str:
    """Current time as an ISO 8601 string in the corpus offset (+08:00).

    Named for the historical Z form it replaced; the name is kept so the
    existing call sites stay untouched.
    """
    return _world_now_iso()


def today_utc() -> str:
    """Today's date (corpus offset) as YYYY-MM-DD.

    Uses the same offset as the stored timestamps so a date derived here cannot
    disagree with the date embedded in a same-moment timestamp.
    """
    return _world_now().strftime(DATE_FMT)
