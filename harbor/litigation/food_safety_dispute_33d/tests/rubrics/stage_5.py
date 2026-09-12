"""Stage 5: filing materials and defendant options."""
from __future__ import annotations
from ._helpers import _stage_corpus
from .cross_stage import d_fees, d_defendant_election

def s5_filing_checklist(env) -> bool:
    text = _stage_corpus(env, 5)
    checks = [any(k in text for k in ("complaint", "claims", "facts and grounds")), any(k in text for k in ("defendant", "Global Select", "FreshChoice", "producer", "platform")), any(k in text for k in ("Pudong", "court", "place of receipt", "jurisdiction")), any(k in text for k in ("litigation fee", "court acceptance fee", "prepay", "losing party")), any(k in text for k in ("testing", "submit for testing", "SQI", "expert examination"))]
    return sum(checks) >= 4

def s5_defendant_consideration(env) -> bool:
    text = _stage_corpus(env, 5)
    subjects = sum(any(k in text for k in group) for group in [["Global Select", "seller"], ["FreshChoice", "platform"], ["producer", "manufacturer"]]) >= 2
    return subjects and any(k in text for k in ("choose one", "choose", "whether to add", "consider", "option", "you decide"))
CHECKS = [("d_fees", d_fees, 0.5), ("d_defendant_election", d_defendant_election, 1)]
