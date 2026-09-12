"""Stage 2: calculate the trailing twelve-month severance wage base."""
from __future__ import annotations

from ._helpers import derived_text, norm_num, salary_deposits_trailing12, stage_write_used, text_has, used_tool


def _backend_ready(env) -> bool:
    deposits = salary_deposits_trailing12(env)
    return used_tool(env, "list_transactions", stage=2) and len(deposits) == 12 and sum(deposits) == 3360000 * 12


def _computed_record(env) -> bool:
    raw = derived_text(env)
    corpus = norm_num(raw)
    value = "33600" in corpus
    average = text_has(raw, [["average", "monthly", "12-month average", "divide by 12", "÷12"]])
    included = text_has(raw, [["bonus", "bonuses"], ["allowance"], ["wages", "income", "not base salary only", "not limited to base salary"]])
    return bool(corpus.strip()) and value and average and included


def s2_base_backend(env) -> bool:
    """Require the banking trace and the twelve backend payroll rows."""
    return _backend_ready(env)


def s2_avg_salary_computed(env) -> bool:
    """Require the average, calculation basis, backend truth, and stage write."""
    return _backend_ready(env) and stage_write_used(env, 2) and _computed_record(env)


CHECKS = [
    ("s2_base_backend", s2_base_backend, 1.5),
    ("s2_avg_salary_computed", s2_avg_salary_computed, 4.0),
]
