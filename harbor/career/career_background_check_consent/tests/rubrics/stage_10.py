"""Stage 10: save an unsent calculation memo for HR."""
from __future__ import annotations
from ._helpers import count_value_hits, draft_to_recruiter_text, norm_num, text_has, used_tool

_HR_KEYS = ["yanmunet", "yihui", "Yanmu Network", "Yi Hui", "hr"]


def s10_demand_letter_drafted(env) -> bool:
    if not used_tool(env, "save_draft", stage=10, server="email"):
        return False
    raw = draft_to_recruiter_text(env, _HR_KEYS)
    corpus = norm_num(raw)
    if not corpus.strip() or not all(value in corpus for value in ("33500", "301500", "97000")):
        return False
    years = text_has(raw, [["eight", "8 years", "n=8"], ["additional", "notice", "n+1", "months"]])
    basis = text_has(raw, [["article40", "law-lcl-040-blpnlbptx"], ["article46", "law-lcl-046-dvyxmanqx"], ["article47", "law-lcl-047-7nfprxbbx"], ["article27", "art_lcl_reg_027"], ["judg-2025-q7m4v2c6t3knx", "severance monthly wages dispute"]])
    demand = text_has(raw, [["shortfall", "shortfall", "negotiate", "claim", "request"]])
    return years and basis and demand and count_value_hits(raw, [["301500"], ["97000"]]) == 2


CHECKS = [("s10_demand_letter_drafted", s10_demand_letter_drafted, 4.0)]
