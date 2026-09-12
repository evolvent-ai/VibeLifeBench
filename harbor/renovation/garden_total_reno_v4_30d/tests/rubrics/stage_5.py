"""Stage 5 — partition courtyard evidence into four domains."""
from .shared import _helpers as R

def s5_evidence(env):
    backend = (
        R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=?", ("ntf_qgrd_photo_scale",))
        and R.scalar(env, "ecommerce", "SELECT COUNT(*) FROM orders WHERE order_id IN (?,?)", ("ord_qgrd_0001", "ord_qgrd_0002")) == 2
        and R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM statements WHERE statement_id=?", ("stmt_qgrd",))
        and R.backend_exists(env, "listing_platform", "SELECT COUNT(*) FROM listings WHERE listing_id=?", ("lst_qgrd_0001",))
    )
    queried = R.trace_has_success(env, 5, ("ecommerce", "email", "credit_card", "listing_platform"), min_count=3)
    return backend and queried and R.artifact_has(env, "/workspace/evidence_log.md", (("design contract", "entity"), ("drainage", "pavement"), ("nursery stock", "maintenance"), ("funds", "retention payment"), ("elevation", "grading"), ("service", "source"), ("observed_at_stage", "date"))) and R.heartbeat_has_stage(env, 5)

CHECKS = [("s5_evidence", s5_evidence, 4.0)]
