from datetime import date, datetime, timedelta

from .exceptions import BadArgError
from .world_clock import now as _world_now, now_iso as _world_now_iso, now_iso_z as _world_now_iso_z, today_utc as _world_today_utc

DATE_FMT = "%Y-%m-%d"


def parse_date(s: str) -> date:
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except (TypeError, ValueError) as e:
        raise BadArgError(f"invalid date '{s}': {e}", code="BAD_DATE")


def fmt(d: date) -> str:
    return d.strftime(DATE_FMT)


def add_days(d: str, n: int) -> str:
    return fmt(parse_date(d) + timedelta(days=n))


def days_between(a: str, b: str) -> int:
    return (parse_date(b) - parse_date(a)).days


def now_iso_z() -> str:
    """UTC ISO timestamp in Z form, used for created_at audit fields."""
    return _world_now_iso_z()


def today_utc() -> str:
    """Current world date in UTC as YYYY-MM-DD."""
    return _world_today_utc()
