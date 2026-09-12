from __future__ import annotations

from ._helpers import (derived_text, get_article, get_case, result_rows,
                       successful_tool_results, text_has, used_tool)


def s3_legal_tool_used(env) -> bool:
    searched = used_tool(env, 'search_cases', stage=3)
    read_case = used_tool(env, 'get_case', stage=3, arg_substr='case_012')
    read_article = used_tool(env, 'get_article', stage=3, arg_substr='art_lcl_047')
    found = any(str(case.get('case_id') or '') == 'case_012'
                for result in successful_tool_results(env, 'search_cases', 3)
                for case in result_rows(result))
    return searched and read_case and read_article and found and s3_basis_caliber_cited(env)


def s3_basis_caliber_cited(env) -> bool:
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    backend_ok = get_article(env, 'art_lcl_047') is not None and get_case(env, 'case_012') is not None
    return backend_ok and text_has(corpus, [
        ['art_lcl_047'], ['case_012'], ['months', 'twelve-months', '12-month'],
        ['wage', 'average', 'salary'], ['bonus', 'allowance', 'including'],
    ])


CHECKS = [('s3_legal_tool_used', s3_legal_tool_used, 2.5), ('s3_basis_caliber_cited', s3_basis_caliber_cited, 3.5)]
