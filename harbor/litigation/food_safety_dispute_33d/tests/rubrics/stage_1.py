"""Stage 1: official procedure, jurisdiction, and compensation rules."""
from __future__ import annotations
from ._helpers import _food_journal_text
from .cross_stage import d_tenfold_not_treble, d_knowing_purchase_ok, d_delivery_jurisdiction

def s1_reads_official_notice(env) -> bool:
    text = _food_journal_text(env)
    if not text: return False
    return (any(k in text for k in ("Pudong Court", "oa_pudong_court", "official guidance", "filing and litigation guidance")) and any(k in text for k in ("place of receipt", "place of performance")) and any(k in text for k in ("Shanghai Pudong", "Pudong Court", "Pudong")) and any(k in text for k in ("refund plus tenfold compensation", "tenfold compensation")) and any(k in text for k in ("Article 148", "Food Safety Law")) and "knowingly buying counterfeit goods" in text and any(k in text for k in ("does not affect", "still may claim compensation", "defense is invalid", "still compensable")))
CHECKS = [("s1_reads_official_notice", s1_reads_official_notice, 0.5), ("d_tenfold_not_treble_safety", d_tenfold_not_treble, 2), ("d_knowing_purchase_ok", d_knowing_purchase_ok, 1), ("d_delivery_jurisdiction", d_delivery_jurisdiction, 1)]

