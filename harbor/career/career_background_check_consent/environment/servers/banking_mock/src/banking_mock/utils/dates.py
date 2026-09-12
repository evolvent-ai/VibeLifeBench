from datetime import date, datetime, timedelta

from .exceptions import BadDateError
from .world_clock import is_configured as _world_clock_configured, now as _world_now, now_iso as _world_now_iso, now_iso_z as _world_now_iso_z, today_utc as _world_today_utc

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


def add_months(d: str, n: int) -> str:
    """Add n calendar months, clamping to the last day if the target month is short."""
    base = parse_date(d)
    month_index = base.month - 1 + n
    year = base.year + month_index // 12
    month = month_index % 12 + 1
    # Clamp day to month's length.
    if month == 12:
        next_first = date(year + 1, 1, 1)
    else:
        next_first = date(year, month + 1, 1)
    last_day = (next_first - timedelta(days=1)).day
    return fmt(date(year, month, min(base.day, last_day)))


def days_between(a: str, b: str) -> int:
    return (parse_date(b) - parse_date(a)).days


def now_iso_z() -> str:
    """UTC ISO timestamp in Z form, used for posted_at audit fields."""
    return _world_now_iso_z()


def today_utc() -> str:
    """Current world date in UTC, used to bucket transaction IDs by day."""
    return _world_today_utc()


def scenario_date(conn) -> str:
    """The controller date when configured, then the seeded scenario date.

    A ledger written against the build machine's wall clock is not reproducible:
    the same run replayed a month later would otherwise stamp different dates. Seeding ``scenario_clock`` pins the books to the
    scenario, matching how this catalogue's lodging service already resolves
    "today". An unseeded standalone database falls back through the shared helper.
    """
    if _world_clock_configured():
        return _world_now().date().strftime(DATE_FMT)
    try:
        row = conn.execute(
            "SELECT scenario_date FROM scenario_clock WHERE clock_id = 'default'"
        ).fetchone()
    except Exception:
        row = None
    if row is not None:
        value = str(row["scenario_date"] if hasattr(row, "keys") else row[0])
        try:
            return parse_date(value).strftime(DATE_FMT)
        except Exception:
            pass
    return today_utc()


def scenario_now_iso(conn) -> str:
    """Scenario-aligned ``posted_at``.

    Uses the midday convention already used for synthesized postings so the
    stamp is identical on every replay; borrowing the host's time-of-day would
    reintroduce the very non-determinism the scenario clock exists to remove.
    """
    if _world_clock_configured():
        return _world_now_iso_z()
    day = scenario_date(conn)
    return now_iso_z() if day == today_utc() else at_noon_iso(day)


def at_noon_iso(date_str: str) -> str:
    """Return ``<date>T12:00:00Z`` for synthesized backdated posted_at values."""
    parse_date(date_str)  # validates
    return f"{date_str}T12:00:00Z"
