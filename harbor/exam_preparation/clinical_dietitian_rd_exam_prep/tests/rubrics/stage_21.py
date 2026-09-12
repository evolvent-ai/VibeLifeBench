from ._helpers import icu_base_calendar_ready, icu_makeup_calendar_ready, outpatient_approval_present, pediatrics_approval_present, notion_page_contains, sent_message_contains, tool_used, used_all_tools, workspace_contains, workspace_line_contains

STAGE = 21

def _tracker_core(env) -> bool:
    return workspace_contains(
        env,
        "internship_tracker.md",
        [["department"], ["planned_hours"], ["cancelled_hours"], ["completed_hours"], ["approved_hours"], ["approval_source"], ["evidence_status"], ["gap_hours"], ["last_verified_at"]],
        220,
    )

def _outpatient_row(env) -> bool:
    return workspace_line_contains(env, "internship_tracker.md", [["outpatient"], ["300"], ["approved", "confirmed"]], 220)

def _peds_row(env) -> bool:
    return workspace_line_contains(env, "internship_tracker.md", [["pediatrics"], ["400"], ["20"], ["380"], ["approved", "confirmed"]], 220)

def _icu_pending_row(env) -> bool:
    return workspace_line_contains(env, "internship_tracker.md", [["icu"], ["500"], ["20"], ["520"], ["pending", "awaiting confirmation", "draft"]], 220)

def _icu_email(env) -> bool:
    return sent_message_contains(env, "icu.preceptor@example.test", ["icu", "500", "20", "520", "confirmation"])

def _icu_notion(env) -> bool:
    return notion_page_contains(env, ["department competency", "hours", "tracker"], [["icu"], ["500"], ["20"], ["520"], ["pending", "awaiting confirmation"]])

def s21_icu_progress_reconciled(env) -> bool:
    return _tracker_core(env) and _icu_pending_row(env) and icu_base_calendar_ready(env) and icu_makeup_calendar_ready(env)

def s21_midpoint_tracker_present(env) -> bool:
    return outpatient_approval_present(env) and pediatrics_approval_present(env) and _tracker_core(env) and _outpatient_row(env) and _peds_row(env) and _icu_pending_row(env)

def s21_midpoint_calendar_reviewed(env) -> bool:
    return tool_used(env, STAGE, "calendar", None) and icu_base_calendar_ready(env) and icu_makeup_calendar_ready(env)

def s21_midpoint_three_places_reviewed(env) -> bool:
    return used_all_tools(env, STAGE, [("calendar", None), ("email", None), ("notion", None)]) and _icu_email(env) and _icu_notion(env)

CHECKS = [
    ("s21_icu_progress_reconciled", s21_icu_progress_reconciled, 1.25),
    ("s21_midpoint_tracker_present", s21_midpoint_tracker_present, 1.25),
    ("s21_midpoint_calendar_reviewed", s21_midpoint_calendar_reviewed, 1.25),
    ("s21_midpoint_three_places_reviewed", s21_midpoint_three_places_reviewed, 1.25),
]
