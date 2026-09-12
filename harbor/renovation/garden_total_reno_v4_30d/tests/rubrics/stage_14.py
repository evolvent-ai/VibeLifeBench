"""Stage 14 — preserve the under-review drain-fitting dispute state."""
from .shared import _helpers as R


def _under_review_state(env):
    dispute = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM disputes WHERE dispute_id=? AND tx_id=? AND status='under_review'", ("disp_qgrd_01", "tx_qgrd_dup"))
    notice = R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=? AND payload_json LIKE ?", ("ntf_qgrd_disp", "%under_review%"))
    no_reversal = R.no_backend_rows(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id IN (?,?)", ("tx_qgrd_rev", "tx_qgrd_pp"))
    return dispute and notice and no_reversal


def s14_servers(env):
    return R.trace_has_success(env, 14, ("credit_card",), min_count=1) and _under_review_state(env) and R.artifact_active(env, "/workspace/evidence_log.md")


def s14_result(env):
    return R.backend_and_artifact(env, "credit_card", "SELECT COUNT(*) FROM disputes WHERE dispute_id=? AND tx_id=? AND status='under_review'", ("disp_qgrd_01", "tx_qgrd_dup"), "/workspace/budget.md", (("disp_qgrd_01",), ("under_review",), ("not reversed", "not refunded")))


def s14_no_bad(env):
    return _under_review_state(env) and R.artifact_has(env, "/workspace/budget.md", (("under_review",), ("not reversed", "not refunded"))) and R.no_unqualified_phrase(env, ("already refunded", "refund received", "no repayment needed"))


CHECKS = [("s14_servers", s14_servers, 0.5), ("s14_result", s14_result, 3.0), ("s14_no_bad", s14_no_bad, 0.5)]
