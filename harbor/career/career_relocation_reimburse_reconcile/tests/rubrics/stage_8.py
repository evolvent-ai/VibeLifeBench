from __future__ import annotations
from ._helpers import derived_text, result_rows, successful_tool_results, text_has, used_tool

def s8_search_done(env) -> bool:
    if not used_tool(env, 'search_jobs', stage=8):
        return False
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    companies = ['meituan', 'xiaohongshu', 'zhipu ai', 'bilibili', 'alibaba', 'ant group', 'trip.com', 'dewu', 'netease', 'pinduoduo', 'jd.com', 'didi', 'ele.me', 'hellobike', 'minimax']
    jobs = [job for result in successful_tool_results(env, 'search_jobs', 8) for job in result_rows(result)]
    matching = [job for job in jobs if str(job.get('city') or '').casefold() == 'shanghai'
                and any(term in (str(job.get('category') or '') + str(job.get('title') or '')).casefold()
                        for term in ('backend', 'platform'))]
    return len(matching) >= 3 and sum(c in corpus.casefold() for c in companies) >= 3 and text_has(corpus, [['Shanghai']])
CHECKS = [('s8_search_done', s8_search_done, 2.5)]
