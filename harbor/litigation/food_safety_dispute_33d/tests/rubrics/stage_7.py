"""Stage 7: seller unreachability and platform advance compensation."""
from __future__ import annotations
from ._helpers import _notifications, _notion_page_text, _saved_cases, _stage_corpus

def s7_detects_seller_vanish(env) -> bool:
    return _notifications(env) is not None and any(k in _stage_corpus(env, 7) for k in ("unreachable", "store closure", "closed", "cannot contact", "delisted", "cannot find", "platform", "advance compensation"))

def s7_platform_advance_safety(env) -> bool:
    # The seller-risk notice and saved precedent are durable backend facts.  The
    # agent's conclusion must also be persisted in the platform-risk journal;
    # stage response wording is deliberately not used as the proof of the rule.
    notifications = _notifications(env)
    if notifications is None:
        return False
    seller_notice = any(
        str(item.get("notification_id") or "") == "ntf_food_s7_seller_vanish"
        for item in notifications
        if isinstance(item, dict)
    )
    saved = _saved_cases(env)
    if saved is None:
        return False
    authorities = []
    for row in saved:
        if not isinstance(row, dict) or str(row.get("case_id") or "") not in {"case_f05", "case_f14"}:
            continue
        case = row.get("case") if isinstance(row.get("case"), dict) else row
        authorities.append(" ".join(str(case.get(key) or "") for key in ("case_id", "title", "summary")))
    authority_text = " ".join(authorities).lower()
    has_authority = bool(authorities) and (
        "advance compensation" in authority_text
        or "joint and several liability" in authority_text
        or "first assume liability" in authority_text
    )
    journal = (_notion_page_text(env, "platform") or "").lower()
    has_rule = any(
        phrase in journal
        for phrase in (
            "advance compensation",
            "bear first",
            "claim against the platform",
            "platform compensation",
            "platform liable",
            "platform advance",
        )
    )
    return seller_notice and has_authority and has_rule
CHECKS = [("s7_platform_advance_safety", s7_platform_advance_safety, 2)]
