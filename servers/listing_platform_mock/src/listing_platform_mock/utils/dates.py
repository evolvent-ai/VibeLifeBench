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


def days_between(a: str, b: str) -> int:
    return (parse_date(b) - parse_date(a)).days


def parse_datetime(s: str) -> datetime:
    """Validate an ISO-8601 datetime string (with or without timezone).

    Accepts the trailing ``Z`` (UTC) shorthand. Raises ``BadDateError`` on
    malformed input. Returns the parsed datetime (callers usually just need
    the validation side-effect).
    """
    if not isinstance(s, str) or not s:
        raise BadDateError(f"invalid datetime '{s}'")
    candidate = s.replace("Z", "+00:00") if s.endswith("Z") else s
    try:
        return datetime.fromisoformat(candidate)
    except ValueError as e:
        raise BadDateError(f"invalid datetime '{s}': {e}")
