"""Stage 22 — cross-check courtyard evidence across all readable systems."""
from .shared import _helpers as R

SERVERS = ("weather", "ecommerce", "credit_card", "email", "calendar", "listing_platform")


def s22_consistency(env):
    weather = R.backend_exists(env, "weather", "SELECT COUNT(*) FROM daily_weather WHERE geo_key=? AND date='2026-07-09' AND precip_mm=14.0", ("geo_qgrd",))
    claim = R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='approved' AND refund_amount_minor=2646000", ("ref_qgrd_b",))
    funds = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id=? AND amount_minor=-2646000", ("tx_qgrd_pp",))
    survey = R.backend_exists(env, "email", "SELECT COUNT(*) FROM messages WHERE message_id=? AND headers_json LIKE ?", ("<20260625.1750.47ac@inspect.example>", "%XA-GR-0625%"))
    calendar = R.backend_exists(env, "calendar", "SELECT COUNT(*) FROM events WHERE event_id=? AND status='confirmed'", ("evt_qgrd_budget_review_0628",))
    listing = R.backend_exists(env, "listing_platform", "SELECT COUNT(*) FROM listings WHERE listing_id=? AND status='active'", ("lst_qgrd_0001",))
    queried = R.trace_has_success(env, 22, SERVERS, min_count=5)
    evidence = R.artifact_has(env, "/workspace/evidence_log.md", (("weather",), ("ecommerce", "order"), ("credit_card",), ("email",), ("calendar",), ("listing_platform", "listing"), ("limits", "cannot replace")))
    decision = R.artifact_has(env, "/workspace/decision_log.md", (("state conflict", "cross-check"), ("rain test", "acceptance"), ("posted",)))
    return weather and claim and funds and survey and calendar and listing and queried and evidence and decision


CHECKS = [("s22_consistency", s22_consistency, 2.0)]
