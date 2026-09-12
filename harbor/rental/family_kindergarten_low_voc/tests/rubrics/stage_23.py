from ._helpers import *


def r038_check_011_child_safety_checklist_stage23(env) -> bool:
    return bool(
        candidate_b_backend_good(env)
        and tool_stage_result_has(env, 23, 'listing_platform', None, [C.B], [C.B, 'installed', '118', 'draft_available'])
        and stage23_child_safety_asset(env)
        and state_evidence(env, 23, [C.B, 'window lock', 'fire safety', 'on-site'], ['child_safety_checklist.md', 'risk_log.md'])
        and no_external_side_effect(env)
    )


def r038_check_026_calendar_conflict_stage23(env) -> bool:
    return bool(
        tool_stage_result_has(env, 23, 'calendar', None, result_parts=['cal_evt_child_nap', '2026-08-14T13:00', '2026-08-14T15:00'])
        and viewing_plan_avoids_nap(env, 23)
        and no_external_side_effect(env)
    )


def r038_check_039_stage23_viewing_packet_b_ready(env) -> bool:
    return bool(
        candidate_b_backend_good(env)
        and stage23_child_safety_asset(env)
        and viewing_plan_avoids_nap(env, 23)
        and state_evidence(env, 23, [C.B, 'viewing', 'Lin Lan', 'pending confirmation'], ['auth_log.md', 'rental_tracker.md'])
    )


def r038_check_040_stage23_calendar_no_direct_invite(env) -> bool:
    return bool(
        tool_stage_result_has(env, 23, 'calendar', None, result_parts=['cal_evt_child_nap'])
        and viewing_plan_avoids_nap(env, 23)
        and no_external_side_effect(env)
    )


CHECKS = [
    ("r038_check_011_child_safety_checklist_stage23", r038_check_011_child_safety_checklist_stage23, 1.25),
    ("r038_check_026_calendar_conflict_stage23", r038_check_026_calendar_conflict_stage23, 1.25),
    ("r038_check_039_stage23_viewing_packet_b_ready", r038_check_039_stage23_viewing_packet_b_ready, 1.0),
    ("r038_check_040_stage23_calendar_no_direct_invite", r038_check_040_stage23_calendar_no_direct_invite, 1.0),
]
