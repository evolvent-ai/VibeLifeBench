"""Stage 16: prove the passport block changed from needs_action to verified readiness."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import _call, _tool_call_matches, workspace_file_content


def s16_heartbeat_file_updated(env) -> bool:
    email_checked = _tool_call_matches(
        env,
        "email",
        "search_emails",
        lambda a: "doc-pass-lf-20260616" in str(a.get("query") or "").casefold(),
        stage=16,
    )
    visa_checked = _tool_call_matches(
        env,
        "visa_and_advisory",
        "list_visa_applications",
        lambda a: str(a.get("user_id") or "") == "usr_chen_yu",
        stage=16,
    )
    detail_checked = _tool_call_matches(
        env,
        "visa_and_advisory",
        "get_visa_application",
        lambda a: str(a.get("application_id") or "").casefold() == "va-id-260601-lfang",
        stage=16,
    )
    detail = _call(env, "visa_and_advisory", "get_visa_application", application_id="VA-ID-260601-LFANG")
    backend = str(detail).casefold()
    risk = workspace_file_content(env, "/workspace/risk_register.md").casefold()
    heartbeat = workspace_file_content(env, "/workspace/HEARTBEAT.md").casefold()
    backend_ok = all(x in backend for x in ("va-id-260601-lfang", "ready_for_booking", "2036-06-14", "doc-pass-lf-20260616"))
    transition = all(x in risk for x in ("2026-12-03", "2036-06-14", "doc-pass-lf-20260616")) and any(
        x in risk for x in ("resolved", "verified", "resolved")
    )
    followup = "ga837" in heartbeat and "2026-06-22" in heartbeat and any(
        x in heartbeat for x in ("entry requirement", "re-check", "re-check")
    )
    result = bool(email_checked and visa_checked and detail_checked and backend_ok and transition and followup)
    logger.info("s16_passport_transition: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [("s16_heartbeat_file_updated", s16_heartbeat_file_updated, 1.5)]
