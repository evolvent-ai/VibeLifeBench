"""Stage 23 — finalize a structured, three-line courtyard closeout."""
from .shared import _helpers as R

THREADS = ("ord_qgrd_0001", "ord_qgrd_0002", "lst_qgrd_0001")


def s23_structured(env):
    return R.final_sections_present(env, THREADS) and R.artifact_fields_set(env, "/workspace/final_summary.md", ("as_of_stage",))


def s23_threads(env):
    orders = R.scalar(env, "ecommerce", "SELECT COUNT(*) FROM orders WHERE order_id IN (?,?)", ("ord_qgrd_0001", "ord_qgrd_0002")) == 2
    claim = R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='approved' AND refund_amount_minor=2646000", ("ref_qgrd_b",))
    card = R.backend_exists(env, "credit_card", "SELECT COUNT(*) FROM disputes WHERE dispute_id=? AND status='approved'", ("disp_qgrd_01",)) and R.scalar(env, "credit_card", "SELECT COUNT(*) FROM unbilled_transactions WHERE tx_id IN (?,?) AND amount_minor < 0", ("tx_qgrd_rev", "tx_qgrd_pp")) == 2
    listing = R.backend_exists(env, "listing_platform", "SELECT COUNT(*) FROM listings WHERE listing_id=? AND status='active'", ("lst_qgrd_0001",))
    structured = R.three_threads_present(env, THREADS)
    content = R.artifact_has(env, "/workspace/final_summary.md", (("grading",), ("drainage-channel connection",), ("permeable pavement",), ("ponding",), ("nursery stock",), ("outdoor light",), ("retention payment",), ("reversal",), ("surplus-material proceeds", "listing")))
    return orders and claim and card and listing and structured and content


CHECKS = [("s23_structured", s23_structured, 2.0), ("s23_threads", s23_threads, 1.0)]
