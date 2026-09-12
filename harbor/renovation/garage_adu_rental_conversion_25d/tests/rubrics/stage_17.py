from ._helpers import rough_inspection_recorded, trace_stage, text_stage


def s17_rough_inspection_scheduled(env) -> bool:
    return trace_stage(env, 17) and rough_inspection_recorded(env)


CHECKS = [
    ("s17_rough_inspection_scheduled", s17_rough_inspection_scheduled, 1.2),
]
