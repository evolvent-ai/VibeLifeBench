from . import _helpers as H


def tax_ledger_initialized(env):
    text = H.ledger(env)
    rows = H.markdown_table_rows(text)
    required = {"source_id", "tax_year", "income_period", "income_category", "reported_amount", "withheld_tax", "withholding_gap", "filing_status", "evidence_object_id", "last_verified_stage", "next_action"}
    return bool(rows) and required <= set(rows[0]) and H.has_terms(text, ("2025",), ("pending", "pending review", "under_review", "source_pending"))


CHECKS = [("tax_s00_ledger_initialized", tax_ledger_initialized, 1.0)]
