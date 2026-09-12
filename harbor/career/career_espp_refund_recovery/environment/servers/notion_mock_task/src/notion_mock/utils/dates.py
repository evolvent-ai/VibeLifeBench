"""Date / time helpers.

``last_edited_time`` / ``created_time`` are TEXT and ``API-post-search`` orders
them as strings, so writes must use the same offset form as the corpus. Every
seeded row and world-controller mutation writes ``+08:00``.

A fixed ``DEFAULT_WRITE_TIME`` was previously stamped on all writes for
determinism. It made every agent-authored page sort *behind* every seeded page
under "most recently edited first" (the seeds are 2026-02..06, the constant was
2026-01-01), so a page the agent had just created ranked last in its own
search results. Writes now carry the controller-provided world time and fail
closed when no virtual clock is configured, which keeps ordering truthful;
nothing in the rubrics or tests pins the old constant.
"""
from datetime import datetime, timedelta, timezone

from .world_clock import now as _world_now, now_iso as _world_now_iso, now_iso_z as _world_now_iso_z, today_utc as _world_today_utc

WRITE_TZ = timezone(timedelta(hours=8))

# Retained for compatibility with any caller that imported the constant; it is
# no longer what the server stamps on writes.
DEFAULT_WRITE_TIME = "2026-01-01T00:00:00+08:00"


def now_iso() -> str:
    """Current world time as an ISO 8601 string in the corpus offset (+08:00)."""
    return _world_now_iso()
