"""Date helpers. ISO YYYY-MM-DD strings everywhere."""
from datetime import date, datetime, timedelta
import os

from .world_clock import is_configured as _world_clock_configured, now as _world_now, now_iso as _world_now_iso, now_iso_z as _world_now_iso_z, today_utc as _world_today_utc
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
    """Current world time in UTC Z form for created_at audit trails."""
    return _world_now_iso_z()


def today_utc() -> str:
    """Current world date in UTC as YYYY-MM-DD."""
    return _world_today_utc()


def scenario_date_or_today() -> str:
    """Controller date, then legacy scenario date, then standalone fallback."""
    if _world_clock_configured():
        return _world_now().date().isoformat()
    configured = os.environ.get("ECOMMERCE_SCENARIO_DATE")
    if configured:
        return parse_date(configured).strftime(DATE_FMT)
    return today_utc()
