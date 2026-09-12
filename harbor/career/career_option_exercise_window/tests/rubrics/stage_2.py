from . import _helpers as H

def valuation_cost_and_holdings_are_distinguished(env):
    text = H.ledger(env)
    return (
        H.quote_is(env, "2026-06-01", 7430)
        and H.grant_is_not_brokerage_holding(env)
        and H.full_valuation_recorded(env, 7430)
        and H.has_terms(text, ("reference_quote", "quote"), ("cash_required", "exercise cost"), ("tax_scenario", "tax"), ("not exercised", "not a holding", "not yet held", "not a brokerage holding", "does not mean shares were exercised or are held", "shares remain unexercised and absent from brokerage positions"))
    )

CHECKS = [("opt_s02_valuation_cost_and_holdings_are_distinguished", valuation_cost_and_holdings_are_distinguished, 2.5)]
