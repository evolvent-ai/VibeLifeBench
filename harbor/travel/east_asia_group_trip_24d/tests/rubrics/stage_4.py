"""Stage 4 gate: budget splits, units, and resistance to lazy advice."""
from __future__ import annotations
import re

from loguru import logger

from ._helpers import (
    _workspace_file_text,
    _any,
    _number_count,
    _has_bad_advice,
    _stage_corpus,
    _count_any,
)


def s4_gate(env) -> bool:
    """Require categories, correct 3/4 traveler denominators, units, and minor-unit amounts."""

    budget = _workspace_file_text(env, "/workspace/budget.md").lower()
    corpus = _stage_corpus(env, 4)
    combined = budget or corpus

    # budget.md is non-empty, estimated, and itemized.
    budget_nonempty = bool(budget.strip())
    has_estimated = _any(combined, ["estimated", "budget", "estimate"])
    category_count = _count_any(combined, [
        "lodging", "intercity", "flight", "local", "meals", "visa", "contingency",
        "transport", "hotel", "airfare",
    ])
    category_ok = category_count >= 4

    # Split counts must be durable in budget.md.
    has_seoul_3 = (
        _any(budget, ["seoul 3", "seoul segment 3", "seoul_split_count=3"])
        or (_any(budget, ["seoul"]) and _any(budget, ["3 travelers", "3 people", "3-person"]))
    )
    has_tokyo_4 = (
        _any(budget, ["tokyo 4", "tokyo segment 4", "tokyo_split_count=4"])
        or (_any(budget, ["tokyo"]) and _any(budget, ["4 travelers", "4 people", "4-person"]))
    )
    aa_ok = has_seoul_3 and has_tokyo_4

    # Amount units must be explicit and consistent.
    unit_ok = (
        _any(budget, ["cny", "rmb", "¥", "amount_minor"])
        or _number_count(budget) >= 4
    )
    # Detect a bare minor-unit label with no currency context.
    only_fen = "fen" in budget and "cny" not in budget and "rmb" not in budget
    if only_fen:
        unit_ok = False

    # Include several large amount_minor values, not just category labels.
    big_nums = [int(n) for n in re.findall(r'\d+', budget) if len(n) >= 5 and int(n) >= 10000]
    has_fen_amounts = len(big_nums) >= 2

    # Reject lazy advice while requiring structured output.
    no_lazy = not _has_bad_advice(corpus, [
        "roughly estimate", "good enough", "no need for detail", "whatever", "later",
    ])
    has_structure = category_ok or _number_count(budget) >= 4

    ok = (budget_nonempty and has_estimated and category_ok and aa_ok
          and unit_ok and has_fen_amounts and no_lazy and has_structure)
    logger.info(
        f"s4_gate: budget={budget_nonempty} estimated={has_estimated} cats={category_count}({category_ok}) "
        f"aa={aa_ok} unit={unit_ok} fen_amounts={has_fen_amounts}(n={len(big_nums)}) "
        f"no_lazy={no_lazy} structure={has_structure} → {'PASS' if ok else 'FAIL'}"
    )
    return ok


CHECKS = [("s4_gate", s4_gate, 2.5)]
