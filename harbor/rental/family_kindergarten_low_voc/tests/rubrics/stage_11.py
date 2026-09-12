from ._helpers import *


def r038_check_020_mutation_description(env) -> bool:
    return bool(
        a_description_changed(env)
        and tool_stage_result_has(
            env, 11, 'listing_platform', None, [C.A],
            [C.A, 'description_changed', '2026-07-29', 'continue ventilation', 'rainy-season wall corners'],
        )
        and state_evidence(env, 11, [C.A, 'description', '2026-07-29'], ['risk_log.md', 'rental_tracker.md'])
        and state_evidence(env, 11, [C.A, 'continue ventilation', 'rainy-season wall corners'], ['risk_log.md', 'rental_tracker.md'])
        and no_external_side_effect(env)
    )


CHECKS = [
    ("r038_check_020_mutation_description", r038_check_020_mutation_description, 1.25),
]
