from ._helpers import trace_stage, text_stage, zoning_notice_recorded


def s01_zoning_sources(env) -> bool:
    return trace_stage(env, 1) and zoning_notice_recorded(env)


CHECKS = [
    ("s01_zoning_sources", s01_zoning_sources, 0.8),
]
