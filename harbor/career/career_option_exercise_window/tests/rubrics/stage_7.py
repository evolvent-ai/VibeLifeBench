from . import _helpers as H

def immutable_grant_terms_survive_quote_changes(env):
    return H.grant_sources_valid(env) and H.quote_is(env, "2026-06-01", 7430) and H.has_terms(H.ledger(env), ("G-2021-0427",), ("4000",), ("29.72",), ("quote change", "market", "reference_quote"), ("does not change", "fixed"))

CHECKS = [("opt_s07_immutable_grant_terms_survive_quote_changes", immutable_grant_terms_survive_quote_changes, 1.5)]
