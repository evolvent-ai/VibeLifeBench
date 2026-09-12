from . import _helpers as H

def grant_terms_are_source_traceable(env):
    text = H.ledger(env)
    return H.grant_sources_valid(env) and H.has_terms(text, ("G-2021-0427",), ("20210427-grant",), ("20250427-vesting",), ("4000",), ("1500",), ("29.72",), ("deadline", "pending", "pending written notice"))

CHECKS = [("opt_s01_grant_terms_are_source_traceable", grant_terms_are_source_traceable, 2.5)]
