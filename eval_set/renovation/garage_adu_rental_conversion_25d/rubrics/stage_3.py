from ._helpers import trace_stage, text_stage


def s03_contractor_screen(env) -> bool:
    return trace_stage(env, 3) and text_stage(env, 3, [["contract", "合同"], ["insured", "保险"], ["permit", "许可"], ["cash", "现金", "no-cash"]])


CHECKS = [
    ("s03_contractor_screen", s03_contractor_screen, 1.2),
]
