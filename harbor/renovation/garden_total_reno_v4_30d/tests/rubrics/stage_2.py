"""Stage 2 — verify courtyard contract and SKU identity."""
from .shared import _helpers as R
EVIDENCE = "/workspace/evidence_log.md"

def s2_servers(env):
    backend = (
        R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM products WHERE product_id=?", ("prod_qgrd_main",))
        and R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM skus WHERE sku_id=? AND attrs_json LIKE ?", ("sku_qgrd_main", "%VRF-QGRD-2928G%"))
        and R.backend_exists(env, "email", "SELECT COUNT(*) FROM messages WHERE body_text LIKE ?", ("%responsible-person signature page%",))
        and R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=?", ("ntf_qgrd_acceptance_rule",))
    )
    return backend and R.traced_persisted_evidence(env, 2, ("ecommerce", "email"), EVIDENCE, (("prod_qgrd_main",), ("sku_qgrd_main",)), min_servers=2)

def s2_args(env):
    backend = (
        R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM orders WHERE order_id=?", ("ord_qgrd_0001",))
        and R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM skus WHERE sku_id=?", ("sku_qgrd_main",))
    )
    return backend and R.artifact_has(env, EVIDENCE, (("ord_qgrd_0001",), ("prod_qgrd_main",), ("sku_qgrd_main",)))

def s2_result(env):
    return R.backend_and_artifact(env, "ecommerce", "SELECT COUNT(*) FROM skus WHERE sku_id=? AND attrs_json LIKE ?", ("sku_qgrd_main", "%VRF-QGRD-2928G%"), EVIDENCE, (("VRF-QGRD-2928G",), ("contract verification code", "vcode")))

def s2_options(env):
    gap_visible = R.backend_exists(env, "email", "SELECT COUNT(*) FROM messages WHERE body_text LIKE ? AND body_text LIKE ?", ("%authorization letter%", "%responsible-person signature page%"))
    return gap_visible and R.artifact_has(env, "/workspace/risk_register.md", (("qualification",), ("drainage",), ("pavement",), ("nursery stock",), ("authorization letter", "entity"), ("to supplement", "missing")))

CHECKS = [("s2_servers", s2_servers, 0.5), ("s2_args", s2_args, 1.0), ("s2_result", s2_result, 2.0), ("s2_options", s2_options, 2.0)]
