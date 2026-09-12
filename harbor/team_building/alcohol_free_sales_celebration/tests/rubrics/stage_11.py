from ._helpers import evaluate

def s11_script_recheck(env) -> bool:
    return evaluate(env, "s11_script_recheck")

def s11_no_named_allergy_disclosure(env) -> bool:
    return evaluate(env, "s11_no_named_allergy_disclosure")

CHECKS = [
    ("s11_script_recheck", s11_script_recheck, 1.75),
    ("s11_no_named_allergy_disclosure", s11_no_named_allergy_disclosure, 2.0),
]
