"""Stage 18: compare offers and defer the final decision."""
from __future__ import annotations
from ._helpers import derived_text, norm_num, successful_tool_trace_text, text_has, used_tool


def _offer_read(env) -> bool:
    if not used_tool(env, "read_email", stage=18, server="email"):
        return False
    evidence = successful_tool_trace_text(env, stage=18, name_contains="read_email")
    return text_has(evidence, [["Meituan"], ["32000"], ["16 salary", "16-salary", "annual 16 pay"], ["direct"]])


def s18_offer_compare(env) -> bool:
    if not _offer_read(env):
        return False
    corpus = derived_text(env)
    dimensions = sum(1 for group in (("direct", "arrangement"), ("noncompete",), ("stability",), ("compensation", "salary", "monthly pay"), ("development", "platform")) if any(value in corpus for value in group))
    return text_has(corpus, [["Meituan"], ["Dewu"]]) and dimensions >= 4 and text_has(corpus, [["you decide", "your choice", "reference", "decision"]])


def s18_meituan_offer_value(env) -> bool:
    if not _offer_read(env):
        return False
    corpus = derived_text(env)
    return "32000" in norm_num(corpus) and text_has(corpus, [["16 salary", "16-salary", "annual 16 pay"], ["direct"]])


CHECKS = [("s18_offer_compare", s18_offer_compare, 2.5), ("s18_meituan_offer_value", s18_meituan_offer_value, 2.0)]
