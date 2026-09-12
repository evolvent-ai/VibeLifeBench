"""Stage 21: card status is taken from the real card backend."""
from ._helpers import any_successful_tool, artifact_has, object_field


def _statement_balance(env):
    value = object_field(env, "credit_card", "get_card", "statement_balance_minor", card_id="card_primary")
    return None if value is None else int(value)


def s21_card_requery(env):
    return any_successful_tool(env, 21, (("credit_card", ("get_card", "list_statements")),))


def s21_backend_payment_state(env):
    balance = _statement_balance(env)
    return balance == 394000 and artifact_has(
        env,
        "execution_log.md",
        stage=21,
        all_terms=("394000", "payment"),
        any_terms=("backend", "statement", "result"),
    )


def s21_ledger_matches_state(env):
    balance = _statement_balance(env)
    if balance is None:
        return False
    if balance == 394000:
        return artifact_has(env, "execution_log.md", stage=21, all_terms=("394000",), any_terms=("executed", "paid", "partial"))
    return False


def s21_no_inference_from_authorization(env):
    return artifact_has(env, "decision_ledger.md", stage=21, any_terms=("backend", "statement", "authorization is not execution", "actual result"))


CHECKS = [
    ("s21_card_requery", s21_card_requery, 1.5),
    ("s21_backend_payment_state", s21_backend_payment_state, 1.25),
    ("s21_ledger_matches_state", s21_ledger_matches_state, 2.0),
    ("s21_no_inference_from_authorization", s21_no_inference_from_authorization, 1.5),
]
