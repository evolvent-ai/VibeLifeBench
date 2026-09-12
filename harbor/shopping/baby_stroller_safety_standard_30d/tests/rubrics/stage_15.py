from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS
def s15_servers(env): return H._stage_servers_correct(env, 15, min_count=2)
def s15_result(env):
    text = H.files_text(env, ["decision", "tracker", "gear"]) + "\n" + H._agent_response(env, 15)
    return H._stages_have_servers(env, [(15, "calendar"), (15, "delivery_logistics")]) and H._thread_block_has_terms(text, THREAD_IDS[1], ["platform intervention", "additional evidence", "7/9", "return", "deadline", "evidence"], min_count=3, window=320) and bool(H._backend_refund_status_is(env, "ord_strr_0002", "ref_strr_b", "rejected"))
CHECKS = guard_stage_checks(15, [("s15_servers", s15_servers, 0.5), ("s15_result", s15_result, 3.0)])
