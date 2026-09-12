"""Stage 2 — verify floor-system contract and SKU identity."""
from .shared import _helpers as R
from .shared import _helpers as H
EVIDENCE = "/workspace/evidence_log.md"

def s2_servers(env):
    return H.contract_context(env) and (R.traced_persisted_evidence(env, 2, ("ecommerce", "email"), EVIDENCE, (("prod_qflr_main",), ("sku_qflr_main",)), min_servers=2))

def s2_args(env):
    return H.contract_context(env) and (R.artifact_has(env, EVIDENCE, (("ord_qflr_0001",), ("prod_qflr_main",), ("sku_qflr_main",))))

def s2_result(env):
    return R.backend_and_artifact(env, "ecommerce", "SELECT COUNT(*) FROM skus WHERE sku_id=? AND attrs_json LIKE ?", ("sku_qflr_main", "%VRF-QFLR-7584G%"), EVIDENCE, (("VRF-QFLR-7584G",), ("contract validation code", "vcode")))

def s2_options(env):
    return H.contract_context(env) and (R.artifact_has(env, "/workspace/risk_register.md", (("credentials",), ("underfloor heating", "underfloor-heating"), ("leveling",), ("flooring",), ("authorization letter", "contractor"), ("supplementation needed", "missing"))))

CHECKS = [("s2_servers", s2_servers, 0.5), ("s2_args", s2_args, 1.0), ("s2_result", s2_result, 2.0), ("s2_options", s2_options, 2.0)]
