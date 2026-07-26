from ._helpers import trace_stage, text_stage


def s17_rough_inspection_scheduled(env) -> bool:
    return trace_stage(env, 17) and text_stage(env, 17, [["inspection", "检查"], ["rough", "粗检"], ["egress", "逃生"], ["alarm", "报警"]])


CHECKS = [
    ("s17_rough_inspection_scheduled", s17_rough_inspection_scheduled, 1.2),
]
