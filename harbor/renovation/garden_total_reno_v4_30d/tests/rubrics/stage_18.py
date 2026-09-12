"""Stage 18 — verify dispute approval and the drain-charge reversal entry."""
from .shared import _helpers as R


def _reversal_state(env):
    approved = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM disputes WHERE dispute_id=? AND tx_id=? AND status='approved'", ("disp_qgrd_01", "tx_qgrd_dup"))
    reversal = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=? AND amount_minor=-23800 AND kind IN ('adjustment','reversal')", ("tx_qgrd_rev",))
    notice = R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=? AND payload_json LIKE ?", ("ntf_qgrd_rev", "%tx_qgrd_rev%"))
    return approved and reversal and notice


def s18_servers(env):
    return R.trace_has_success(env, 18, ("credit_card",), min_count=1) and _reversal_state(env) and R.artifact_active(env, "/workspace/budget.md")


def s18_result(env):
    persisted = R.artifact_has(env, "/workspace/budget.md", (("disp_qgrd_01",), ("tx_qgrd_rev",), ("approved",), ("reversal",), ("-23800", "23800")))
    return _reversal_state(env) and persisted


CHECKS = [("s18_servers", s18_servers, 0.5), ("s18_result", s18_result, 2.0)]
