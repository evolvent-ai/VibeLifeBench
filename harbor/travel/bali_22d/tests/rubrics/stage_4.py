"""Stage 4: the live visa object and durable state must keep Liu Fang blocked."""
from __future__ import annotations

from .shared._helpers import _call, _tool_call_matches, workspace_file_content


def s4_indonesia_entry_rule_rechecked(env) -> bool:
    queried = _tool_call_matches(
        env,
        "visa_and_advisory",
        "check_entry_requirements",
        lambda a: str(a.get("nationality") or "").upper() == "CN" and str(a.get("destination") or "").upper() == "ID" and str(a.get("purpose") or "").casefold() == "tourism",
        stage=4,
    )
    apps_queried = _tool_call_matches(env, "visa_and_advisory", "list_visa_applications", lambda a: str(a.get("user_id") or "") == "usr_chen_yu", stage=4)
    detail_queried = _tool_call_matches(env, "visa_and_advisory", "get_visa_application", lambda a: str(a.get("application_id") or "").casefold() == "va-id-260601-lfang", stage=4)
    rule = _call(env, "visa_and_advisory", "check_entry_requirements", nationality="CN", destination="ID", purpose="tourism")
    detail = _call(env, "visa_and_advisory", "get_visa_application", application_id="VA-ID-260601-LFANG")
    backend = str(detail).casefold()
    return bool(queried and apps_queried and detail_queried and int(rule.get("passport_validity_months") or 0) == 6 and all(x in backend for x in ("va-id-260601-lfang", "needs_action", "2026-12-03", "5 months 11 days")))


def s4_passport_risk_record_is_date_specific(env) -> bool:
    text = workspace_file_content(env, "/workspace/risk_register.md").casefold()
    return all(x in text for x in ("2026-12-03", "2026-06-22")) and any(x in text for x in ("liu fang",)) and any(x in text for x in ("5 months 11 days", "511", "5  11 ")) and any(x in text for x in ("blocked", "not met")) and any(x in text for x in ("renew", "passport")) and any(x in text for x in ("owner",)) and any(x in text for x in ("next review", "next check"))


def s4_mother_flight_register_remains_blocked(env) -> bool:
    text = workspace_file_content(env, "/workspace/booking_register.md").casefold()
    return any(x in text for x in ("liu fang",)) and "2026-06-22" in text and "ga837" in text and any(x in text for x in ("blocked", "hold")) and any(x in text for x in ("not booked", "no booking")) and "va-id-260601-lfang" in text


CHECKS = [
    ("s4_indonesia_entry_rule_rechecked", s4_indonesia_entry_rule_rechecked, 1.0),
    ("s4_passport_risk_record_is_date_specific", s4_passport_risk_record_is_date_specific, 1.25),
    ("s4_mother_flight_register_remains_blocked", s4_mother_flight_register_remains_blocked, 0.75),
]
