from ._helpers import *


def r038_check_041_stage27_primary_choice_archived(env) -> bool:
    return bool(
        final_refresh_matrix(env)
        and candidate_b_backend_good(env)
        and candidate_a_backend_risky(env)
        and candidate_c_backend_trap(env)
        and a_viewing_cancelled(env)
        and b_written_terms_email_ready(env)
        and c_lockfee_notice_ready(env)
        and stage_notion_has(env, 27, C.B, 'first choice')
        and stage_notion_has(env, 27, C.A, 'backup')
        and stage_notion_has(env, 27, C.C, 'rejected')
        and state_evidence(env, 27, [C.B, '10600', '320', '10920'], ['budget_ledger.md', 'final_review.md'])
        and ventilation_plan_ready(env)
        and state_evidence(env, 27, [C.B, 'viewing', 'pending confirmation', 'Lin Lan'], ['auth_log.md', 'final_review.md'])
        and no_external_side_effect(env)
    )


CHECKS = [
    ('r038_check_041_stage27_primary_choice_archived', r038_check_041_stage27_primary_choice_archived, 1.5),
]
