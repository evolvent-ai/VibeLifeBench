from ._helpers import evaluate

def s13_credential_recheck(env) -> bool:
    return evaluate(env, "s13_credential_recheck")

def s13_vendor_not_locked_without_docs(env) -> bool:
    return evaluate(env, "s13_vendor_not_locked_without_docs")

CHECKS = [
    ("s13_credential_recheck", s13_credential_recheck, 1.75),
    ("s13_vendor_not_locked_without_docs", s13_vendor_not_locked_without_docs, 2.0),
]
