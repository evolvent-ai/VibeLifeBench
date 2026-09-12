from datetime import datetime, timedelta, timezone

from .world_clock import now as _world_now, now_iso as _world_now_iso, now_iso_z as _world_now_iso_z, today_utc as _world_today_utc
# ``messages.date`` is TEXT and every listing sorts it as a string, so a single
# stored offset form is required for that sort to agree with real time. All seed
# rows and every world-controller mutation write +08:00; emitting Z here would
# order server-written mail against the seed purely on the offset character
# ('+' 0x2B < digits < 'Z' 0x5A), so a newly sent message sorted below older
# seeded mail under "newest first".
WRITE_TZ = timezone(timedelta(hours=8))


def now_iso_z() -> str:
    """Current time as an ISO 8601 string in the corpus offset (+08:00).

    Named for the historical Z form it replaced; the name is kept so the
    existing call sites stay untouched.
    """
    return _world_now_iso()
