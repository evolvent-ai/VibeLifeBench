from ._helpers import *


def r038_check_032_a_as_backup_with_risk(env) -> bool:
    return bool(
        candidate_a_backend_risky(env)
        and a_viewing_cancelled(env)
        and tool_stage_result_has(
            env, 25, 'listing_platform', None, [C.A],
            [C.A, 'cancelled_until_2026-08-22', '2026-08-18T08:45'],
        )
        and state_evidence(env, 25, [C.A, 'backup', '8/22'], ['rental_tracker.md', 'risk_log.md'])
        and state_evidence(env, 25, [C.A, 'musty odor', 'testing'], ['rental_tracker.md', 'risk_log.md'])
        and no_external_side_effect(env)
    )


CHECKS = [
    ("r038_check_032_a_as_backup_with_risk", r038_check_032_a_as_backup_with_risk, 1.5),
]
