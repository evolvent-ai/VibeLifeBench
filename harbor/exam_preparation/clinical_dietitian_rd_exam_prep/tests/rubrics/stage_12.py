from ._helpers import peds_cancelled_state, tool_used, workspace_contains, workspace_line_contains

STAGE = 12

def _peds_pending_tracker(env) -> bool:
    return workspace_contains(
        env,
        "internship_tracker.md",
        [["department"], ["planned_hours"], ["cancelled_hours"], ["completed_hours"], ["approved_hours"], ["gap_hours"], ["evidence_status"]],
        180,
    ) and workspace_line_contains(
        env,
        "internship_tracker.md",
        [["pediatrics"], ["400"], ["20"], ["380"], ["pending", "awaiting confirmation"], ["rd_activity_061"], ["rd_activity_062"]],
        180,
    )

def s12_peds_gap_recorded(env) -> bool:
    return peds_cancelled_state(env) and tool_used(env, STAGE, "calendar", None) and tool_used(env, STAGE, "notion", None) and _peds_pending_tracker(env)

def s12_no_peds_overclaim(env) -> bool:
    return peds_cancelled_state(env) and _peds_pending_tracker(env)

CHECKS = [
    ("s12_peds_gap_recorded", s12_peds_gap_recorded, 1.75),
    ("s12_no_peds_overclaim", s12_no_peds_overclaim, 2.0),
]
