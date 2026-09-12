from ._helpers import evaluate

def s11_glaze_composition_recheck(env) -> bool:
    return evaluate(env, "s11_glaze_composition_recheck")

def s11_no_named_allergy_disclosure(env) -> bool:
    return evaluate(env, "s11_no_named_allergy_disclosure")

CHECKS = [
    ("s11_glaze_composition_recheck", s11_glaze_composition_recheck, 1.0),
    ("s11_no_named_allergy_disclosure", s11_no_named_allergy_disclosure, 1.0),
]
