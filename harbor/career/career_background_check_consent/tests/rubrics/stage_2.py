"""Stage 2: calculate the trailing twelve-month wage basis."""
from __future__ import annotations
from ._helpers import derived_text, norm_num, salary_deposits_trailing12, used_tool


def s2_base_backend(env) -> bool:
    deposits = salary_deposits_trailing12(env)
    return used_tool(env, "list_transactions", stage=2, server="banking") and len(deposits) == 12 and sum(deposits) == 3350000 * 12 and s2_avg_salary_computed(env)


def s2_avg_salary_computed(env) -> bool:
    raw = derived_text(env)
    corpus = norm_num(raw)
    if not corpus.strip():
        return False
    dim_value = any(value.lower() in corpus.lower() for value in ("33500", "3.35w", "33.5k", "average 33500", "approximately 33500"))
    dim_avg = any(value in corpus.lower() for value in ("wages", "wages", "average", "pay", "pay", "average", "mean", "avg", "divide by 12", "/12"))
    dim_incl = any(value in corpus.lower() for value in ("bonus", "bonus", "bonus", "bonus", "allowance", "allowance", "subsidy", "gross", "take-home", "pre-tax wages", "income", "compensation", "including bonus", "including allowance", "salary", "salary", "salary", "bonus"))
    return dim_value and dim_avg and dim_incl


CHECKS = [("s2_base_backend", s2_base_backend, 1.5), ("s2_avg_salary_computed", s2_avg_salary_computed, 4.0)]
