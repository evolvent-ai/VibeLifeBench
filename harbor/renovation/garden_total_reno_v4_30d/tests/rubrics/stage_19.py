"""Stage 19 — record approved local drainage responsibility without inventing receipt."""
from .shared import _helpers as R


def s19_result(env):
    notice = R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=? AND payload_json LIKE ?", ("ntf_qgrd_ship", "%2646000%"))
    refund = R.backend_and_artifact(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='approved' AND refund_amount_minor=2646000", ("ref_qgrd_b",), "/workspace/order_tracker.md", (("ref_qgrd_b",), ("approved",), ("localized grading", "drainage connection"), ("delay compensation", "compensation"), ("pending", "pending posting")))
    not_posted = R.no_backend_rows(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=?", ("tx_qgrd_pp",))
    return notice and refund and not_posted


CHECKS = [("s19_result", s19_result, 2.5)]
