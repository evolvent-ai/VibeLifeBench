"""Date helpers — ISO YYYY-MM-DD only."""
from datetime import date, datetime, timedelta

from .world_clock import now as _world_now, now_iso as _world_now_iso, now_iso_z as _world_now_iso_z, today_utc as _world_today_utc
DATE_FMT = "%Y-%m-%d"


def parse_date(s: str) -> date:
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except Exception as e:
        raise ValueError(f"invalid date '{s}': {e}")


def add_days(d: str, n: int) -> str:
    return (parse_date(d) + timedelta(days=n)).strftime(DATE_FMT)


def days_between(a: str, b: str) -> int:
    """Returns integer days from a to b (b - a)."""
    return (parse_date(b) - parse_date(a)).days


def now_iso_z() -> str:
    """Current world time in UTC Z form (audit trail only)."""
    return _world_now_iso_z()


def iso_at(date_str: str, hour: int = 9, minute: int = 0) -> str:
    """Compose an ISO timestamp at a given hour/minute on a date (no tz)."""
    return f"{date_str}T{hour:02d}:{minute:02d}:00"
