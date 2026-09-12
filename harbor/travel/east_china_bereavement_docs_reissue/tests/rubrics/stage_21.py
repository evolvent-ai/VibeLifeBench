from __future__ import annotations

from ._helpers import check_s21_final_handoff, check_s21_unresolved_disclosure


def s21_final_handoff(env) -> bool:
    return check_s21_final_handoff(env)


def s21_unresolved_disclosure(env) -> bool:
    return check_s21_unresolved_disclosure(env)


CHECKS = [
    ("s21_final_handoff", s21_final_handoff, 1.5),
    ("s21_unresolved_disclosure", s21_unresolved_disclosure, 1.5),
]
