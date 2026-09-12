from ._helpers import guard_stage_checks
from . import _helpers as H
def s2_servers(env): return H._stage_servers_correct(env, 2, min_count=2)
def s2_args(env): return H._stage_tool_args_reference(env, 2, ["prod_strr_main", "sku_strr_main", "ord_strr_0001", "oa_strr_brand"], min_count=2)
def s2_result(env):
    text = H.scoped_text(env, ["tracker", "decision", "risk", "gear"], idx=2)
    return H._stage_has_server(env, 2, "ecommerce", tool="get_product") and H._stage_has_server(env, 2, "notification_hub") and H._count_any(text, ["recall", "batch", "brake", "safety harness", "standard", "replacement", "return"]) >= 3 and H._count_any(text, ["gbs5-2026-03"]) >= 1 and H._count_any(text, ["vrf-strr-3m6693"]) >= 1 and bool(H._backend_batch_verified(env, "prod_strr_main", "GBS5-2026-03"))
def s2_options(env):
    text = H.scoped_text(env, ["gear", "decision", "tracker"], idx=2)
    return H._count_any(text, ["recall replacement", "brake reinforcement", "return", "free replacement"]) >= 2 and H._count_any(text, ["0", "120", "600", "free"]) >= 2 and H._count_any(text, ["onsite", "nearby", "cycle", "convenient"]) >= 2
CHECKS = guard_stage_checks(2, [("s2_servers", s2_servers, 0.5), ("s2_args", s2_args, 1.0), ("s2_result", s2_result, 2.0), ("s2_options", s2_options, 2.0)])
