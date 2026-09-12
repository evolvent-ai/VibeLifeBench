from . import _helpers as H

def cash_review_preserves_protected_funds(env):
    return H.cash_snapshot_recorded(env) and H.has_terms(H.ledger(env), ("cash_required", "exercise cost"), ("emergency fund", "must not be used", "protected"), ("shortfall 0", "gap 0", "no shortfall"), ("do not transfer", "do not borrow", "user decision"))

CHECKS = [("opt_s23_cash_review_preserves_protected_funds", cash_review_preserves_protected_funds, 2.0)]
