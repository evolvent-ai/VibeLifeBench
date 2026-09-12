"""Stage 1 checker — passport reminder notification."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _tool_called_in_stage,
    _ws,
    _any,
    _contains_all,
)


def s1_passport_issue_handled(env) -> bool:
    """Agent queried formal visa data and documented the short passport margin."""
    ok_tools = _tool_called_in_stage(env, 1, ["get_visa_application", "list_visa_applications", "check_entry_requirements"])  # real visa tools (were phantom get_passport_info/get_visa_info)
    tp = _ws(env, "/workspace/trip_plan.md")
    dl = _ws(env, "/workspace/decision_log.md")
    combined = (tp + "\n" + dl).lower()

    has_expiry = _any(combined, ["2026-05-30", "05-30", "May 30"])
    has_trip_end = _any(combined, ["2026-03-30", "03-30", "March 30"])
    has_margin = _any(combined, ["short margin", "limited margin", "short margin", "limited margin", "near expiry"])
    has_confirmation = (
        _any(combined, ["carrier", "operating airline", "operating airline", "airline"])
        and _any(combined, ["cbp", "official", "CBP", "official"])
        and _any(combined, ["confirm", "verify", "written confirmation", "verify", "confirm"])
    )
    has_contingency = _any(
        combined,
        ["renew passport", "replace passport", "new passport", "replace passport", "hold booking", "hold booking", "refundable", "refundable", "escalate"],
    )
    ok_text = has_expiry and has_trip_end and has_margin and has_confirmation and has_contingency
    ok = ok_tools and ok_text
    logger.info(
        f"s1_passport_issue_handled: tools={ok_tools} expiry={has_expiry} trip_end={has_trip_end} "
        f"margin={has_margin} confirmation={has_confirmation} contingency={has_contingency} -> {ok}"
    )
    return bool(ok)


CHECKS = [
    ("s1_passport_issue_handled", s1_passport_issue_handled, 1.75),
]
