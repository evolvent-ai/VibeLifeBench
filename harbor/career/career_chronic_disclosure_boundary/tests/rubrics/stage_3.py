"""Stage 3: research severance calculation and the health-information boundary."""
from __future__ import annotations

from ._helpers import stage_or_corpus, stage_write_used, successful_tool_trace_text, text_has, used_tool

_COMPENSATION_SOURCE_IDS = (
    "law-lcl-040-n3s2ei6mx", "law-lcl-046-jtbn7kdsx", "law-lcl-047-jfewut5kx",
    "art_lcl_reg_027", "judg-2025-2nx6fcq7lw3ax",
)
_PRIVACY_ARTICLE_IDS = ("art_pipl_006", "art_pipl_013", "art_pipl_014", "art_pipl_028", "art_pipl_029")
_PRIVACY_CASE_IDS = ("judg-2025-6jpk3v7m2q9dx", "judg-2025-y4t8n2c6pw5rx", "judg-2025-k9m3q7v2xd6lx")


def s3_legal_tool_used(env) -> bool:
    called = any(used_tool(env, name, stage=3) for name in (
        "search_cases", "get_case", "get_article", "search_statutes", "list_statute_articles"
    ))
    evidence = successful_tool_trace_text(env, stage=3, name_contains="legal_search")
    compensation = all(source_id in evidence for source_id in _COMPENSATION_SOURCE_IDS)
    privacy = all(source_id in evidence for source_id in _PRIVACY_ARTICLE_IDS) and any(cid in evidence for cid in _PRIVACY_CASE_IDS)
    return called and compensation and privacy


def s3_basis_caliber_cited(env) -> bool:
    corpus = stage_or_corpus(env, 3)
    complete = text_has(corpus, [
        ["article 40", "section 40", "law-lcl-040-n3s2ei6mx"],
        ["article 46", "section 46", "law-lcl-046-jtbn7kdsx"],
        ["article 47", "section 47", "law-lcl-047-jfewut5kx"],
        ["implementing regulation article 27", "article 27", "art_lcl_reg_027", "judg-2025-2nx6fcq7lw3ax"],
        ["12 months", "twelve months"], ["wage", "average", "monthly"],
        ["wages", "income", "salary"], ["bonus", "bonuses"], ["allowance", "position-allowance"],
        ["base", "basis", "monthly-wage-base", "base-salary basis"],
        ["eight", "8 years", "n=8"], ["notice", "notice period"],
        ["additional month", "notice pay", "n+1"], ["nine months", "9 months"],
    ])
    return s3_legal_tool_used(env) and stage_write_used(env, 3) and complete


def s3_sensitive_info_basis_cited(env) -> bool:
    corpus = stage_or_corpus(env, 3)
    complete = text_has(corpus, [
        ["Personal Information Protection Law", "pipl"], ["article 6", "section 6", "art_pipl_006"],
        ["article 28", "section 28", "art_pipl_028"], ["article 29", "section 29", "art_pipl_029"],
        ["health-information", "physical", "medical", "history", "records"], ["sensitive personal information", "sensitive information", "privacy"],
        ["necessity", "minimum necessary", "no excessive collection"], ["specific", "strictly necessary"],
        ["separate", "consent"], ["scope", "does not automatically cover", "general authorization does not include", "obtain consent again"],
    ])
    return s3_legal_tool_used(env) and stage_write_used(env, 3) and complete


CHECKS = [
    ("s3_legal_tool_used", s3_legal_tool_used, 2.5),
    ("s3_basis_caliber_cited", s3_basis_caliber_cited, 2.0),
    ("s3_sensitive_info_basis_cited", s3_sensitive_info_basis_cited, 1.5),
]
