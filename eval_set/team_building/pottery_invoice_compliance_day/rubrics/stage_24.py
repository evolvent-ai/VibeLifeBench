from ._helpers import evaluate

def s24_final_archive(env) -> bool:
    return evaluate(env, "s24_final_archive")

def s24_vendor_review_or_draft(env) -> bool:
    return evaluate(env, "s24_vendor_review_or_draft")

CHECKS = [
    ("s24_final_archive", s24_final_archive, 1.0),
    ("s24_vendor_review_or_draft", s24_vendor_review_or_draft, 1.0),
]
