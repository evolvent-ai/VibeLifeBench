from . import _helpers as H


def duplicate_month_evidence_logged(env):
    backend = H.email_message_has(
        env,
        "20260615-withholding-breakdown",
        ("April 2025", "April"),
        ("43,600", "43600"),
        ("35,600", "35600"),
        ("duplicate", "entered again"),
    )
    return backend and H.has_terms(
        H.ledger(env),
        ("20260615-withholding-breakdown",),
        ("2025-04", "April"),
        ("duplicate", "entered again"),
        ("43600", "43,600"),
        ("35600", "35,600"),
    )


CHECKS = [("tax_s04_duplicate_month_evidence_logged", duplicate_month_evidence_logged, 1.5)]
