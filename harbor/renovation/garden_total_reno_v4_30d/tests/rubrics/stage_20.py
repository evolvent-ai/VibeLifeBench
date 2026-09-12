"""Stage 20 — distinguish the posted drainage credit from earlier approval."""
from .shared import _helpers as R


def _posted_state(env):
    refund = R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='approved' AND refund_amount_minor=2646000", ("ref_qgrd_b",))
    adjustment = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=? AND amount_minor=-2646000 AND kind='adjustment'", ("tx_qgrd_pp",))
    notice = R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=? AND payload_json LIKE ?", ("ntf_qgrd_funds", "%tx_qgrd_pp%"))
    return refund and adjustment and notice


def s20_servers(env):
    return R.trace_has_success(env, 20, ("credit_card",), min_count=1) and _posted_state(env) and R.artifact_active(env, "/workspace/budget.md")


def s20_result(env):
    return _posted_state(env) and R.backend_and_artifact(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=? AND amount_minor=-2646000", ("tx_qgrd_pp",), "/workspace/budget.md", (("tx_qgrd_pp",), ("-2646000", "2646000"), ("posted",), ("refunded_minor",), ("net_outflow_minor",)))


CHECKS = [("s20_servers", s20_servers, 0.5), ("s20_result", s20_result, 2.5)]
