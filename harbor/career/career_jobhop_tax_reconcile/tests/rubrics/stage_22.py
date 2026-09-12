from . import _helpers as H


def monthly_statement_verification_is_recorded(env):
    statement = H.email_message_has(env, H.STATEMENT_TOKEN, ("July 2026", "July 2026"), (H.REFUND_TX_ID,), ("846,500", "846500"))
    return statement and len(H.refund_transactions(env)) == 1 and H.has_terms(H.ledger(env), ("monthly statement", "account statement"), (H.STATEMENT_TOKEN,), (H.REFUND_TX_ID,), ("reviewed", "match", "variance"))


CHECKS = [("tax_s22_monthly_statement_verification_is_recorded", monthly_statement_verification_is_recorded, 1.0)]
