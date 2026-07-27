"""Date helpers — ISO YYYY-MM-DD only."""
from datetime import date, datetime, timedelta

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
    """Current real-world UTC in Z-iso format (audit trail only)."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def iso_at(date_str: str, hour: int = 9, minute: int = 0) -> str:
    """Compose an ISO timestamp at a given hour/minute on a date (no tz)."""
    return f"{date_str}T{hour:02d}:{minute:02d}:00"
