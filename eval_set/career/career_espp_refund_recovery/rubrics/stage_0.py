"""Stage 0 — 建立持股计划争议与再就业双线持久看板。"""
from __future__ import annotations

from ._helpers import record_text, text_has


def _structured_track(text: str, topic_groups: list[list[str]]) -> bool:
    return text_has(text, topic_groups + [["状态"], ["下一步", "待办"], ["来源", "依据"]])


def s0_dual_track_tracker(env) -> bool:
    equity = record_text(env, "severance_review.md")
    jobs = record_text(env, "job_tracker.md")
    return _structured_track(equity, [["持股", "股权", "价差", "回购"]]) and _structured_track(
        jobs, [["再就业", "求职", "岗位"]]
    )


CHECKS = [("s0_dual_track_tracker", s0_dual_track_tracker, 1.5)]
