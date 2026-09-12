from . import _helpers as H


def source_documents_itemized(env):
    text = H.ledger(env)
    source_ids = (
        "20260608-annual-settlement",
        "20260118-old-employer-withholding",
        "20250905-deduction-switch",
    )
    return all(H.email_message(env, token) for token in source_ids) and H.source_rows_are_itemized(text, source_ids)


CHECKS = [("tax_s01_source_documents_itemized", source_documents_itemized, 1.5)]
