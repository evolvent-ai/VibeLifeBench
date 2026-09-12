from ._helpers import kickoff_dossier, trace_stage, text_stage


def s00_kickoff_scope(env) -> bool:
    return trace_stage(env, 0) and kickoff_dossier(env)


CHECKS = [
    ("s00_kickoff_scope", s00_kickoff_scope, 0.8),
]
