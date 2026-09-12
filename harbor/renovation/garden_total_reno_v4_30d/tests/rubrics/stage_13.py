"""Stage 13 — reconcile courtyard money states without counting promises as cash."""
from .shared import _helpers as R


def s13_budget(env):
    calendar = R.backend_exists(env, "calendar", "SELECT COUNT(*) FROM events WHERE event_id=? AND status='confirmed' AND description LIKE ?", ("evt_qgrd_budget_review_0628", "%approval, posting, and proceeds are separate%"))
    paid_order = R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM orders WHERE order_id=? AND status='delivered' AND total_minor=4200000", ("ord_qgrd_0001",))
    claim = R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='rejected' AND refund_amount_minor=2478000", ("ref_qgrd_b",))
    duplicate = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=? AND amount_minor=23800", ("tx_qgrd_dup",))
    listing = R.backend_exists(env, "listing_platform", "SELECT COUNT(*) FROM listings WHERE listing_id=? AND status='active' AND price_minor=31800", ("lst_qgrd_0001",))
    queried = R.trace_has_success(env, 13, ("calendar", "ecommerce", "credit_card", "listing_platform"), min_count=3)
    fields = R.artifact_fields_set(env, "/workspace/budget.md", ("currency", "paid_minor", "refund_pending_minor", "refunded_minor", "holdback_minor", "resale_received_minor", "source_objects", "as_of_stage"))
    text = R.artifact_has(env, "/workspace/budget.md", (("project payment",), ("retention payment",), ("corrective work",), ("nursery stock",), ("surplus materials",), ("under review", "pending"), ("posted",)))
    return calendar and paid_order and claim and duplicate and listing and queried and fields and text


CHECKS = [("s13_budget", s13_budget, 3.0)]
