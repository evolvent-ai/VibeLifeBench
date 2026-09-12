from ._helpers import no_premature_cdr_submission, registration_pending_state, tool_used, workspace_contains

STAGE = 26

def s26_registration_confirmed_after_auth(env) -> bool:
    return (
        tool_used(env, STAGE, "notification_hub", None)
        and registration_pending_state(env)
        and no_premature_cdr_submission(env)
        and workspace_contains(env, "auth_log.md", [["eligibility"], ["submitted"], ["authorization to test", "att"], ["pending"], ["pearson vue"], ["not_booked"], ["do not pay", "not paid", "pending authorization"]], 120)
    )

CHECKS = [("s26_registration_confirmed_after_auth", s26_registration_confirmed_after_auth, 1.75)]
