import math

from ._helpers import all_three_approvals_present, exam_booking_state, exam_calendar_confirmed, exact_1200_tracker_ready, has_compliant_medprep_refusal, health_fatigue_signal_present, response, task_subscription_inactive, tool_used, workspace_contains

def final_all_core_logs_exist(env) -> bool:
    return (
        workspace_contains(env, "internship_tracker.md", [["department"], ["approved_hours"], ["approval_source"], ["evidence_status"], ["gap_hours"], ["last_verified_at"]], 180)
        and workspace_contains(env, "risk_log.md", [["risk"], ["evidence"], ["severity"], ["mitigation"], ["authorization_needed"], ["next_review"]], 120)
        and workspace_contains(env, "final_review.md", [["local_program_1200_hours_status"], ["department_approval_chain"], ["cdr_eligibility_status"], ["authorization_to_test_status"], ["pearson_vue_status"], ["privacy_status"], ["fatigue_interventions"], ["subscription_status"], ["open_items"]], 300)
        and all_three_approvals_present(env)
        and exact_1200_tracker_ready(env)
        and has_compliant_medprep_refusal(env)
        and health_fatigue_signal_present(env)
        and exam_booking_state(env)
        and exam_calendar_confirmed(env)
        and task_subscription_inactive(env)
    )

def final_checker_count_sanity(env) -> bool:
    return (
        tool_used(env, 34, "notion", "API-post-search")
        and all(term in response(env, 34).lower() for term in ("final", "review", "recorded"))
    )

CHECKS = [
    ("final_all_core_logs_exist", final_all_core_logs_exist, 1.5),
    ("final_checker_count_sanity", final_checker_count_sanity, 1.0),
]
