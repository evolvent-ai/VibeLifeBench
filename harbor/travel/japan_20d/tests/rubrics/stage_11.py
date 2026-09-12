"""Stage 11 rubric — typhoon upgraded, replan (D11)."""
from __future__ import annotations


from .shared._helpers import (
    _any_kw,
    _call,
    _cron_reminders,
    _notion_text,
)
from .cross_stage import weather_advisory_surfaced_timely

from loguru import logger


def s11_typhoon_replan(env) -> bool:
    """After high-confidence track: agent proposes replan for Kyoto/Osaka."""
    notion = _notion_text(env)
    if notion:
        replan_hit = _any_kw(notion, ["typhoon", "maya", "t2602"]) \
            and _any_kw(notion, ["replan", "reschedule", "swap", "indoor",
                                 "kyoto", "osaka", "kansai"])
        if replan_hit:
            logger.info("s11 replan: PASS via notion")
            return True

    hotels = _call(env, "hotel_booking", "list_reservations", user_id="li_wei")
    if isinstance(hotels, dict):
        for rid in (hotels.get("reservation_ids") or [])[:10]:
            detail = _call(env, "hotel_booking", "get_reservation",
                           reservation_id=rid)
            if not isinstance(detail, dict):
                continue
            city = str(detail.get("city") or detail.get("hotel_name") or "").lower()
            hist = detail.get("history") or []
            if any(w in city for w in ["kyoto", "osaka", "kansai"]):
                if any(str(h.get("event", "")).lower() in
                       ("modified", "rescheduled", "moved")
                       for h in hist if isinstance(h, dict)):
                    logger.info(f"s11 replan: PASS via hotel {rid} modified")
                    return True

    for r in _cron_reminders(env):
        text = str(r.get("text", "")).lower()
        if "typhoon" in text or "replan" in text or "maya" in text:
            if int(r.get("registered_by_day", 99)) <= 11:
                logger.info("s11 replan: PASS via cron")
                return True

    logger.info("s11 replan: FAIL")
    return False


def s11_typhoon_track_surfaced(env) -> bool:
    """Agent surfaced the high-confidence track update PROACTIVELY."""
    notion = _notion_text(env)
    if notion:
        storm_hit = _any_kw(notion, ["maya", "t2602"])
        region_hit = _any_kw(notion, ["kansai", "osaka", "kyoto"])
        if storm_hit and region_hit:
            logger.info("s11 track surfaced: PASS via notion")
            return True

    for r in _cron_reminders(env):
        if int(r.get("registered_by_day", 99)) <= 11:
            t = str(r.get("text", "")).lower()
            if "maya" in t or "t2602" in t or "typhoon" in t:
                logger.info("s11 track surfaced: PASS via cron")
                return True

    logger.info("s11 track surfaced: FAIL")
    return False


CHECKS = [
    ("s11_typhoon_replan",                 s11_typhoon_replan,                2.5),
    ("s11_typhoon_track_surfaced",         s11_typhoon_track_surfaced,        1.5),
    ("d_weather_advisory_surfaced_timely", weather_advisory_surfaced_timely,  1.5),
]
