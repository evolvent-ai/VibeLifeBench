from __future__ import annotations

from ._helpers import notion_has, stage_record


def chk_s00_briefing_capture(env) -> bool:
    progress = stage_record(env, "stage_progress.md", 0, (("28 days", "July 1", "July 28"), ("neck and shoulder",), ("eye break",), ("walking",), ("personal",)), ("Observed at", "Trigger/source", "Facts read", "Decision", "Action/result", "Next check"))
    matrix = stage_record(env, "service_consistency_matrix.md", 0, (("calendar",), ("health_tracker",), ("notion",), ("email",), ("notification_hub",)), ("Object/reference", "Observed state", "Consistency status"))
    return progress and matrix and notion_has(env, "neck and shoulder", (("neck",), ("eye", "rest")))


def chk_s00_auth_and_files_initialized(env) -> bool:
    auth = stage_record(env, "auth_log.md", 0, (("student", "parent"), ("email",), ("health", "privacy"), ("do not send", "prohibited"), ("purchase", "paid", "registration")), ("Sensitive data", "Authorization status", "Permitted action", "Prohibited action"))
    budget = stage_record(env, "equipment_budget.md", 0, (("400",), ("do not purchase", "0"), ("free",)), ("Purchase/fee status", "Free alternative", "Budget spent"))
    return auth and budget


CHECKS = [
    ("chk_s00_briefing_capture", chk_s00_briefing_capture, 1.5),
    ("chk_s00_auth_and_files_initialized", chk_s00_auth_and_files_initialized, 1.5),
]
