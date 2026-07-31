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


def add_months(d: str, n: int) -> str:
    """Add n calendar months, clamping to the last day if the target month is short."""
    base = parse_date(d)
    month_index = base.month - 1 + n
    year = base.year + month_index // 12
    month = month_index % 12 + 1
    # Clamp day to month's length.
    if month == 12:
        next_first = date(year + 1, 1, 1)
    else:
        next_first = date(year, month + 1, 1)
    last_day = (next_first - timedelta(days=1)).day
    return fmt(date(year, month, min(base.day, last_day)))


def days_between(a: str, b: str) -> int:
    return (parse_date(b) - parse_date(a)).days


def now_iso_z() -> str:
    """UTC ISO timestamp in Z form, used for posted_at audit fields."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def today_utc() -> str:
    """Wall-clock UTC date as YYYY-MM-DD. Used to bucket tx IDs by day."""
    return datetime.utcnow().strftime(DATE_FMT)


def at_noon_iso(date_str: str) -> str:
    """Return ``<date>T12:00:00Z`` for synthesized backdated posted_at values."""
    parse_date(date_str)  # validates
    return f"{date_str}T12:00:00Z"
