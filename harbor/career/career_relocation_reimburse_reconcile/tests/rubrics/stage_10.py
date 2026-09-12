from __future__ import annotations
from ._helpers import derived_text, norm_num, count_value_hits, text_has

def s10_demand_letter_drafted(env) -> bool:
    raw = derived_text(env)
    corpus = norm_num(raw)
    if not corpus.strip():
        return False
    base = '33800' in corpus
    due = count_value_hits(raw, [['297800', '297,800']]) >= 1
    diff = count_value_hits(raw, [['97000', '97,000']]) >= 1
    basis = text_has(raw, [['Lawful', 'calculation', 'calculation-alternative-12', 'Labor Contract Law statute']])
    demand = text_has(raw, [['claim-alternative-13', 'negotiated-alternative-14', 'remaining-alternative-15', 'shortfall-alternative-16', 'request', 'litigation-alternative-17', 'demand']])
    return base and due and diff and basis and demand
CHECKS = [('s10_demand_letter_drafted', s10_demand_letter_drafted, 4.0)]
