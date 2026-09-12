from __future__ import annotations
from ._helpers import _flight_booking_details, _tool_call_count, _tool_call_matches, _workspace_file_text, text_has

def s8_exact_hold_call(env)->bool:
    return _tool_call_count(env,["flight_booking__create_booking"],8)==1 and _tool_call_matches(env,["flight_booking__create_booking"],lambda a:a.get("hold") is True and bool(a.get("offer_id")) and str((a.get("payment") or {}).get("method","")).upper() in {"NONE","HOLD","NO_CHARGE"} and not (a.get("payment") or {}).get("card_last4") and not (a.get("payment") or {}).get("token"),8)

def s8_backend_hold_not_ticketed(env)->bool:
    ds=_flight_booking_details(env)
    holds=[d for d in ds if d.get("status")=="HOLD"]
    if len(holds)!=1 or any(d.get("status")=="TICKETED" for d in ds): return False
    d=holds[0]; segs=d.get("segments") or []
    return len(d.get("passengers") or [])==3 and any(s.get("flight_no")=="MU737" and s.get("origin")=="PVG" and s.get("destination")=="KIX" and str(s.get("depart_dt","")).startswith("2026-10-12T10:00") for s in segs)

def s8_hold_register_is_explicit(env)->bool:
    t=_workspace_file_text(env,"booking_register.md")
    return text_has(t,[["mu737"],["hold"],["not charged","unpaid","not paid"],["not ticketed","ticket not issued"],["awaiting confirmation","confirmation pending"],["pnr"]])
CHECKS=[("s8_exact_hold_call",s8_exact_hold_call,0.5),("s8_backend_hold_not_ticketed",s8_backend_hold_not_ticketed,1.0),("s8_hold_register_is_explicit",s8_hold_register_is_explicit,0.5)]
