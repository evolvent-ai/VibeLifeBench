"""Stage 0 — establish equity dispute with re-employmentparallel trackspersistenttracker."""
from __future__ import annotations

from ._helpers import record_text, text_has


def _structured_track(text: str, topic_groups: list[list[str]]) -> bool:
    return text_has(text, topic_groups + [["status"], ["next", "next"], ["source", "basis"]])


def s0_dual_track_tracker(env) -> bool:
    equity = record_text(env, "severance_review.md")
    jobs = record_text(env, "job_tracker.md")
    return _structured_track(equity, [["ESPP", "redemption", "spread", "shortfall"]]) and _structured_track(
        jobs, [["re-employment", "job search", "role"]]
    )


CHECKS = [("s0_dual_track_tracker", s0_dual_track_tracker, 1.5)]
