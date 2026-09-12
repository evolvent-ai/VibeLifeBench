from . import _helpers as H

def equity_ledger_initialized(env):
    return H.table_has_data(H.ledger(env)) and H.has_terms(H.ledger(env), ("G-2021-0427",), ("evidence_pending", "scenario_review", "pending verification"))

CHECKS = [("opt_s00_equity_ledger_initialized", equity_ledger_initialized, 1.0)]
