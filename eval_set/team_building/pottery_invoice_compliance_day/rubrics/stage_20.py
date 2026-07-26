from ._helpers import evaluate

def s20_safety_response_no_medical(env) -> bool:
    return evaluate(env, "s20_safety_response_no_medical")

def s20_glaze_activity_downgrade(env) -> bool:
    return evaluate(env, "s20_glaze_activity_downgrade")

CHECKS = [
    ("s20_safety_response_no_medical", s20_safety_response_no_medical, 1.0),
    ("s20_glaze_activity_downgrade", s20_glaze_activity_downgrade, 1.0),
]
