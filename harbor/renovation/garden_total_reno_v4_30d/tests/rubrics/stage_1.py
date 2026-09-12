"""Stage 1 — persist cross-service courtyard state distinctions."""
from .shared import _helpers as R

def s1_servers(env):
    backend = (
        R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM orders WHERE order_id=? AND status='delivered'", ("ord_qgrd_0001",))
        and R.backend_exists(env, "delivery_logistics", "SELECT COUNT(*) FROM shipments WHERE shipment_id=? AND status='delivered'", ("shp_qgrd_0001",))
        and R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM statements WHERE statement_id=? AND status='open'", ("stmt_qgrd",))
        and R.backend_exists(env, "listing_platform", "SELECT COUNT(*) FROM listings WHERE listing_id=? AND status='active'", ("lst_qgrd_0001",))
    )
    return backend and R.traced_persisted_evidence(env, 1, ("ecommerce", "delivery_logistics", "credit_card", "listing_platform"), "/workspace/order_tracker.md", (("ecommerce", "order"), ("logistics", "arrival"), ("listing", "display")), min_servers=3)

def s1_args(env):
    backend = (
        R.scalar(env, "ecommerce", "SELECT COUNT(*) FROM orders WHERE order_id IN (?,?)", ("ord_qgrd_0001", "ord_qgrd_0002")) == 2
        and R.backend_exists(env, "listing_platform", "SELECT COUNT(*) FROM listings WHERE listing_id=?", ("lst_qgrd_0001",))
    )
    return backend and R.three_threads_present(env, ("ord_qgrd_0001", "ord_qgrd_0002", "lst_qgrd_0001"))

def s1_result(env):
    backend = (
        R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM orders WHERE order_id=? AND total_minor=4200000 AND status='delivered'", ("ord_qgrd_0001",))
        and R.backend_exists(env, "listing_platform", "SELECT COUNT(*) FROM listings WHERE listing_id=? AND status='active'", ("lst_qgrd_0001",))
        and R.no_backend_rows(env, "listing_platform", "SELECT COUNT(*) FROM contacts")
    )
    return backend and R.artifact_has(env, "/workspace/budget.md", (("paid_minor",), ("resale_received_minor",), ("pending", "0"))) and R.heartbeat_has_stage(env, 1)

CHECKS = [("s1_servers", s1_servers, 0.5), ("s1_args", s1_args, 0.5), ("s1_result", s1_result, 1.0)]
