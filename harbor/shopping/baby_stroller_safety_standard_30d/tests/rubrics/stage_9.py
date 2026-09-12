from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS
def s9_servers(env): return H._stage_servers_correct(env, 9, min_count=2) and H._stage_server_order_ok(env, 9, ["ecommerce", "notification_hub"])
def s9_args(env): return H._stage_tool_args_reference(env, 9, ["ord_strr_0002", "ref_strr_b", "ntf_strr_b2"], min_count=1)
def s9_result(env): return H._stage_has_server(env, 9, "ecommerce", tool="get_order") and H._stage_has_server(env, 9, "notification_hub") and H._thread_block_has_terms(H.files_text(env, ["decision", "tracker", "risk"]) + "\n" + H._agent_response(env, 9), THREAD_IDS[1], ["additional evidence", "unboxing video", "usage marks", "platform intervention", "deadline", "burden of proof"], min_count=3, window=320) and bool(H._backend_refund_status_is(env, "ord_strr_0002", "ref_strr_b", "rejected"))
CHECKS = guard_stage_checks(9, [("s9_servers", s9_servers, 0.5), ("s9_args", s9_args, 0.5), ("s9_result", s9_result, 2.5)])
