from . import _helpers as H


def variance_table_is_recomputable(env):
    text = H.ledger(env)
    source_ok = H.email_message_has(env, "20260615-withholding-breakdown", ("43,600", "43600"), ("1,760", "1760"))
    return source_ok and H.variance_table_recomputes_april(text)


CHECKS = [("tax_s05_variance_table_is_recomputable", variance_table_is_recomputable, 2.5)]
