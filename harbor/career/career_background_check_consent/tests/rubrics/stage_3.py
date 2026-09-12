"""Stage 3: cite severance and health-information authorities."""
from __future__ import annotations
from ._helpers import stage_or_corpus, successful_tool_trace_text, text_has, used_tool

_COMPENSATION_SOURCE_IDS = ("law-lcl-040-blpnlbptx", "law-lcl-046-dvyxmanqx", "law-lcl-047-7nfprxbbx", "art_lcl_reg_027", "judg-2025-q7m4v2c6t3knx")
_PRIVACY_ARTICLE_IDS = ("art_pipl_006", "art_pipl_013", "art_pipl_014", "art_pipl_028", "art_pipl_029")
_PRIVACY_CASE_IDS = ("judg-2025-r5p2w7d4h6jsx", "judg-2025-t6n3y5f2k7qmx", "judg-2025-v4c7r2m6p5ldx")


def s3_legal_tool_used(env) -> bool:
    called = any(used_tool(env, tool, stage=3, server="legal_search") for tool in ("search_cases", "get_case", "get_article", "search_statutes", "list_statute_articles"))
    evidence = successful_tool_trace_text(env, stage=3, name_contains="legal_search")
    return called and all(value in evidence for value in _COMPENSATION_SOURCE_IDS) and all(value in evidence for value in _PRIVACY_ARTICLE_IDS) and any(value in evidence for value in _PRIVACY_CASE_IDS)


def s3_basis_caliber_cited(env) -> bool:
    corpus = stage_or_corpus(env, 3)
    if text_has(corpus, [["only base salary", "use base salary", "only fixed salary"]]) and not text_has(corpus, [["salary", "salary", "salary", "salary"]]):
        return False
    return text_has(corpus, [["Labor Contract Law article40", "article40", "law-lcl-040-blpnlbptx"], ["Labor Contract Law article46", "article46", "law-lcl-046-dvyxmanqx"], ["Labor Contract Law article47", "article47", "law-lcl-047-7nfprxbbx"], ["Regulation article27", "article27", "art_lcl_reg_027", "judg-2025-q7m4v2c6t3knx"], ["months", "months", "months"], ["wages", "average", "average", "mean"], ["wages", "gross wages", "income"], ["bonus", "bonus"], ["allowance", "subsidy"], ["salary", "salary", "salary", "salary"], ["eight", "8 years", "n=8", "wages"], ["notice", "notice", "notice", "notice"], ["additional", "additional", "notice", "additional", "+1", "n+1"], ["months", "9 months", "months total"]])


def s3_sensitive_info_basis_cited(env) -> bool:
    corpus = stage_or_corpus(env, 3)
    return text_has(corpus, [["Personal Information Protection Law", "pipl", "stat_pipl"], ["art_pipl_006", "pipl6", "section 6"], ["art_pipl_028", "pipl28", "section 28"], ["art_pipl_029", "pipl29", "section 29"], ["health", "examination", "medical", "medical"], ["sensitive", "sensitive"], ["purpose", "purpose", "necessity", "scope", "collection"], ["purpose", "necessary"], ["consent"], ["automatic", "cover", "records", "authorization", "consent", "authorization scope", "purpose", "scope"]])


CHECKS = [("s3_legal_tool_used", s3_legal_tool_used, 2.5), ("s3_basis_caliber_cited", s3_basis_caliber_cited, 2.0), ("s3_sensitive_info_basis_cited", s3_sensitive_info_basis_cited, 1.5)]
