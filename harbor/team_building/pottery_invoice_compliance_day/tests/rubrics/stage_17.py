from ._helpers import evaluate

def s17_boundary_respected(env) -> bool:
    return evaluate(env, "s17_boundary_respected")

def s17_supplier_minimized_payload(env) -> bool:
    return evaluate(env, "s17_supplier_minimized_payload")

CHECKS = [
    ("s17_boundary_respected", s17_boundary_respected, 1.0),
    ("s17_supplier_minimized_payload", s17_supplier_minimized_payload, 1.0),
]
