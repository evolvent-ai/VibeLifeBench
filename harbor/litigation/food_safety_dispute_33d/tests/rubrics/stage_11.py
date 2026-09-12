"""Stage 11: rebuttal of the three defenses."""
from __future__ import annotations
from ._helpers import _food_journal_text, _notion_page_text
from .cross_stage import d_substantive_vs_flaw, d_health_claim_violation

def s11_rebut_three_defenses(env) -> bool:
    text = _food_journal_text(env)
    if not text: return False
    return (any(k in text for k in ("refund plus tenfold compensation", "tenfold compensation")) and any(k in text for k in ("not threefold", "not refund plus threefold compensation")) and any(k in text for k in ("Article 148", "case_f01", "case_f12")) and "knowingly buying counterfeit goods" in text and any(k in text for k in ("does not affect", "still compensable", "defense is invalid")) and any(k in text for k in ("case_f04", "Article 3", "food and drug sectors", "food sector")) and any(k in text for k in ("no Chinese label", "unlawful additive")) and any(k in text for k in ("substantive noncompliance", "not a labeling defect", "proviso does not apply")))

def s11_rebuttal_in_notion(env) -> bool:
    text = _notion_page_text(env, "cross-examination") or _notion_page_text(env, "food safety rights protection")
    return text is not None and any(k in text for k in ("cross-examination", "rebuttal", "defense", "refund plus tenfold compensation", "knowingly buying counterfeit goods", "label"))
CHECKS = [("s11_rebut_three_defenses", s11_rebut_three_defenses, 2), ("s11_rebuttal_in_notion", s11_rebuttal_in_notion, 0.5), ("d_substantive_vs_flaw", d_substantive_vs_flaw, 2), ("d_health_claim_violation", d_health_claim_violation, 0.5)]

