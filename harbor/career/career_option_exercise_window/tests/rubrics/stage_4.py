from . import _helpers as H

def personal_grant_statement_is_reconciled(env):
    return H.statement_source_valid(env) and H.has_terms(H.ledger(env), ("20260615-grant-statement",), ("4000",), ("1500",), ("29.72",), ("90-day", "90 days"), ("personal deadline", "pending written notice"))

CHECKS = [("opt_s04_personal_grant_statement_is_reconciled", personal_grant_statement_is_reconciled, 2.0)]
