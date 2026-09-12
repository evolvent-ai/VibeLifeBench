from ._helpers import bid_comparison_recorded, trace_stage, text_stage


def s08_bid_compare_code_scope(env) -> bool:
    return trace_stage(env, 8) and bid_comparison_recorded(env)


CHECKS = [
    ("s08_bid_compare_code_scope", s08_bid_compare_code_scope, 1.4),
]
