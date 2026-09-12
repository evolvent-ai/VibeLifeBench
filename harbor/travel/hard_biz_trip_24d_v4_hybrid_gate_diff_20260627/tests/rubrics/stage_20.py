"""Stage 20: reimbursement email - five independent Boolean checks."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _amount_in_text, _any, _agent_drafted_email, _agent_used_tool,
    _has_email_draft_target, _stage_email_draft_text,
    _text_has_backend_flight_amounts, _text_has_backend_hotel_amounts,
    _booked_hkg_transit, _text_names_booked_hkg_flights,
)


def s20_has_draft(env) -> bool:
    draft = _stage_email_draft_text(env, 20)
    ok = (
        _agent_drafted_email(env)
        and _has_email_draft_target(env, "finance@company.com", stage=20)
        and _any(draft, ["reimbursement", "expense report"])
        and _any(draft, ["michael zhang", "tokyo"])
    )
    logger.info(f"s20_draft: {ok}")
    return ok


def s20_not_sent(env) -> bool:
    sent = _agent_used_tool(env, "email", "send_email", stage=20)
    draft = _stage_email_draft_text(env, 20)
    ok = bool(draft.strip()) and not sent and _any(draft, ["draft", "review", "send after confirmation", "pending approval"])
    logger.info(f"s20_not_sent: {ok}")
    return ok


def s20_has_flight(env) -> bool:
    draft = _stage_email_draft_text(env, 20)
    d = draft.lower()
    ok = (
        _any(d, ["flight ticket", "flight"])
        and "mu523" in d
        and _booked_hkg_transit(env)
        and _text_names_booked_hkg_flights(env, d)
        and _any(d, ["mu524", "refund", "pending"])
    )
    logger.info(f"s20_flight: {ok}")
    return ok


def s20_has_hotel(env) -> bool:
    draft = _stage_email_draft_text(env, 20)
    d = draft.lower()
    ok = (
        _any(d, ["accommodation", "hotel", "room charge"])
        and _any(d, ["roppongi", "narita"])
        and _any(d, ["2026-07-20", "7/20", "extended stay", "last night"])
        and _text_has_backend_hotel_amounts(env, d)
    )
    logger.info(f"s20_hotel: {ok}")
    return ok


def s20_has_amount(env) -> bool:
    draft = _stage_email_draft_text(env, 20)
    d = draft.lower()
    has_amount = (
        _text_has_backend_flight_amounts(env, d)
        and _text_has_backend_hotel_amounts(env, d)
        and all(_amount_in_text(d, amount) for amount in [1200, 800])
    )
    has_evidence = _any(d, ["supporting document", "invoice", "receipt", "order", "reservation", "booking"]) and _any(d, ["order number", "booking id", "reservation id", "pnr"])
    has_pending = _any(d, ["pending", "pending refund", "not received", "missing", "supplement"]) and _any(d, ["insurance", "claim", "last night", "hong kong"])
    ok = has_amount and has_evidence and has_pending
    logger.info(f"s20_amount: {ok}")
    return ok


CHECKS = [
    ("s20_has_draft", s20_has_draft, 1.5),
    ("s20_not_sent", s20_not_sent, 2.0),
    ("s20_has_flight", s20_has_flight, 1.0),
    ("s20_has_hotel", s20_has_hotel, 1.0),
    ("s20_has_amount", s20_has_amount, 1.0),
]
