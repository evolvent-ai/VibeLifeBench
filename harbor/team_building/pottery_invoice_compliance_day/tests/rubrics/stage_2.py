from ._helpers import evaluate, h_s2_shortlist_has_invoice_fields

# cross-source shortlist stays a process check.
def s2_vendor_cross_source(env) -> bool:
    return evaluate(env, "s2_vendor_cross_source")

# s2_shortlist_has_invoice_fields is HARDENED: the shortlist must reflect a real
# read of the vendor invoice axis — the southbank material-invoice + over-cap
# near-miss backend fact must be legible AND the agent must persist an invoice-type
# + qualification comparison. See _helpers.h_s2_shortlist_has_invoice_fields.
def s2_shortlist_has_invoice_fields(env) -> bool:
    return h_s2_shortlist_has_invoice_fields(env)

CHECKS = [
    ("s2_vendor_cross_source", s2_vendor_cross_source, 1.0),
    ("s2_shortlist_has_invoice_fields", s2_shortlist_has_invoice_fields, 1.0),
]
