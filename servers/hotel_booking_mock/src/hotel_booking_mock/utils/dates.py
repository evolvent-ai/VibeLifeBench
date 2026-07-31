import sqlite3
from datetime import date, datetime, timedelta, timezone
from typing import Iterator, List

DATE_FMT = "%Y-%m-%d"


def parse_date(s: str) -> date:
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except Exception as e:
        raise ValueError(f"invalid date '{s}': {e}")


def iter_nights(check_in: str, check_out: str) -> List[str]:
    """Return the list of night-dates for a stay (check-in inclusive, check-out exclusive)."""
    ci = parse_date(check_in)
    co = parse_date(check_out)
    if co <= ci:
        raise ValueError("check_out must be after check_in")
    nights: List[str] = []
    cur = ci
    while cur < co:
        nights.append(cur.strftime(DATE_FMT))
        cur += timedelta(days=1)
    return nights


def is_weekend(d: str) -> bool:
    """Friday or Saturday counts as 'weekend' for pricing (JST convention)."""
    dt = parse_date(d)
    # Monday=0 ... Friday=4, Saturday=5
    return dt.weekday() in (4, 5)


def add_days(d: str, n: int) -> str:
    return (parse_date(d) + timedelta(days=n)).strftime(DATE_FMT)


def days_between(a: str, b: str) -> int:
    """Returns integer days from a to b (b-a)."""
    return (parse_date(b) - parse_date(a)).days


def compact(d: str) -> str:
    return d.replace("-", "")


def from_compact(s: str) -> str:
    if len(s) != 8 or not s.isdigit():
        raise ValueError(f"invalid compact date: {s}")
    return f"{s[:4]}-{s[4:6]}-{s[6:]}"


def jst_iso_end_of_day_minus_one(date_str: str, hour: int = 18) -> str:
    """Return e.g. 2026-04-30T18:00:00+09:00 for reservation refund cutoff."""
    d = parse_date(date_str)
    return f"{d.strftime(DATE_FMT)}T{hour:02d}:00:00+09:00"


def current_date_iso(conn: sqlite3.Connection) -> str:
    """Return the scenario date when seeded, otherwise the host UTC date."""
    try:
        row = conn.execute(
            "SELECT scenario_date FROM scenario_clock WHERE clock_id = 'default'"
        ).fetchone()
    except sqlite3.Error:
        row = None
    if row is not None:
        value = str(row["scenario_date"] if hasattr(row, "keys") else row[0])
        try:
            return date.fromisoformat(value).isoformat()
        except ValueError:
            pass
    return datetime.now(timezone.utc).date().isoformat()
