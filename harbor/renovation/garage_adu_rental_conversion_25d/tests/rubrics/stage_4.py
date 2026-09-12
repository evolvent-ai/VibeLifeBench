from ._helpers import permit_checklist_recorded, trace_stage, text_stage


def s04_permit_checklist(env) -> bool:
    return trace_stage(env, 4) and permit_checklist_recorded(env)


CHECKS = [
    ("s04_permit_checklist", s04_permit_checklist, 1.4),
]
