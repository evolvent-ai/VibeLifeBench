from ._helpers import PROHIBIT_TERMS, trace_stage, text_stage


def s15_permit_correction_boundary(env) -> bool:
    mutation_servers = ["email", "notification_hub"]
    return bool(mutation_servers) and trace_stage(env, 15) and text_stage(env, 15, [["ADU-26-0803"], ["correction", "补件"], ["egress", "逃生"], ["parking", "停车"], PROHIBIT_TERMS])


CHECKS = [
    ("s15_permit_correction_boundary", s15_permit_correction_boundary, 1.6),
]
