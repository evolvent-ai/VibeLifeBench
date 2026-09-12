from ._helpers import trace_stage, text_stage, zoning_mutation_rechecked


def s06_rechecked_zoning_mutation(env) -> bool:
    mutation_servers = ["legal_search", "notification_hub"]
    return bool(mutation_servers) and trace_stage(env, 6) and zoning_mutation_rechecked(env)


CHECKS = [
    ("s06_rechecked_zoning_mutation", s06_rechecked_zoning_mutation, 1.6),
]
