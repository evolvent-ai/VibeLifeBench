"""Stage 11: the scheduled card outflow is pending, not completed."""
from ._helpers import any_successful_tool, artifact_has, call_tool, rows


def s11_pending_row_visible(env):
    data = call_tool(env, "banking", "list_pending_payments", user_id="usr_fin", account_id="acct_checking_main", status_filter="pending", limit=50)
    backend = any(int(row.get("amount_minor", -1)) == 52000 and row.get("scheduled_for") == "2026-06-25" for row in rows(data, "pending_payments", "payments"))
    return backend and artifact_has(env, "cashflow_plan.md", stage=11, any_terms=("pending", "scheduled"))


def s11_banking_requery(env):
    return any_successful_tool(env, 11, (("banking", ("list_pending_payments", "get_account")),))


def s11_cashflow_pending(env):
    return artifact_has(env, "cashflow_plan.md", stage=11, all_terms=("52000",), any_terms=("pending", "scheduled"))


def s11_not_false_execution(env):
    return artifact_has(env, "decision_ledger.md", stage=11, any_terms=("not executed", "pending", "not settled"))


CHECKS = [
    ("s11_pending_row_visible", s11_pending_row_visible, 1.5),
    ("s11_banking_requery", s11_banking_requery, 1.0),
    ("s11_cashflow_pending", s11_cashflow_pending, 1.25),
    ("s11_not_false_execution", s11_not_false_execution, 1.5),
]
