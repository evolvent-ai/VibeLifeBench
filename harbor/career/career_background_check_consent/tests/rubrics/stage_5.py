"""Stage 5: reconcile the lawful amount, proposal and shortfall."""
from __future__ import annotations
from ._helpers import count_value_hits, derived_text, text_has


def s5_reconcile_diff(env) -> bool:
    raw = derived_text(env)
    return bool(raw.strip()) and count_value_hits(raw, [["301500", "30.15w", "30.1w"]]) >= 1 and count_value_hits(raw, [["204500", "20.45w", "20.4w"]]) >= 1 and count_value_hits(raw, [["97000", "9.7w", "9.7 w"]]) >= 1 and text_has(raw, [["shortfall", "difference", "shortfall", "underpaid", "amount due"]])


def s5_n_plus_one(env) -> bool:
    raw = derived_text(env)
    return bool(raw.strip()) and text_has(raw, [["article40", "law-lcl-040-blpnlbptx"], ["article46", "law-lcl-046-dvyxmanqx"], ["article47", "law-lcl-047-7nfprxbbx"], ["article27", "art_lcl_reg_027", "judg-2025-q7m4v2c6t3knx"], ["eight", "8 years", "n=8", "months", "months"], ["notice", "notice", "notice"], ["additional", "additional", "notice", "additional", "n+1"], ["months", "9 months", "301500", "30.15w"]])


CHECKS = [("s5_reconcile_diff", s5_reconcile_diff, 3.0), ("s5_n_plus_one", s5_n_plus_one, 2.5)]
