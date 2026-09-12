from ._helpers import guard_stage_checks
from . import _helpers as H
def s10_servers(env): return H._stage_servers_correct(env, 10, min_count=1)
def s10_args(env): return H._stage_tool_args_reference(env, 10, ["card_strr_01", "tx_strr_dup", "6693"], min_count=1)
def s10_result(env): return H._stage_has_server(env, 10, "credit_card", tool="list_unbilled") and H._count_any(H.scoped_text(env, ["risk", "decision", "budget"], idx=10), ["duplicate charge", "duplicate payment", "same merchant", "two charges", "same amount", "dispute", "reconcile", "258"]) >= 3
def s10_no_bad(env):
    text = H.scoped_text(env, ["risk", "decision"], idx=10)
    return H._count_any(text, ["duplicate charge", "reconcile", "dispute", "pending verification", "do not ignore"]) >= 2 and not H._has_bad_advice(text, ["it is normal", "no action needed", "ignore this charge"])
CHECKS = guard_stage_checks(10, [("s10_servers", s10_servers, 0.5), ("s10_args", s10_args, 0.5), ("s10_result", s10_result, 3.0), ("s10_no_bad", s10_no_bad, 0.5)])
