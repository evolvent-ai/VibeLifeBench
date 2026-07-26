from ._helpers import trace_stage, text_stage


def s00_kickoff_scope(env) -> bool:
    return trace_stage(env, 0) and text_stage(env, 0, [["ADU"], ["240000", "24万"], ["permit", "许可"], ["parking", "停车"], ["rent", "出租"]])


CHECKS = [
    ("s00_kickoff_scope", s00_kickoff_scope, 0.8),
]
