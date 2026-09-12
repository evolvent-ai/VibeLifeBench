from ._helpers import guard_stage_checks
from . import _helpers as H
def s18_servers(env): return H._stage_servers_correct(env, 18, min_count=1)
def s18_result(env):
    text = H.scoped_text(env, ["budget", "decision", "tracker"], idx=18)
    if H._count_any(text, ["dispute", "approved", "reversal", "reversed", "amount due", "archive", "258"]) < 3: return False
    if not H._stage_has_server(env, 18, "credit_card", tool="list_disputes"):
        return False
    return H._backend_dispute_status_is(env, "card_strr_01", "disp_strr_01", "approved") is True and H._backend_reversal_present(env, "card_strr_01", amount_minor=-25800) is True
CHECKS = guard_stage_checks(18, [("s18_servers", s18_servers, 0.5), ("s18_result", s18_result, 2.0)])
