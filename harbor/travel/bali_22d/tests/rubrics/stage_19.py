"""Stage 19: bind VOA/pickup guidance to the live GA837 arrival and exact entry rule."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import _agent_responses, _call, _tool_call_matches, search_calendar_events, workspace_file_content


def s19_voa_guidance_for_mother(env) -> bool:
    visa_checked = _tool_call_matches(
        env,
        "visa_and_advisory",
        "check_entry_requirements",
        lambda a: str(a.get("nationality") or "").upper() == "CN"
        and str(a.get("destination") or "").upper() == "ID"
        and str(a.get("purpose") or "").casefold() == "tourism",
        stage=19,
    )
    status_checked = _tool_call_matches(
        env,
        "flight_booking",
        "get_flight_status",
        lambda a: str(a.get("flight_no") or "").replace(" ", "").upper() == "GA837"
        and str(a.get("date") or "") == "2026-06-22",
        stage=19,
    )
    road_checked = _tool_call_matches(
        env,
        "maps",
        "get_traffic_estimate",
        lambda a: "ubud" in str(a).casefold()
        and "kintamani" in str(a).casefold()
        and "2026-06-22" in str(a.get("depart_at") or ""),
        stage=19,
    )
    rule = _call(env, "visa_and_advisory", "check_entry_requirements", nationality="CN", destination="ID", purpose="tourism")
    status = _call(env, "flight_booking", "get_flight_status", flight_no="GA837", date="2026-06-22")
    road = _call(env, "maps", "get_traffic_estimate", origin="pl_ubud_palace", dest="pl_kintamani_view", depart_at="2026-06-22T09:00:00+08:00")
    resp = _agent_responses(env, 19).casefold().replace(",", "")
    itinerary = workspace_file_content(env, "/workspace/itinerary.md").casefold()
    risk = workspace_file_content(env, "/workspace/risk_register.md").casefold()
    calendar = search_calendar_events(env, "GA837")
    rule_ok = "500000" in str(rule).replace(",", "") and int(rule.get("passport_validity_months") or 0) == 6
    arrival_ok = isinstance(status, dict) and str(status.get("status") or "").upper() == "ARRIVED" and str(status.get("gate") or "").upper() == "A2"
    road_ok = "evt_kintamani_volcano_closure" in str(road).casefold() and "closure" in str(road).casefold()
    guided = any(x in resp for x in ("liu fang", "mother", "mother", "mother")) and any(
        x in resp for x in ("voa", "visa on arrival", "VOA")
    ) and "500000" in resp and any(x in resp for x in ("a2", "carousel 5", "carousel 5", "pickup"))
    durable = "ga837" in itinerary and "2026-06-22" in itinerary and any(
        "ga837" in str(event).casefold() and "2026-06-22" in str(event) for event in calendar
    )
    volcano_action = any(x in (itinerary + "\n" + risk) for x in ("level 3", "siaga", "level 3")) and "6km" in (itinerary + risk).replace(" ", "") and "kintamani" in (itinerary + risk) and any(
        x in (itinerary + "\n" + risk) for x in ("closed", "cancel", "closed", "cancel")
    )
    result = bool(visa_checked and status_checked and road_checked and rule_ok and arrival_ok and road_ok and guided and durable and volcano_action)
    logger.info("s19_voa_guidance_for_mother: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [("s19_voa_guidance_for_mother", s19_voa_guidance_for_mother, 2.5)]
