"""Stage 0: kickoff and basic case facts."""
from __future__ import annotations
from ._helpers import _food_journal_text, _notion_page_text

def s0_grasps_facts(env) -> bool:
    text = _food_journal_text(env)
    if not text:
        return False
    groups = (("Global Select", "seller"), ("FreshChoice", "platform"), ("infant formula",), ("no Chinese label",), ("wellness tea", "tea substitute"), ("claim", "lower blood sugar", "lower blood pressure", "unlawful additive"), ("1880", "1,880"), ("680",), ("1200", "1,200"), ("medical treatment", "emergency treatment", "320"))
    return all(any(token.lower() in text.lower() for token in group) for group in groups)
CHECKS = [("s0_grasps_facts", s0_grasps_facts, 0.5)]

