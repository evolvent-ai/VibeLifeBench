from ._helpers import guard_stage_checks
from . import _helpers as H
def s1_servers(env): return H._stage_servers_correct(env, 1, min_count=3)
def s1_args(env): return H._stage_tool_args_reference(env, 1, ["ord_strr_0001", "ord_strr_0002", "card_strr_01", "lst_strr_0001"], min_count=2)
def s1_result(env): return H._backend_tracking_numbers_present(env, ["sf6693520001cn", "ztostrr5520002cn"], "6693")
CHECKS = guard_stage_checks(1, [("s1_servers", s1_servers, 0.5), ("s1_args", s1_args, 0.5), ("s1_result", s1_result, 1.0)])
