from ._helpers import guard_stage_checks
from . import _helpers as H
def s6_servers(env): return H._stage_servers_correct(env, 6, min_count=1)
def s6_args(env): return H._stage_tool_args_reference(env, 6, ["card_strr_01", "tx_strr_fx", "6693"], min_count=1)
def s6_result(env):
    text = H.scoped_text(env, ["budget", "decision", "risk"], idx=6)
    return H._stage_has_server(env, 6, "credit_card", tool="list_unbilled") and H._count_any(text, ["babyjogger", "overseas purchase", "dollars", "foreign currency"]) >= 1 and H._count_any(text, ["258"]) >= 1 and H._count_any(text, ["foreign currency", "exchange rate", "pending posting", "reconcile", "normal"]) >= 1
CHECKS = guard_stage_checks(6, [("s6_servers", s6_servers, 0.5), ("s6_args", s6_args, 0.5), ("s6_result", s6_result, 1.5)])
