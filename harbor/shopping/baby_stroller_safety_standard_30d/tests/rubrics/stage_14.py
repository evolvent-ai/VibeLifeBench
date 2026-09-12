from ._helpers import guard_stage_checks
from . import _helpers as H
def s14_servers(env): return H._stage_servers_correct(env, 14, min_count=1)
def s14_result(env): return H._stage_has_server(env, 14, "credit_card", tool="list_disputes") and H._count_any(H.scoped_text(env, ["decision", "budget", "risk"], idx=14), ["dispute", "under review", "due date", "amount due", "separate", "normal repayment", "7/10"]) >= 3
def s14_no_bad(env):
    text = H.scoped_text(env, ["decision", "risk"], idx=14)
    return H._count_any(text, ["dispute", "under review", "normal repayment", "due date", "amount due"]) >= 2 and not H._has_bad_advice(text, ["do not repay because of the dispute", "stop repayment", "skip payment"])
CHECKS = guard_stage_checks(14, [("s14_servers", s14_servers, 0.5), ("s14_result", s14_result, 3.0), ("s14_no_bad", s14_no_bad, 0.5)])
