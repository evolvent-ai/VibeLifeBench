"""Stage 23: final archive - summary, unresolved items, evidence, and checklist."""
from __future__ import annotations

from loguru import logger

from ._helpers import (
    _any, _workspace_file_nonempty, _workspace_file_text, _notion_text,
    _text_has_backend_flight_amounts, _text_has_backend_hotel_amounts,
)


def _final_text(env) -> str:
    return (
        _workspace_file_text(env, "/workspace/final_summary.md") + "\n" +
        _workspace_file_text(env, "/workspace/evidence_log.md") + "\n" +
        _workspace_file_text(env, "/workspace/budget.md") + "\n" +
        _notion_text(env)
    ).lower()


def s23_file_exists(env) -> bool:
    final = _workspace_file_text(env, "/workspace/final_summary.md")
    notion = _notion_text(env)
    ok = _workspace_file_nonempty(env, "/workspace/final_summary.md") and len(final.strip()) > 120 and _any(notion.lower(), ["final", "archive", "retrospective"])
    logger.info(f"s23_file: {ok}")
    return ok


def s23_has_summary(env) -> bool:
    text = _final_text(env)
    ok = (
        _any(text, ["summary", "retrospective", "actual", "budget", "itinerary"])
        and all(x in text for x in ["flight", "accommodation", "insurance"])
        and _any(text, ["typhoon", "flight cancellation", "transit", "hong kong"])
        and _text_has_backend_flight_amounts(env, text)
        and _text_has_backend_hotel_amounts(env, text)
    )
    logger.info(f"s23_summary: {ok}")
    return ok


def s23_has_checklist(env) -> bool:
    text = _final_text(env)
    has_items = all(_any(text, [kw]) for kw in ["passport", "cash", "charger"])
    has_business_items = _any(text, ["suit", "business card", "business attire"]) and _any(text, ["insurance", "approval", "visa", "transit"])
    ok = _any(text, ["checklist", "reusable"]) and has_items and has_business_items
    logger.info(f"s23_checklist: {ok}")
    return ok


def s23_has_pending(env) -> bool:
    text = _final_text(env)
    has_refund = "mu524" in text and _any(text, ["refund", "pending", "not received", "3-5"])
    has_claim = _any(text, ["insurance", "claim"]) and _any(text, ["cancellation certificate", "fare difference", "extended stay", "submit"])
    has_receipts = _any(text, ["invoice", "supporting document", "receipt", "missing"]) and _any(text, ["last night", "hong kong", "hkg"])
    has_owner_or_next = _any(text, ["owner", "next step", "deadline", "follow-up", "to-do"])
    ok = has_refund and has_claim and has_receipts and has_owner_or_next
    logger.info(f"s23_pending: refund={has_refund} claim={has_claim} receipts={has_receipts} -> {ok}")
    return ok


def s23_has_reusable(env) -> bool:
    text = _final_text(env)
    ok = (
        _any(text, ["next time", "reusable", "template", "experience", "lesson", "future"])
        and _any(text, ["approval", "refundable", "non-refundable"])
        and _any(text, ["transit", "mct", "connection", "visa"])
        and _any(text, ["reconciliation", "bank", "refund", "fee", "ftf"])
    )
    logger.info(f"s23_reuse: {ok}")
    return ok


CHECKS = [
    ("s23_file_exists", s23_file_exists, 1.0),
    ("s23_has_summary", s23_has_summary, 1.0),
    ("s23_has_checklist", s23_has_checklist, 1.0),
    ("s23_has_pending", s23_has_pending, 1.0),
    ("s23_has_reusable", s23_has_reusable, 1.0),
]
