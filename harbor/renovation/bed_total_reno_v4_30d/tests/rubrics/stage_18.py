"""Stage 18 — verify both dispute approval and the posted reversal entry."""
from .shared import _helpers as R
from .shared import _backend as B


def s18_servers(env):
    return B.approved_reversal(env) and R.trace_has_success(env, 18, ("credit_card",), min_count=1) and R.artifact_active(env, "/workspace/budget.md")


def s18_result(env):
    approved = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM disputes WHERE dispute_id=? AND status='approved'", ("disp_qbed_01",))
    reversal = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=? AND amount_minor=-22000", ("tx_qbed_rev",))
    persisted = R.artifact_has(env, "/workspace/budget.md", (("disp_qbed_01",), ("tx_qbed_rev",), ("approved",), ("reversal",), ("-22000", "22000")))
    return B.approved_reversal(env) and approved and reversal and persisted


CHECKS = [("s18_servers", s18_servers, 0.5), ("s18_result", s18_result, 2.0)]
