from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS
def s7_servers(env): return H._stage_servers_correct(env, 7, min_count=1)
def s7_args(env): return H._stage_tool_args_reference(env, 7, ["lst_strr_0001", "usr_yan_ting", "ntf_strr_buyer_20260621"], min_count=1)
def s7_result(env): return H._stage_has_server(env, 7, "listing_platform") and H._thread_block_has_terms(H.files_text(env, ["tracker", "decision", "gear"]) + "\n" + H._agent_response(env, 7), THREAD_IDS[2], ["buyer", "inquiry", "price negotiation", "in person", "platform escrow", "comparison"], min_count=2, window=320)
CHECKS = guard_stage_checks(7, [("s7_servers", s7_servers, 0.5), ("s7_args", s7_args, 0.5), ("s7_result", s7_result, 1.0)])
