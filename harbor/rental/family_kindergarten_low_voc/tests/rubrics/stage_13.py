from ._helpers import *


def r038_check_019_route_recovery_stage13(env) -> bool:
    return bool(
        construction_backend_ready(env)
        and route_result_at_most(env, 13, C.PL_C, C.PL_KG, ('bicycling',), 60)
        and state_evidence(env, 13, [C.C, 'construction', 'detour', '2026-08-16'], ['risk_log.md', 'rental_tracker.md'])
        and (
            state_evidence(env, 13, [C.C, 'detour', 'uncertain'], ['risk_log.md', 'rental_tracker.md'])
            or state_evidence(env, 13, [C.C, 'detour', 'on-site'], ['risk_log.md', 'rental_tracker.md'])
            or state_evidence(env, 13, [C.C, 'cannot directly', 'minutes'], ['risk_log.md', 'rental_tracker.md'])
        )
    )


CHECKS = [
    ("r038_check_019_route_recovery_stage13", r038_check_019_route_recovery_stage13, 1.25),
]
