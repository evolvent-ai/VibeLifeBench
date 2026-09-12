"""Stage 21: require a successful journal append and an object-specific five-incident retrospective."""
from __future__ import annotations

from loguru import logger

from ._helpers import _flight_booking_details, _hotel_reservation_details, _notion_text, _tool_calls, _tool_name_matches, _workspace_file_text


def s21_gate(env) -> bool:
    patch_calls=[c for c in _tool_calls(env,21) if _tool_name_matches(str(c.get("name") or ""),"notion","API-patch-block-children")]
    if not patch_calls:
        return False
    notion=_notion_text(env).casefold()
    incident=_workspace_file_text(env,"/workspace/incident_log.md").casefold()
    replacement=next((b for b in _flight_booking_details(env) if str(b.get("status") or "").upper()=="TICKETED" and any(str(s.get("origin") or "").upper() in {"PVG","SHA"} and str(s.get("destination") or s.get("dest") or "").upper() in {"NRT","HND"} and str(s.get("flight_no") or "").upper()!="MU501" for s in b.get("segments") or [] if isinstance(s,dict))),None)
    hotels=_hotel_reservation_details(env)
    replacement_hotel=next((r for r in hotels if str(r.get("status") or "").casefold() in {"confirmed","modified"} and str(r.get("check_in"))[:10]=="2026-06-05" and r.get("hotel_id")!="htl_shinjuku_grand"),None)
    dynamic=[str(replacement.get("pnr") or "").casefold() if replacement else "",str(replacement_hotel.get("reservation_id") or "").casefold() if replacement_hotel else ""]
    incidents=[
        all(x in notion for x in ("mu501",dynamic[0])) if dynamic[0] else False,
        all(x in notion for x in ("htl_shinjuku_grand",dynamic[1])) if dynamic[1] else False,
        "158/96" in notion,
        "acct_wang_hao_001" in notion,
        ("level 3" in notion and "korea" in notion),
    ]
    review=any(x in notion for x in ("retrospective","lesson"))
    durable_chain=sum(incidents)>=5 and all(x in incident for x in ("mu501","158/96","acct_wang_hao_001"))
    ok=bool(review and durable_chain)
    logger.info("s21_gate: patch={} review={} incidents={} -> {}",bool(patch_calls),review,incidents,"PASS" if ok else "FAIL")
    return ok


CHECKS=[("s21_gate",s21_gate,1.5)]
