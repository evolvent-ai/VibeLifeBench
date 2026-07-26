from ._helpers import trace_stage, text_stage


def s04_permit_checklist(env) -> bool:
    return trace_stage(env, 4) and text_stage(env, 4, [["egress", "逃生"], ["alarm", "报警"], ["light", "采光"], ["ventilation", "通风"], ["parking", "停车"]])


CHECKS = [
    ("s04_permit_checklist", s04_permit_checklist, 1.4),
]
