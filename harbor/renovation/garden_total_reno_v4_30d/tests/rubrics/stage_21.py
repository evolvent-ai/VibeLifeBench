"""Stage 21 — prepare an owner/evidence/next-step courtyard closeout checklist."""
from .shared import _helpers as R


def _closeout_state(env):
    orders = R.scalar(env, "ecommerce", "SELECT COUNT(*) FROM orders WHERE (order_id=? AND status='delivered') OR (order_id=? AND status='shipped')", ("ord_qgrd_0001", "ord_qgrd_0002")) == 2
    claim = R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='approved' AND refund_amount_minor=2646000", ("ref_qgrd_b",))
    dispute = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM disputes WHERE dispute_id=? AND status='approved'", ("disp_qgrd_01",))
    credits = R.scalar(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id IN (?,?) AND amount_minor < 0", ("tx_qgrd_rev", "tx_qgrd_pp")) == 2
    listing = R.backend_exists(env, "listing_platform", "SELECT COUNT(*) FROM listings WHERE listing_id=? AND status='active'", ("lst_qgrd_0001",))
    return orders and claim and dispute and credits and listing


def s21_checklist(env):
    text = R.artifact_has(env, "/workspace/order_tracker.md", (("entity", "contract"), ("localized pavement removal",), ("drainage-channel connection",), ("rain test",), ("nursery stock",), ("outdoor light",), ("credit card",), ("retention payment",), ("surplus materials",), ("evidence",), ("next step", "next_action"), ("responsibility", "owner")))
    return _closeout_state(env) and text and R.heartbeat_has_stage(env, 21)


CHECKS = [("s21_checklist", s21_checklist, 2.0)]
