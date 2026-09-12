"""Stage 17 — persist the authorized platform evidence-submission plan only."""
from .shared import _helpers as R


def s17_platform(env):
    return R.artifact_has(env, "/workspace/decision_log.md", (("authorization",), ("submit to platform", "platform submission"), ("measurement", "rain test"), ("localized pavement removal",), ("connection adjustment",)))


def s17_confirm(env):
    return R.artifact_has(env, "/workspace/order_tracker.md", (("ref_qgrd_b",), ("next step", "next_action"), ("final acceptance",), ("Evan Young", "owner")))


def s17_no_bad(env):
    claim = R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='rejected'", ("ref_qgrd_b",))
    dispute = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM disputes WHERE dispute_id=? AND status='under_review'", ("disp_qgrd_01",))
    listing = R.backend_exists(env, "listing_platform", "SELECT COUNT(*) FROM listings WHERE listing_id=? AND status='active'", ("lst_qgrd_0001",))
    no_mail = R.no_backend_rows(env, "email", "SELECT COUNT(*) FROM sent_log")
    no_order = R.no_new_order(env, after="2026-06-22T00:00:00+08:00")
    text = R.artifact_has(env, "/workspace/decision_log.md", (("authorization",), ("submit to platform", "platform submission"), ("final acceptance", "owner")))
    return claim and dispute and listing and no_mail and no_order and text and R.no_unqualified_phrase(env, ("final acceptance completed", "confirm acceptance on behalf", "addition paid"))


CHECKS = [("s17_platform", s17_platform, 2.0), ("s17_confirm", s17_confirm, 2.0), ("s17_no_bad", s17_no_bad, 0.5)]
