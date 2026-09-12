from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS
def s3_servers(env): return H._stage_servers_correct(env, 3, min_count=2) and H._stage_server_order_ok(env, 3, ["ecommerce", "notification_hub"])
def s3_args(env): return H._stage_tool_args_reference(env, 3, ["ord_strr_0002", "ref_strr_b", "ntf_strr_b1"], min_count=1)
def s3_result(env):
    text = H.files_text(env, ["tracker", "risk", "decision"]) + "\n" + H._agent_response(env, 3)
    return H._stage_has_server(env, 3, "ecommerce", tool="get_order") and H._stage_has_server(env, 3, "notification_hub") and H._thread_block_has_terms(text, THREAD_IDS[1], ["return", "quality issue", "evidence", "deadline", "merchant response", "proof"], min_count=3, window=320) and bool(H._backend_refund_status_is(env, "ord_strr_0002", "ref_strr_b", "submitted"))
CHECKS = guard_stage_checks(3, [("s3_servers", s3_servers, 0.5), ("s3_args", s3_args, 1.0), ("s3_result", s3_result, 2.0)])
