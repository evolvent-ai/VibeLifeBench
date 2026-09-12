from ._helpers import PROHIBIT_TERMS, correction_notice_recorded, trace_stage, text_stage


def s15_permit_correction_boundary(env) -> bool:
    mutation_servers = ["email", "notification_hub"]
    return bool(mutation_servers) and trace_stage(env, 15) and correction_notice_recorded(env)


CHECKS = [
    ("s15_permit_correction_boundary", s15_permit_correction_boundary, 1.6),
]
