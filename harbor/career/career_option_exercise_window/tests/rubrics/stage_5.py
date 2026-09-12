from . import _helpers as H

def scenarios_are_recomputable_and_nonbinding(env):
    text = H.ledger(env)
    return H.quote_is(env, "2026-06-01", 7430) and H.exercise_scenarios_for_quote(env, 7430) and H.has_terms(text, ("full exercise",), ("partial exercise",), ("defer exercise", "do not exercise"), ("cash_required", "cash"), ("tax risk", "price risk"), ("authorization_pending", "user decision"))

CHECKS = [("opt_s05_scenarios_are_recomputable_and_nonbinding", scenarios_are_recomputable_and_nonbinding, 2.5)]
