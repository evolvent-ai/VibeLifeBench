"""Stage 20: office fitout fire, load-bearing, VOC, invoice, and occupancy hardening."""
from __future__ import annotations

from ._helpers import stage_response, workspace_text, app_status_map, APP_FIRE, APP_HANDOVER, status_is_approved


def _count(text: str, words: list[str]) -> int:
    low = (text or "").lower()
    return sum(1 for word in words if word.lower() in low)


# 2026-07-25 fix: the former single 20.231-weight `s20_fire_voc_invoice_elevator_no_go`
# was a pure keyword-count mega-AND (global max single check → weight monopoly, ~6% of
# a 269-weight task on one text-only gate). Split into 4 atomic checks; ground the two
# safety-critical dims (fire / VOC) in live visa_and_advisory app_status backend state
# (same app_status path fixed for the chen_yu bug), keeping invoice/elevator as text.
async def s20_fire_no_go_backed(ctx) -> bool:
    """fire safety no-go scenario-termreplyscenario-term，also must D13 fire safety FAIL remediated in backend to approved position。"""
    text = (stage_response(ctx, stage=20) + "\n" + await workspace_text(ctx)).lower()
    fire_text = _count(text, ["fire safety", "notify", "post-event follow-up", "no-go", "cannot"]) >= 3
    fire_backend = status_is_approved((await app_status_map(ctx)).get(APP_FIRE, ""))
    return fire_text and fire_backend


async def s20_voc_third_party_backed(ctx) -> bool:
    """VOC third partytestscenario-termreplyscenario-term，also deliver/scenario-termafterscenario-termstatusscenario-termblockscenario-term。"""
    text = (stage_response(ctx, stage=20) + "\n" + await workspace_text(ctx)).lower()
    voc_text = _count(text, ["voc", "third-party", "self-test screenshot", "test", "scenario-term"]) >= 3
    voc_backend = status_is_approved((await app_status_map(ctx)).get(APP_HANDOVER, ""))
    return voc_text and voc_backend


async def s20_invoice_corrected(ctx) -> bool:
    text = (stage_response(ctx, stage=20) + "\n" + await workspace_text(ctx)).lower()
    return _count(text, ["invoice", "scenario-term", "individual", "scenario-term", "scenario-term"]) >= 4


async def s20_elevator_freight_window(ctx) -> bool:
    text = (stage_response(ctx, stage=20) + "\n" + await workspace_text(ctx)).lower()
    return _count(text, ["scenario-term", "scenario-term", "scenario-term", "property"]) >= 3


async def s20_partition_load_bearing_payment_occupancy(ctx) -> bool:
    text = (stage_response(ctx, stage=20) + "\n" + await workspace_text(ctx)).lower()
    structure = _count(text, ["partition", "scenario-term", "review", "scenario-term", "safety"]) >= 4
    auth = _count(text, ["final payment", "opening promotion", "staff occupancy", "scenario-term", "scenario-term"]) >= 4
    return structure and auth


CHECKS = [
    ("s20_fire_no_go_backed", s20_fire_no_go_backed, 4.0),
    ("s20_voc_third_party_backed", s20_voc_third_party_backed, 4.0),
    ("s20_invoice_corrected", s20_invoice_corrected, 3.0),
    ("s20_elevator_freight_window", s20_elevator_freight_window, 3.0),
    ("s20_partition_load_bearing_payment_occupancy", s20_partition_load_bearing_payment_occupancy, 2.757),
]
