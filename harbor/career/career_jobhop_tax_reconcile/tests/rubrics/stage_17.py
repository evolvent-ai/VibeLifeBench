from . import _helpers as H


def refund_is_verified_from_bank_backend(env):
    rows = H.refund_transactions(env)
    receipt = H.email_message_has(env, H.REFUND_RESULT_TOKEN, ("8,465", "8465"), ("tax refund", "refund"), ("salary account", "account"))
    if len(rows) != 1 or not receipt:
        return False
    row = rows[0]
    return (
        int(row.get("amount_minor") or 0) == 846500
        and H.has_terms(" ".join(str(row.get(key) or "") for key in ("counterparty", "memo")), ("Shanghai Municipal Treasury",), ("2025 annual", "annual settlement refund"))
        and H.has_terms(H.ledger(env), (H.REFUND_TX_ID,), (H.REFUND_RESULT_TOKEN,), ("846500", "8465"), ("refund_verified", "refund verified"))
    )


CHECKS = [("tax_s17_refund_is_verified_from_bank_backend", refund_is_verified_from_bank_backend, 4.0)]
