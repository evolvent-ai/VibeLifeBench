"""Stage 0 — establish three independent courtyard ledgers."""
from .shared import _helpers as R
TRACKER = "/workspace/order_tracker.md"

def s0_servers(env):
    backend = (
        R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM orders WHERE order_id=? AND status='delivered'", ("ord_qgrd_0001",))
        and R.backend_exists(env, "delivery_logistics", "SELECT COUNT(*) FROM shipments WHERE shipment_id=? AND status='delivered'", ("shp_qgrd_0001",))
        and R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM cards WHERE card_id=? AND status='active'", ("card_qgrd_01",))
    )
    return backend and R.traced_persisted_evidence(env, 0, ("ecommerce", "delivery_logistics", "credit_card"), TRACKER, (("ord_qgrd_0001",), ("ord_qgrd_0002",), ("lst_qgrd_0001",)), min_servers=2)

def s0_args(env):
    backend = (
        R.scalar(env, "ecommerce", "SELECT COUNT(*) FROM orders WHERE order_id IN (?,?)", ("ord_qgrd_0001", "ord_qgrd_0002")) == 2
        and R.backend_exists(env, "listing_platform", "SELECT COUNT(*) FROM listings WHERE listing_id=? AND status='active'", ("lst_qgrd_0001",))
    )
    return backend and R.three_threads_present(env, ("ord_qgrd_0001", "ord_qgrd_0002", "lst_qgrd_0001")) and R.heartbeat_has_stage(env, 0)

def s0_result(env):
    backend = (
        R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM orders WHERE order_id=? AND status='delivered'", ("ord_qgrd_0001",))
        and R.backend_exists(env, "delivery_logistics", "SELECT COUNT(*) FROM shipments WHERE shipment_id=? AND status='delivered'", ("shp_qgrd_0001",))
        and R.backend_exists(env, "listing_platform", "SELECT COUNT(*) FROM listings WHERE listing_id=? AND status='active'", ("lst_qgrd_0001",))
        and R.no_backend_rows(env, "ecommerce", "SELECT COUNT(*) FROM refunds")
        and R.no_backend_rows(env, "credit_card", "SELECT COUNT(*) FROM disputes")
    )
    return backend and R.artifact_has(env, TRACKER, (("delivered",), ("drainage", "grading"), ("rain test", "acceptance"), ("posted", "proceeds")))

def s0_files(env):
    return R.artifact_active(env, "/workspace/risk_register.md") and R.artifact_active(env, "/workspace/budget.md")

CHECKS = [("s0_servers", s0_servers, 0.5), ("s0_args", s0_args, 1.0), ("s0_result", s0_result, 1.5), ("s0_files", s0_files, 0.5)]
