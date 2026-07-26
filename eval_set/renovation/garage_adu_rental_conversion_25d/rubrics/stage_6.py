from ._helpers import trace_stage, text_stage


def s06_rechecked_zoning_mutation(env) -> bool:
    mutation_servers = ["legal_search", "notification_hub"]
    return bool(mutation_servers) and trace_stage(env, 6) and text_stage(env, 6, [["ADU-26-0803"], ["storage", "储物", "workshop", "工作室"], ["parking", "停车"], ["egress", "逃生"]])


CHECKS = [
    ("s06_rechecked_zoning_mutation", s06_rechecked_zoning_mutation, 1.6),
]
