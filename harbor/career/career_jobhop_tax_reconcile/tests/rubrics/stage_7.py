from . import _helpers as H


def deadlines_are_separated(env):
    internal = H.email_message_has(env, "20260615-withholding-breakdown", ("June 18", "2026-06-18"))
    return internal and H.official_rule_backend_exists(env) and H.has_terms(
        H.ledger(env),
        ("June 18", "2026-06-18"),
        ("June 30", "2026-06-30"),
        ("internal response",),
        ("statutory", "annual settlement"),
        ("receipt", "pending"),
    )


CHECKS = [("tax_s07_deadlines_are_separated", deadlines_are_separated, 1.0)]
