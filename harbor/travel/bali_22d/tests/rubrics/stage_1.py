"""Stage 1: verify live Zika/entry-rule checks and durable, person-specific risks."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import _agent_responses, _call, _tool_call_matches, workspace_file_content


def s1_zika_user_notified(env) -> bool:
    advisory_checked = _tool_call_matches(
        env,
        "visa_and_advisory",
        "get_advisory",
        lambda a: str(a.get("country_code") or "").upper() == "ID",
        stage=1,
    )
    advisory = _call(env, "visa_and_advisory", "get_advisory", country_code="ID")
    advisory_text = str(advisory).casefold()
    resp = _agent_responses(env, 1).casefold()
    risk = workspace_file_content(env, "/workspace/risk_register.md").casefold()

    backend_ok = all(x in advisory_text for x in ("zika", "pregnant", "microcephaly"))
    communicated = (
        "zika" in resp
        and any(x in resp for x in ("pregnan", " pregnancy", "pregnant traveler", "Meilin", "meilin"))
        and any(x in resp for x in ("microceph", "microcephaly", "birth defect", "birth defect", "birth defect"))
        and any(x in resp for x in ("doctor", "clinician", "doctor", "obstetric"))
        and any(x in resp for x in ("you decide", "you decide", "option", "option"))
    )
    durable = (
        "zika" in risk
        and any(x in risk for x in ("owner", "owner"))
        and any(x in risk for x in ("next review", "next check", "next check"))
        and any(x in risk for x in ("open", "monitor", "pending decision", "monitor"))
    )
    result = bool(advisory_checked and backend_ok and communicated and durable)
    logger.info("s1_zika_user_notified: {}", "PASS" if result else "FAIL")
    return result


def s1_passport_proactive_before_stage4(env) -> bool:
    rule_checked = _tool_call_matches(
        env,
        "visa_and_advisory",
        "check_entry_requirements",
        lambda a: str(a.get("nationality") or "").upper() == "CN"
        and str(a.get("destination") or "").upper() == "ID"
        and str(a.get("purpose") or "").casefold() == "tourism",
        stage=1,
    )
    rule = _call(
        env,
        "visa_and_advisory",
        "check_entry_requirements",
        nationality="CN",
        destination="ID",
        purpose="tourism",
    )
    risk = workspace_file_content(env, "/workspace/risk_register.md").casefold()
    person_specific = any(x in risk for x in ("liu fang",))
    dates = "2026-12-03" in risk and "2026-06-22" in risk
    rule_specific = int(rule.get("passport_validity_months") or 0) == 6 and any(
        x in risk for x in ("6 months", "6 ", "5 months 11 days", "511")
    )
    blocked = any(x in risk for x in ("blocked", "not book", "not booked", "blocked", "booking paused"))
    owned = any(x in risk for x in ("owner", "owner")) and any(
        x in risk for x in ("renew", "renew", "passport")
    )
    result = bool(rule_checked and person_specific and dates and rule_specific and blocked and owned)
    logger.info("s1_passport_proactive: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [
    ("s1_zika_user_notified", s1_zika_user_notified, 4.0),
    ("s1_passport_proactive_before_stage4", s1_passport_proactive_before_stage4, 3.5),
]
