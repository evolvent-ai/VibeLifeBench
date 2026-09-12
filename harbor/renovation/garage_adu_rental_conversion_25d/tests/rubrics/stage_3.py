from ._helpers import contractor_screen_recorded, trace_stage, text_stage


def s03_contractor_screen(env) -> bool:
    return trace_stage(env, 3) and contractor_screen_recorded(env)


CHECKS = [
    ("s03_contractor_screen", s03_contractor_screen, 1.2),
]
