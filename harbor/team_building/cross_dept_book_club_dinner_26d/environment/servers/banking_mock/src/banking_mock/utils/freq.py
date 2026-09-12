"""Frequency math for recurring payments."""
from .dates import add_days, add_months
from .exceptions import BadFreqError

VALID_FREQ = ("daily", "weekly", "monthly")


def validate_freq(freq: str) -> str:
    if freq not in VALID_FREQ:
        raise BadFreqError(f"freq must be one of {VALID_FREQ}; got '{freq}'")
    return freq


def advance(date_str: str, freq: str) -> str:
    """Return the next occurrence date after ``date_str`` for the given freq."""
    if freq == "daily":
        return add_days(date_str, 1)
    if freq == "weekly":
        return add_days(date_str, 7)
    if freq == "monthly":
        return add_months(date_str, 1)
    raise BadFreqError(f"unsupported freq '{freq}'")
