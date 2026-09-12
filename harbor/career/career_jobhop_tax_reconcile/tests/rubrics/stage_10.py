from . import _helpers as H


def accepted_not_completed_is_preserved(env):
    text = H.ledger(env)
    backend = H.email_message_has(env, H.CORRECTION_CASE_TOKEN, ("accepted only", "accepted"), ("correction not completed", "not completed"))
    return backend and H.has_terms(text, (H.CORRECTION_CASE_TOKEN, "correction case accepted", "correction_accepted"), ("pending", "not completed")) and "correction accepted equals correction completed" not in H.norm(text)


CHECKS = [("tax_s10_accepted_not_completed_is_preserved", accepted_not_completed_is_preserved, 2.0)]
