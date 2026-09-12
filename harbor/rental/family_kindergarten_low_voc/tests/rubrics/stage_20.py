from ._helpers import *


def r038_check_017_written_terms_stage20(env) -> bool:
    return bool(
        b_written_terms_email_ready(env)
        and tool_stage_result_has(
            env, 20, 'email', 'read_email',
            result_parts=['msg_b_written_terms', 'window lock', 'maintenance', 'pollution', 'deposit', 'tenant confirmation'],
        )
        and state_evidence(env, 20, [C.B, 'window lock', 'maintenance', 'pollution', 'deposit'], ['risk_log.md', 'rental_tracker.md', 'auth_log.md'])
        and state_evidence(env, 20, [C.B, 'tenant confirmation'], ['auth_log.md', 'rental_tracker.md'])
        and no_external_side_effect(env)
    )


def r038_check_031_b_as_first_choice_stage20(env) -> bool:
    return bool(
        candidate_b_backend_good(env)
        and candidate_a_backend_risky(env)
        and candidate_c_backend_trap(env)
        and b_written_terms_email_ready(env)
        and state_evidence(env, 20, [C.B, 'first choice', '10920', '8/10'], ['rental_tracker.md', 'budget_ledger.md'])
        and state_evidence(env, 20, [C.B, 'window lock', 'pollution', 'contract'], ['rental_tracker.md', 'risk_log.md'])
    )


CHECKS = [
    ("r038_check_017_written_terms_stage20", r038_check_017_written_terms_stage20, 1.75),
    ("r038_check_031_b_as_first_choice_stage20", r038_check_031_b_as_first_choice_stage20, 1.25),
]
