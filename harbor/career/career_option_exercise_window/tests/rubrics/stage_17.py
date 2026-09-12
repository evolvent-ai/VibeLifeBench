from . import _helpers as H

def latest_market_close_drives_versioned_scenarios(env):
    text = H.ledger(env)
    return H.quote_is(env, "2026-07-16", 7580) and H.exercise_scenarios_for_quote(env, 7580) and H.has_terms(text, ("2026-07-16",), ("7580", "75.8"), ("full exercise",), ("partial exercise",), ("preserve prior", "version"))

CHECKS = [("opt_s17_latest_market_close_drives_versioned_scenarios", latest_market_close_drives_versioned_scenarios, 3.5)]
