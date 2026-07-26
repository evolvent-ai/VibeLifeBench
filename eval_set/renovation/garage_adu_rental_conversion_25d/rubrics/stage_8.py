from ._helpers import trace_stage, text_stage


def s08_bid_compare_code_scope(env) -> bool:
    return trace_stage(env, 8) and text_stage(env, 8, [["egress", "逃生"], ["alarm", "报警"], ["optional", "可选"], ["contract", "合同"]])


CHECKS = [
    ("s08_bid_compare_code_scope", s08_bid_compare_code_scope, 1.4),
]
