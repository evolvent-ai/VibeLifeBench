"""Minimal task-local timezone fallback for the rubric inventory process."""
from datetime import timedelta, timezone


class ZoneInfoNotFoundError(KeyError):
    pass


def ZoneInfo(key: str):
    if key == "Asia/Shanghai":
        return timezone(timedelta(hours=8))
    raise ZoneInfoNotFoundError(key)
