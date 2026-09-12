from __future__ import annotations
from ._helpers import derived_text, text_has

def s18_offer_compare(env) -> bool:
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    both = text_has(corpus, [['Meituan'], ['Dewu']])
    dims = sum((1 for d in (['direct-employment', 'employment arrangement'], ['non-compete'], ['stability'], ['total package', 'salary', 'monthly salary']) if any((x in corpus for x in d))))
    defer = text_has(corpus, [['decided-alternative-52', 'your-alternative-53', 'decision-alternative-54', 'recommendation-alternative-55', 'reference', 'final-alternative-56', 'matter-alternative-57']])
    return both and dims >= 3 and defer

def s18_meituan_offer_value(env) -> bool:
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    from ._helpers import norm_num
    nb = norm_num(corpus)
    return '32000' in nb and text_has(corpus, [['16 salaries', 'salaries', 'direct-employment']])
CHECKS = [('s18_offer_compare', s18_offer_compare, 2.5), ('s18_meituan_offer_value', s18_meituan_offer_value, 2.0)]
