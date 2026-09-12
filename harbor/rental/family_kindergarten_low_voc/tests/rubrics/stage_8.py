from ._helpers import *


def r038_check_019_mutation_construction(env) -> bool:
    return bool(
        construction_backend_ready(env)
        and tool_stage_result_has(env, 8, 'maps', 'get_place_details', [C.PL_C], ['rd_sunbay_construction', '2026-08-16T22:00'])
        and tool_stage_result_has(env, 8, 'notification_hub', None, result_parts=['nt_sunbay_construction', C.C, 'midday_and_evening'])
        and state_evidence(env, 8, [C.C, 'construction', '2026-08-16'], ['risk_log.md', 'rental_tracker.md'])
        and construction_risks_recorded(env, 8)
    )


CHECKS = [
    ("r038_check_019_mutation_construction", r038_check_019_mutation_construction, 1.75),
]
