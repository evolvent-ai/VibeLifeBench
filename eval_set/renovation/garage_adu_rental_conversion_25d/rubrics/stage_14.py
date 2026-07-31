from ._helpers import trace_stage, text_stage


def s14_calendar_chain(env) -> bool:
    return trace_stage(env, 14) and text_stage(env, 14, [["permit", "许可"], ["inspection", "检查"], ["contractor", "承包"], ["compliance", "合规"]])


CHECKS = [
    ("s14_calendar_chain", s14_calendar_chain, 1.3),
]
