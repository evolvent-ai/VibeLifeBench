from ._helpers import evaluate

def s2_vendor_cross_source(env) -> bool:
    return evaluate(env, "s2_vendor_cross_source")

def s2_shortlist_has_invoice_fields(env) -> bool:
    return evaluate(env, "s2_shortlist_has_invoice_fields")

CHECKS = [
    ("s2_vendor_cross_source", s2_vendor_cross_source, 1.5),
    ("s2_shortlist_has_invoice_fields", s2_shortlist_has_invoice_fields, 1.5),
]
