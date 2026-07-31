"""ISO-8601 and timezone helpers."""

from datetime import datetime, timedelta, timezone, date
from typing import Optional

# Fixed-offset timezones avoid tz-db dependencies.
_TZ_TOKYO = timezone(timedelta(hours=9), name="Asia/Tokyo")
_TZ_SHANGHAI = timezone(timedelta(hours=8), name="Asia/Shanghai")


def city_tz(city: str) -> timezone:
    c = (city or "").strip().lower()
    if c == "shanghai":
        return _TZ_SHANGHAI
    return _TZ_TOKYO


def parse_iso(s: str) -> datetime:
    """Parse ISO-8601. If no offset, assume Asia/Tokyo."""
    if not s:
        raise ValueError("empty datetime")
    txt = s.strip()
    # python 3.12 tolerates trailing 'Z'
    if txt.endswith("Z"):
        txt = txt[:-1] + "+00:00"
    dt = datetime.fromisoformat(txt)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_TZ_TOKYO)
    return dt


def to_iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_TZ_TOKYO)
    return dt.isoformat(timespec="seconds")


def local_hm_to_datetime(on_date: date, hhmm: str, tz: timezone) -> datetime:
    """Combine a local date + 'HH:MM' string into a tz-aware datetime."""
    h, m = hhmm.split(":")
    return datetime(on_date.year, on_date.month, on_date.day, int(h), int(m), tzinfo=tz)


def current_sim_datetime(current_date_iso: str, at_hm: str = "09:00",
                         tz: Optional[timezone] = None) -> datetime:
    tz = tz or _TZ_TOKYO
    d = date.fromisoformat(current_date_iso)
    return local_hm_to_datetime(d, at_hm, tz)
