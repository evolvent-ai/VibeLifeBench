"""Stage 4 rubric — eVisa portal passport block (D4)."""
from __future__ import annotations


from .shared._helpers import (
    _all_corpus,
    _all_calendar_events,
    _any_kw,
    _call,
    _cron_reminders,
    _list_visa_apps,
    _sent_emails_any,
)

from loguru import logger


def s4_passport_resolved(env) -> bool:
    """Passport-renewal path in motion (cron / notion / calendar)."""
    for r in _cron_reminders(env):
        if _any_kw(r.get("text") or "",
                   ["passport", "renewal", "renew"]):
            logger.info("s4 passport resolved: PASS via cron reminder")
            return True

    body = _all_corpus(env)
    if body and _any_kw(body, ["passport"]) and _any_kw(
        body, ["renew", "replan", "plan", "todo", "reissue", "urgent", "to-do"],
    ):
        logger.info("s4 passport resolved: PASS via notion plan")
        return True

    for e in _all_calendar_events(env) or []:
        s = str(e.get("summary") or "") + " " + str(e.get("description") or "")
        if _any_kw(s, ["passport", "renewal"]):
            logger.info("s4 passport resolved: PASS via calendar")
            return True

    logger.info("s4 passport resolved: FAIL")
    return False


def s4_visa_application_started(env) -> bool:
    """For father (and maybe Li Wei), at least one visa app in flight."""
    found_any = False
    for user_id in ("li_wei", "dad", "li_jianguo"):
        apps = _list_visa_apps(env, user_id)
        for a in apps:
            status = str(a.get("status") or "").lower()
            if status in ("draft", "submitted", "processing", "rfi", "approved"):
                logger.info(f"s4 visa app: PASS via {user_id} / {status}")
                return True
        if apps:
            found_any = True
    if not found_any:
        probe = _call(env, "visa_and_advisory", "list_visa_products",
                      nationality="CN", destination="JP")
        if probe is None:
            logger.info("s4 visa app: lenient pass — visa backend unreachable")
            return False
    logger.info("s4 visa app: FAIL — no application in flight")
    return False


def s4_passport_cross_service(env) -> bool:
    """Passport block triggered BOTH notion/cron todo AND email-or-calendar update."""
    channel_a = False
    body = _all_corpus(env)
    if body and _any_kw(body, ["passport"]):
        channel_a = True
    for r in _cron_reminders(env):
        if _any_kw(r.get("text") or "", ["passport", "renewal"]):
            channel_a = True
            break

    channel_b = False
    msgs = _sent_emails_any(env)
    for m in msgs:
        blob = str(m.get("subject") or "") + " " + str(m.get("body") or "")
        if _any_kw(blob, ["passport"]):
            channel_b = True
            break
    if not channel_b:
        for e in _all_calendar_events(env) or []:
            s = (str(e.get("summary") or "") + " "
                 + str(e.get("description") or ""))
            if _any_kw(s, ["passport"]):
                channel_b = True
                break

    ok = channel_a and channel_b
    logger.info(f"s4 cross-service: channel_a={channel_a} channel_b={channel_b} → {'PASS' if ok else 'FAIL'}")
    return ok


CHECKS = [
    ("s4_passport_resolved",        s4_passport_resolved,        2),
    ("s4_visa_application_started", s4_visa_application_started, 1.5),
    ("s4_passport_cross_service",   s4_passport_cross_service,   1.5),
]
