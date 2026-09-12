from __future__ import annotations
from ._helpers import derived_text, norm_num, count_value_hits, text_has

def s5_reconcile_diff(env) -> bool:
    raw = derived_text(env)
    corpus = norm_num(raw)
    if not corpus.strip():
        return False
    legal_due = count_value_hits(raw, [['297800', '297,800', '297.8 thousand']]) >= 1
    diff = count_value_hits(raw, [['97000', '97,000', '97 thousand']]) >= 1
    diff_sem = text_has(raw, [['shortfall', 'calculated', 'difference', 'remaining', 'low', 'depressed', 'amount']])
    return legal_due and diff and diff_sem

def s5_n_plus_one(env) -> bool:
    raw = derived_text(env)
    if not raw.strip():
        return False
    return text_has(raw, [['item-by-item total', 'statement line items', 'line-item reconciliation', 'actual amount', 'calculate each item', 'reconciliation details']])
CHECKS = [('s5_reconcile_diff', s5_reconcile_diff, 3.0), ('s5_n_plus_one', s5_n_plus_one, 2.5)]
