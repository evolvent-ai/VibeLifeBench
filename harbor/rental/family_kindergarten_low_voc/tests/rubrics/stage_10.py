from ._helpers import *


def r038_check_017_lease_written_terms(env) -> bool:
    return bool(
        tool_stage_result_has(env, 10, 'listing_platform', None, [C.B], [C.B, 'draft_available', 'installed', 'low'])
        and b_written_terms_backend_ready(env)
        and state_evidence(env, 10, [C.B, 'window lock', 'maintenance', 'pollution', 'deposit'], ['risk_log.md', 'rental_tracker.md', 'auth_log.md'])
        and state_evidence(env, 10, [C.B, 'written', 'confirmation'], ['risk_log.md', 'rental_tracker.md', 'auth_log.md'])
        and no_external_side_effect(env)
    )


CHECKS = [
    ("r038_check_017_lease_written_terms", r038_check_017_lease_written_terms, 1.5),
]
