from . import _helpers as H

def official_equity_tax_rules_are_recorded(env):
    text = H.ledger(env)
    return H.official_policy_source(env) and H.has_terms(text, ("Ministry of Finance", "State Taxation Administration", "equity incentive"), ("individual income tax",), ("stat_xm_incentive_extension", "art_xm_extension"), ("applicability limits", "does not mean an extended window"))

CHECKS = [("opt_s03_official_equity_tax_rules_are_recorded", official_equity_tax_rules_are_recorded, 2.0)]
