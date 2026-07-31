from datetime import date, datetime, timedelta
from typing import Tuple

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


def add_months(d: str, n: int) -> str:
    """Add n calendar months; clamp day-of-month to the last valid day."""
    src = parse_date(d)
    total = src.month - 1 + n
    year = src.year + total // 12
    month = total % 12 + 1
    for day in range(src.day, 0, -1):
        try:
            return date(year, month, day).strftime(DATE_FMT)
        except ValueError:
            continue
    return date(year, month, 1).strftime(DATE_FMT)


def _clamp_day(year: int, month: int, day: int) -> date:
    """Build date(year, month, day) clamping day to the last valid day."""
    for d in range(min(day, 31), 0, -1):
        try:
            return date(year, month, d)
        except ValueError:
            continue
    # Should never reach here — month always has day 1.
    return date(year, month, 1)


def cycle_window(current_date: str, cycle_start_day: int, cycle_end_day: int) -> Tuple[str, str]:
    """Return (period_start, period_end) of the cycle that contains current_date.

    Convention: a cycle runs from day `cycle_start_day` of month M (inclusive)
    to day `cycle_end_day` of month M+1 (inclusive). E.g. cycle 26-25 covers
    Apr 26 .. May 25. Day-of-month is clamped to the last valid day so a
    `cycle_end_day = 31` works in February.
    """
    d = parse_date(current_date)
    if d.day >= cycle_start_day:
        period_start = _clamp_day(d.year, d.month, cycle_start_day)
        end_month = d.month + 1
        end_year = d.year + (1 if end_month > 12 else 0)
        end_month = end_month if end_month <= 12 else end_month - 12
        period_end = _clamp_day(end_year, end_month, cycle_end_day)
    else:
        start_month = d.month - 1
        start_year = d.year - (1 if start_month < 1 else 0)
        start_month = start_month if start_month >= 1 else start_month + 12
        period_start = _clamp_day(start_year, start_month, cycle_start_day)
        period_end = _clamp_day(d.year, d.month, cycle_end_day)
    return period_start.strftime(DATE_FMT), period_end.strftime(DATE_FMT)


def now_iso_z() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def today_utc() -> str:
    """Wall-clock UTC date as YYYY-MM-DD. Used to bucket payment/dispute IDs by day."""
    return datetime.utcnow().strftime(DATE_FMT)
