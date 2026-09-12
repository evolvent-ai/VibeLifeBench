from __future__ import annotations

from ._helpers import (derived_text, has_exact_number, relocation_statement_total_minor,
                       salary_deposits_trailing12, text_has, used_tool)


def s2_base_backend(env) -> bool:
    banking = used_tool(env, 'list_transactions', stage=2, arg_substr='acct_gk_checking')
    statement = used_tool(env, 'get_statement', stage=2, arg_substr='stm_card_gk_main_anchor')
    return banking and statement and relocation_statement_total_minor(env, 2) == 29780000


def s2_avg_salary_computed(env) -> bool:
    raw = derived_text(env)
    if not raw.strip():
        return False
    deposits = salary_deposits_trailing12(env, stage=2)
    if len(deposits) != 12 or sum(deposits) % 12:
        return False
    average_minor = sum(deposits) // 12
    return average_minor == 3380000 and has_exact_number(raw, 33800) and text_has(
        raw, [['average', 'monthly', 'mean', 'avg'], ['bonus', 'allowance', 'including']]
    )


CHECKS = [('s2_base_backend', s2_base_backend, 1.5), ('s2_avg_salary_computed', s2_avg_salary_computed, 4.0)]
