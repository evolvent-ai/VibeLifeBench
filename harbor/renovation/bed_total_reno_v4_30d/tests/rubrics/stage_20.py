"""Stage 20 — distinguish the posted remediation credit from earlier approval."""
from .shared import _helpers as R
from .shared import _backend as B


def s20_servers(env):
    return B.posted_refund(env) and R.trace_has_success(env, 20, ("credit_card",), min_count=1) and R.artifact_active(env, "/workspace/budget.md")


def s20_result(env):
    return B.posted_refund(env) and R.backend_and_artifact(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=? AND amount_minor=-2142000", ("tx_qbed_pp",), "/workspace/budget.md", (("tx_qbed_pp",), ("-2142000", "2142000"), ("funds posting", "posted"), ("refunded_minor",), ("net_outflow_minor",)))


CHECKS = [("s20_servers", s20_servers, 0.5), ("s20_result", s20_result, 2.5)]
