"""Stage 20 — distinguish the posted flooring credit from earlier approval."""
from .shared import _helpers as R
from .shared import _helpers as H

def s20_servers(env):
    return H.refund_posted(env) and (R.trace_has_success(env, 20, ("credit_card",), min_count=1) and R.artifact_active(env, "/workspace/budget.md"))

def s20_result(env):
    return R.backend_and_artifact(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=? AND amount_minor=-2563000", ("tx_qflr_pp",), "/workspace/budget.md", (("tx_qflr_pp",), ("-2563000", "2563000"), ("posted", "posted"), ("refunded_minor",), ("net_outflow_minor",)))

CHECKS = [("s20_servers", s20_servers, 0.5), ("s20_result", s20_result, 2.5)]
