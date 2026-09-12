"""Provide a deterministic UTC+8 fallback when the host has no tzdata files."""
from datetime import timedelta, timezone
import zoneinfo

_zoneinfo = zoneinfo.ZoneInfo


def ZoneInfo(key: str):
    try:
        return _zoneinfo(key)
    except zoneinfo.ZoneInfoNotFoundError:
        if key == "Asia/Shanghai":
            return timezone(timedelta(hours=8))
        raise


zoneinfo.ZoneInfo = ZoneInfo
