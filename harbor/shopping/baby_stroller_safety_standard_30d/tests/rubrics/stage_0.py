from ._helpers import guard_stage_checks
from . import _helpers as H
def s0_servers(env): return H._stage_servers_correct(env, 0, min_count=3)
def s0_args(env): return H._stage_tool_args_reference(env, 0, ["ord_strr_0001", "ord_strr_0002", "usr_yan_ting", "card_strr_01"], min_count=2)
def s0_result(env): return H._stage_has_server(env, 0, "delivery_logistics") and H._stage_has_server(env, 0, "credit_card") and H._backend_tracking_numbers_present(env, ["sf6693520001cn", "ztostrr5520002cn"], "6693")
def s0_files(env): return H._files_nonempty(env, H.CORE_WORKSPACE_PATHS, min_count=3)
CHECKS = guard_stage_checks(0, [("s0_servers", s0_servers, 0.5), ("s0_args", s0_args, 1.0), ("s0_result", s0_result, 1.5), ("s0_files", s0_files, 0.5)])
