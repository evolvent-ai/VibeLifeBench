from ._helpers import evaluate

def s5_vendor_qa_saved(env) -> bool:
    return evaluate(env, "s5_vendor_qa_saved")

def s5_safety_degrade_plan(env) -> bool:
    return evaluate(env, "s5_safety_degrade_plan")

CHECKS = [
    ("s5_vendor_qa_saved", s5_vendor_qa_saved, 1.0),
    ("s5_safety_degrade_plan", s5_safety_degrade_plan, 1.0),
]
