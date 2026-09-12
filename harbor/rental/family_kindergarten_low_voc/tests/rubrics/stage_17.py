from ._helpers import *


def r038_check_027_scheduled_checks_stage17(env) -> bool:
    return bool(
        stage_results_mention_candidates(env, 17, (C.A, C.B, C.C), min_count=3)
        and tool_stage_result_has(env, 17, 'review_platform', None, result_parts=['rv_river_mold_20260803', 'musty odor', 'dampness'])
        and state_evidence(env, 17, [C.A, C.B, C.C, 'last_checked'], ['rental_tracker.md', 'risk_log.md'])
    )


def r038_check_028_risk_log_open_closed(env) -> bool:
    return bool(
        candidate_a_backend_risky(env)
        and candidate_c_backend_trap(env)
        and state_evidence(env, 17, [C.A, 'open', 'professional inspection'], ['risk_log.md', 'rental_tracker.md'])
        and state_evidence(env, 17, [C.C, 'unacceptable', 'railing'], ['risk_log.md', 'rental_tracker.md'])
    )


CHECKS = [
    ("r038_check_027_scheduled_checks_stage17", r038_check_027_scheduled_checks_stage17, 1.25),
    ("r038_check_028_risk_log_open_closed", r038_check_028_risk_log_open_closed, 1.25),
]
