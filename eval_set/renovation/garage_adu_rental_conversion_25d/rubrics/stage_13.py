from ._helpers import trace_stage, text_stage


def s13_utility_height_light_updated(env) -> bool:
    return trace_stage(env, 13) and text_stage(env, 13, [["height", "层高"], ["light", "采光"], ["ventilation", "通风"], ["utility", "管线"]])


CHECKS = [
    ("s13_utility_height_light_updated", s13_utility_height_light_updated, 1.2),
]
