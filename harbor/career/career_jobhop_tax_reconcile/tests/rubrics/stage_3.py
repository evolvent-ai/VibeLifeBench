from . import _helpers as H


def official_tax_rule_recorded(env):
    text = H.ledger(env)
    return H.official_rule_backend_exists(env) and H.has_terms(
        text,
        (H.OFFICIAL_RULE_ID, "annual comprehensive income tax settlement administration", "Order No. 57"),
        (H.OFFICIAL_RULE_ARTICLE_ID, "record retention", " correction"),
        ("filing deadline", "June 30"),
    )


CHECKS = [("tax_s03_official_tax_rule_recorded", official_tax_rule_recorded, 2.0)]
