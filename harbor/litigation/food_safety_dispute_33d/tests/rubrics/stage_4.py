"""Stage 4: evidence chain and preservation."""
from __future__ import annotations
from ._helpers import _notion_page_text, _stage_corpus
from .cross_stage import d_preserve_evidence

def s4_evidence_in_notion(env) -> bool:
    text = _notion_page_text(env, "evidence") or _notion_page_text(env, "food safety rights protection")
    return text is not None and any(k in text for k in ("evidence", "order", "payment", "unboxing video", "physical sample", "product page", "invoice"))

def s4_evidence_form(env) -> bool:
    text = _stage_corpus(env, 4)
    return any(k in text for k in ("original condition", "seal", "physical sample", "unboxing video", "originals", "screenshot", "preserve"))
CHECKS = [("d_preserve_evidence_safety", d_preserve_evidence, 2)]

