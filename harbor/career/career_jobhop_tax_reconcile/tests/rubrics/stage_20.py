from . import _helpers as H


def archive_reply_preserves_open_rights(env):
    facts = H.email_message(env, H.CORRECTION_RECEIPT_TOKEN) and len(H.refund_transactions(env)) == 1
    candidates = []
    for draft in H.routed_drafts(env, ("payroll.jitong@hanlandata.example",)):
        text = H.messages_corpus((draft,))
        if H.has_terms(text, ("archive", "archival", "for your records"), ("correction receipt", "receipt of correction"), ("refund credit", "refund deposit")):
            candidates.append(draft)
    if not facts or len(candidates) != 1:
        return False
    text = H.messages_corpus(candidates)
    return H.has_terms(text, ("open issue", "unresolved", "open_issue"), ("preserve rights", "rights are preserved", "reserve rights", "reserve my rights", "rights remain preserved")) and not H.asserts_any(text, ("waive rights", "confirm that all data is undisputed", "confirm all data is undisputed", "no objection to data"))


CHECKS = [("tax_s20_archive_reply_preserves_open_rights", archive_reply_preserves_open_rights, 2.0)]
