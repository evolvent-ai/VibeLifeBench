"""Stage 18 — verify dispute approval and the thermostat reversal entry."""
from .shared import _helpers as R
from .shared import _helpers as H

def s18_servers(env):
    return H.reversal(env) and (R.trace_has_success(env, 18, ("credit_card",), min_count=1) and R.artifact_active(env, "/workspace/budget.md"))

def s18_result(env):
    approved = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM disputes WHERE dispute_id=? AND status='approved'", ("disp_qflr_01",))
    reversal = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=? AND amount_minor=-23200", ("tx_qflr_rev",))
    persisted = R.artifact_has(env, "/workspace/budget.md", (("disp_qflr_01",), ("tx_qflr_rev",), ("approved", "approved"), ("reversal",), ("-23200", "23200")))
    return approved and reversal and persisted

CHECKS = [("s18_servers", s18_servers, 0.5), ("s18_result", s18_result, 2.0)]
