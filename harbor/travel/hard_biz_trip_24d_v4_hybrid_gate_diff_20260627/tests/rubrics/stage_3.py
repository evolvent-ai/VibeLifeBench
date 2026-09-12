"""Stage 3: initialize exact budget lines, currencies, states, and funding split."""
from __future__ import annotations

from loguru import logger

from ._helpers import _amount_in_text, _any, _workspace_file_text


def s3_budget_file(env) -> bool:
    """budget.md must carry the exact initial ceiling and major budget lines."""
    text = _workspace_file_text(env, "/workspace/budget.md").lower()
    required_numbers = all(
        _amount_in_text(text, amount)
        for amount in [20000, 6000, 7000, 1200, 800, 5000]
    )
    has_categories = all(x in text for x in ["flight", "accommodation", "insurance"])
    ok = bool(text.strip()) and required_numbers and has_categories
    logger.info(f"s3_budget_file: numbers={required_numbers} categories={has_categories} -> {ok}")
    return ok


def s3_currency_split(env) -> bool:
    """Budget must split CNY and JPY and carry lifecycle states."""
    text = _workspace_file_text(env, "/workspace/budget.md").lower()
    has_cny = _any(text, ["cny"])
    has_jpy = _any(text, ["jpy"])
    has_status = all(s in text for s in ["estimated", "actual", "settled"]) and _any(
        text, ["pending refund", "pending"]
    )
    ok = has_cny and has_jpy and has_status
    logger.info(f"s3_currency_split: cny={has_cny} jpy={has_jpy} status={has_status} -> {ok}")
    return ok


def s3_reimburse_split(env) -> bool:
    """Budget distinguishes reimbursable company items from personal items."""
    text = _workspace_file_text(env, "/workspace/budget.md").lower()
    has_company = _any(text, ["reimbursable", "company"]) and all(x in text for x in ["flight", "accommodation", "registration", "insurance"])
    has_personal = _any(text, ["self-funded", "personal"]) and _any(text, ["meals", "transportation"])
    ok = has_company and has_personal
    logger.info(f"s3_reimburse_split: company={has_company} personal={has_personal} -> {ok}")
    return ok


CHECKS = [
    ("s3_budget_file", s3_budget_file, 1.5),
    ("s3_currency_split", s3_currency_split, 1.0),
    ("s3_reimburse_split", s3_reimburse_split, 1.0),
]
