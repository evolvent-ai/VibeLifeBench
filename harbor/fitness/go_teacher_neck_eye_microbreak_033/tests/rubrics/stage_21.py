from __future__ import annotations

from ._helpers import notion_has, stage_record


def chk_s21_midpoint_review_updates_next_plan(env) -> bool:
    progress = stage_record(env, "stage_progress.md", 21, (("midpoint",), ("teaching-schedule changes",), ("health risks",), ("data quality",), ("authorization",), ("following week", "following week")), ("Facts read", "Decision", "Updated artifacts", "Next check"))
    return progress and notion_has(env, "neck and shoulder", (("neck",), ("eye",)))


CHECKS = [("chk_s21_midpoint_review_updates_next_plan", chk_s21_midpoint_review_updates_next_plan, 1.5)]
