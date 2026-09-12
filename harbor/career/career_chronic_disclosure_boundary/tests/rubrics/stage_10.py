"""Stage 10: draft the severance demand for user review."""
from __future__ import annotations
from ._helpers import count_value_hits, derived_text, norm_num, stage_write_used, text_has
def s10_demand_letter_drafted(env) -> bool:
    raw = derived_text(env); corpus = norm_num(raw)
    values = count_value_hits(raw, [["33600"], ["302400"], ["97000"]]) == 3
    tenure = text_has(raw, [["eight", "8 years", "n=8"], ["additional month", "payment in lieu of notice", "n+1"], ["months", "9 months"]])
    sources = text_has(raw, [["article 40", "law-lcl-040-n3s2ei6mx"], ["article 46", "law-lcl-046-jtbn7kdsx"], ["article 47", "law-lcl-047-jfewut5kx"], ["implementing regulation article 27", "art_lcl_reg_027"], ["judg-2025-2nx6fcq7lw3ax", "severance monthly wage case", "zhou v platform company"]])
    demand = text_has(raw, [["demand", "claim", "request"], ["difference", "remaining", "due"]])
    return stage_write_used(env, 10) and values and tenure and sources and demand
CHECKS = [("s10_demand_letter_drafted", s10_demand_letter_drafted, 4.0)]
