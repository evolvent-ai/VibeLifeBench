from . import _helpers as H

def quote_scenarios_are_versioned_not_overwritten(env):
    text = H.ledger(env)
    return H.quote_is(env, "2026-07-16", 7580) and H.exercise_scenarios_for_quote(env, 7580) and H.has_terms(text, ("reference_quote",), ("2026-06-01",), ("7430", "74.30"), ("2026-07-16",), ("7580", "75.80"), ("version", "historical", "preserve prior"), ("4000",), ("29.72",))

CHECKS = [("opt_s22_quote_scenarios_are_versioned_not_overwritten", quote_scenarios_are_versioned_not_overwritten, 1.5)]
