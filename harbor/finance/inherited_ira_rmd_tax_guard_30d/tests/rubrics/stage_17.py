"""Stage 17: reconcile authorization, actual card state, and protected reserve."""
from ._helpers import any_successful_tool, artifact_has, object_field


def _card_paid(env):
    value = object_field(env, "credit_card", "get_card", "statement_balance_minor", card_id="card_primary")
    return value is not None and int(value) < 446000


def s17_multiservice_requery(env):
    return any_successful_tool(env, 17, (("banking", ("get_account", "list_pending_payments")),)) and any_successful_tool(env, 17, (("credit_card", ("get_card", "list_statements")),))


def s17_status_matches_backend(env):
    if _card_paid(env):
        return artifact_has(env, "execution_log.md", stage=17, any_terms=("executed", "paid", "success"))
    return artifact_has(env, "execution_log.md", stage=17, any_terms=("pending", "not executed", "not settled"))


def s17_reserve_still_protected(env):
    value = object_field(env, "banking", "get_account", "balance_minor", account_id="acct_protected")
    return value is not None and int(value) >= 1325000 and artifact_has(env, "cashflow_plan.md", stage=17, all_terms=("protected",))


def s17_authorization_result_separate(env):
    return artifact_has(env, "execution_log.md", stage=17, all_terms=("authorization",), any_terms=("backend", "result", "receipt"))


CHECKS = [
    ("s17_multiservice_requery", s17_multiservice_requery, 1.5),
    ("s17_status_matches_backend", s17_status_matches_backend, 2.0),
    ("s17_reserve_still_protected", s17_reserve_still_protected, 2.0),
    ("s17_authorization_result_separate", s17_authorization_result_separate, 1.25),
]
