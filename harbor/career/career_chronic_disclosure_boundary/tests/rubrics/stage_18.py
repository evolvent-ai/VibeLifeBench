"""Stage 18: compare Meituan and Poizon offers on compensation, terms, stability, and growth."""
from __future__ import annotations

from ._helpers import derived_text, norm_num, stage_write_used, text_has, trace_result_text, used_tool


def _offers_read(env) -> bool:
    trace = trace_result_text(env, 18, "read_email")
    return used_tool(env, "read_email", stage=18) and text_has(trace, [["Meituan"], ["32000"], ["Poizon"], ["52000"]])


def s18_offer_compare(env) -> bool:
    if not _offers_read(env) or not stage_write_used(env, 18):
        return False
    corpus = derived_text(env)
    dims = text_has(corpus, [
        ["Meituan"], ["Poizon"], ["compensation", "total"], ["employment", "arrangement"],
        ["noncompete"], ["stable", "stability"], ["development", "growth", "technical", "career"],
        ["decide", "decision", "authority", "reference"],
    ])
    return dims and s18_meituan_offer_value(env)


def s18_meituan_offer_value(env) -> bool:
    corpus = derived_text(env)
    normalized = norm_num(corpus)
    meituan = all(value in normalized for value in ("32000", "512000")) and text_has(corpus, [["Meituan"], ["16-salary", "16 salary"], ["employed", "directly-employed", "employment"]])
    dewu = all(value in normalized for value in ("52000", "832000")) and text_has(corpus, [["Poizon"], ["16-salary", "16 salary"]])
    return _offers_read(env) and stage_write_used(env, 18) and meituan and dewu


CHECKS = [
    ("s18_offer_compare", s18_offer_compare, 2.5),
    ("s18_meituan_offer_value", s18_meituan_offer_value, 2.0),
]
