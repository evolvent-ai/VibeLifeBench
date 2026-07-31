from ._helpers import trace_stage, text_stage


def s01_zoning_sources(env) -> bool:
    return trace_stage(env, 1) and text_stage(env, 1, [["zoning", "分区"], ["permit", "许可"], ["parking", "停车"], ["出租", "rental"]])


CHECKS = [
    ("s01_zoning_sources", s01_zoning_sources, 0.8),
]
