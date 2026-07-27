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


def now_iso_z() -> str:
    """UTC ISO timestamp in Z form, used for created_at/updated_at audit fields."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def today_utc() -> str:
    """Wall-clock UTC date as YYYY-MM-DD."""
    return datetime.utcnow().strftime(DATE_FMT)
