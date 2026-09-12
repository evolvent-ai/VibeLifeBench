"""Stage 2 — verify contract/SKU identity and missing evidence."""
from .shared import _helpers as R
from .shared import _backend as B

EVIDENCE = "/workspace/evidence_log.md"

def s2_servers(env):
    return R.traced_persisted_evidence(env, 2, ("ecommerce", "email"), EVIDENCE, (("prod_qbed_main",), ("sku_qbed_main",)), min_servers=2) and B.contract_sources(env)

def s2_args(env):
    return B.contract_sources(env) and R.artifact_has(env, EVIDENCE, (("ord_qbed_0001",), ("prod_qbed_main",), ("sku_qbed_main",)))

def s2_result(env):
    return B.contract_sources(env) and R.backend_and_artifact(env, "ecommerce", "SELECT COUNT(*) FROM skus WHERE sku_id=? AND attrs_json LIKE ?", ("sku_qbed_main", "%VRF-QBED-6473G%"), EVIDENCE, (("VRF-QBED-6473G",), ("contract validation code", "vcode")))

def s2_options(env):
    return B.contract_sources(env) and R.artifact_has(env, "/workspace/risk_register.md", (("credentials", "qualification"), ("authorization letter", "contracting party"), ("contract",), ("supplementation", "missing")))

CHECKS = [("s2_servers", s2_servers, 0.5), ("s2_args", s2_args, 1.0), ("s2_result", s2_result, 2.0), ("s2_options", s2_options, 2.0)]
