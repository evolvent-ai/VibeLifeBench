"""Date helpers. ISO YYYY-MM-DD strings everywhere."""
from datetime import date, datetime, timedelta

DATE_FMT = "%Y-%m-%d"


def parse_date(s: str) -> date:
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except Exception as exc:
        raise ValueError(f"invalid date '{s}': {exc}")


def add_days(d: str, n: int) -> str:
    return (parse_date(d) + timedelta(days=int(n))).strftime(DATE_FMT)


def days_between(a: str, b: str) -> int:
    """Returns integer days from a to b (b - a)."""
    return (parse_date(b) - parse_date(a)).days


def now_iso_z() -> str:
    """UTC wall-clock in Z-iso format. Used only for created_at audit trails."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def today_utc() -> str:
    """Wall-clock UTC date as YYYY-MM-DD."""
    return datetime.utcnow().strftime(DATE_FMT)
