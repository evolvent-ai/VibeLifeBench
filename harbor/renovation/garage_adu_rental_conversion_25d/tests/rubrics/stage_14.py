from ._helpers import calendar_handoff_recorded, trace_stage, text_stage


def s14_calendar_chain(env) -> bool:
    return trace_stage(env, 14) and calendar_handoff_recorded(env)


CHECKS = [
    ("s14_calendar_chain", s14_calendar_chain, 1.3),
]
