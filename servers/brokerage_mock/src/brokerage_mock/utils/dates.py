"""ISO YYYY-MM-DD date helpers."""
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
    return (parse_date(b) - parse_date(a)).days


def ytd_start(d: str) -> str:
    return f"{parse_date(d).year}-01-01"
