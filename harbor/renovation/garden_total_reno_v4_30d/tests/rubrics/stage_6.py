"""Stage 6 — classify the drain-fitting transaction without premature dispute."""
from .shared import _helpers as R

def s6_servers(env):
    backend = (
        R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=? AND amount_minor=23800", ("tx_qgrd_fx",))
        and R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=?", ("ntf_qgrd_fx",))
    )
    return backend and R.trace_has_success(env, 6, ("credit_card",), min_count=1) and R.artifact_active(env, "/workspace/budget.md")

def s6_args(env):
    backend = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=? AND card_id=?", ("tx_qgrd_fx", "card_qgrd_01"))
    return backend and R.artifact_has(env, "/workspace/evidence_log.md", (("ntf_qgrd_fx", "drainage channel"), ("card_qgrd_01", "credit card")))

def s6_result(env):
    return R.backend_and_artifact(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=?", ("ntf_qgrd_fx",), "/workspace/budget.md", (("foreign currency", "original currency"), ("under review", "pending"), ("not refunded", "not disputed")))

CHECKS = [("s6_servers", s6_servers, 0.5), ("s6_args", s6_args, 0.5), ("s6_result", s6_result, 1.5)]
