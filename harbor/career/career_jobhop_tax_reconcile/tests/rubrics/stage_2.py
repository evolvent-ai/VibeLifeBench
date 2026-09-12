from . import _helpers as H


def bank_timeline_is_caveated(env):
    text = H.ledger(env)
    return (
        H.wage_timeline_backend_complete(env)
        and H.wage_timeline_is_itemized(env, text)
        and H.has_terms(text, ("salary", "bonus", "departure settlement"), ("net bank credit", "reconciliation clue", "not taxable income"))
    )


CHECKS = [("tax_s02_bank_timeline_is_caveated", bank_timeline_is_caveated, 2.0)]
