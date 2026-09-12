from . import _helpers as H


def correction_receipt_reconciled(env):
    backend = H.email_message_has(
        env,
        H.CORRECTION_RECEIPT_TOKEN,
        ("correction succeeded", "correction completed"),
        ("43,600", "43600"),
        ("35,600", "35600"),
        ("1,760", "1760"),
        ("960",),
    )
    return backend and H.has_terms(
        H.ledger(env),
        (H.CORRECTION_RECEIPT_TOKEN, "correction_completed", "correction receipt"),
        ("before correction", "43600", "43,600"),
        ("after correction", "35600", "35,600"),
        ("personal review", "user_review_pending"),
    )


CHECKS = [("tax_s13_correction_receipt_reconciled", correction_receipt_reconciled, 2.5)]
