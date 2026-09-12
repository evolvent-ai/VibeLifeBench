"""Stage 12: resync each application after the status mutation."""
from __future__ import annotations

from ._helpers import applications_by_status, derived_text, stage_write_used, used_tool

_STATUS_WORDS = {
    "viewed": ("viewed", "viewing", "seen"),
    "interview": ("interview", "in interview", "advanced to interview", "interview scheduled"),
    "rejected": ("rejected", "not passed", "declined", "refused"),
}


def _bound_status(corpus: str, row: dict, status: str) -> bool:
    ids = [str(row.get(key) or "").lower() for key in ("application_id", "job_id") if row.get(key)]
    low = corpus.lower()
    for identifier in ids:
        start = 0
        while True:
            index = low.find(identifier, start)
            if index < 0:
                break
            window = low[max(0, index - 120):index + len(identifier) + 120]
            if any(word in window for word in _STATUS_WORDS[status]):
                return True
            start = index + 1
    return False


def s12_status_synced(env) -> bool:
    if not used_tool(env, "list_applications", stage=12) or not stage_write_used(env, 12):
        return False
    by_status = applications_by_status(env)
    if by_status.get("submitted"):
        return False
    advanced = [(status, row) for status in _STATUS_WORDS for row in by_status.get(status, [])]
    if not advanced:
        return False
    corpus = derived_text(env)
    return bool(corpus.strip()) and all(_bound_status(corpus, row, status) for status, row in advanced)


CHECKS = [("s12_status_synced", s12_status_synced, 2.5)]
