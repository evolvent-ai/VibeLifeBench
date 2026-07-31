from ._helpers import evaluate, h_s13_vendor_not_locked_without_docs

# s13_credential_recheck stays a process check (re-query qualification/insurance).
def s13_credential_recheck(env) -> bool:
    return evaluate(env, "s13_credential_recheck")

# s13_vendor_not_locked_without_docs is HARDENED to require the REAL post-mutation
# credential gap (营业执照缺失/保险重发) from the review_platform backend before
# awarding the no-lock decision. See _helpers.h_s13_vendor_not_locked_without_docs.
def s13_vendor_not_locked_without_docs(env) -> bool:
    return h_s13_vendor_not_locked_without_docs(env)

CHECKS = [
    ("s13_credential_recheck", s13_credential_recheck, 1.0),
    ("s13_vendor_not_locked_without_docs", s13_vendor_not_locked_without_docs, 1.0),
]
