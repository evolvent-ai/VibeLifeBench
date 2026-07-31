from datetime import date, datetime, timedelta

from .exceptions import BadDateError

DATE_FMT = "%Y-%m-%d"


def parse_date(s: str) -> date:
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except (TypeError, ValueError) as e:
        raise BadDateError(f"invalid date '{s}': {e}")


def parse_datetime(s: str) -> datetime:
    """Parse an ISO datetime. Accepts ``YYYY-MM-DDTHH:MM[:SS]`` with optional Z."""
    if not isinstance(s, str) or not s:
        raise BadDateError(f"invalid datetime '{s}'")
    raw = s.strip()
    if raw.endswith("Z"):
        raw = raw[:-1]
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    raise BadDateError(f"invalid datetime '{s}': expected ISO YYYY-MM-DDTHH:MM[:SS]")


def fmt(d: date) -> str:
    return d.strftime(DATE_FMT)


def add_days(d: str, n: int) -> str:
    return fmt(parse_date(d) + timedelta(days=n))


def now_iso_z() -> str:
    """UTC ISO timestamp in Z form, used for created_at audit fields."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def today_utc() -> str:
    """Wall-clock UTC date as YYYY-MM-DD."""
    return datetime.utcnow().strftime(DATE_FMT)
