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
    """消防 no-go 结论既要在回复里成立，也要 D13 消防 FAIL 已在后端整改到 approved 口径。"""
    text = (stage_response(ctx, stage=20) + "\n" + await workspace_text(ctx)).lower()
    fire_text = _count(text, ["消防", "报备", "活动后补", "no-go", "不能"]) >= 3
    fire_backend = status_is_approved((await app_status_map(ctx)).get(APP_FIRE, ""))
    return fire_text and fire_backend


async def s20_voc_third_party_backed(ctx) -> bool:
    """VOC 第三方检测既要在回复里成立，也要交付/空气质量后端状态脱离阻断基线。"""
    text = (stage_response(ctx, stage=20) + "\n" + await workspace_text(ctx)).lower()
    voc_text = _count(text, ["voc", "第三方", "自测截图", "检测", "证据"]) >= 3
    voc_backend = status_is_approved((await app_status_map(ctx)).get(APP_HANDOVER, ""))
    return voc_text and voc_backend


async def s20_invoice_corrected(ctx) -> bool:
    text = (stage_response(ctx, stage=20) + "\n" + await workspace_text(ctx)).lower()
    return _count(text, ["发票", "抬头", "个人", "错误", "更正"]) >= 4


async def s20_elevator_freight_window(ctx) -> bool:
    text = (stage_response(ctx, stage=20) + "\n" + await workspace_text(ctx)).lower()
    return _count(text, ["电梯", "限时", "罚款", "物业"]) >= 3


async def s20_partition_load_bearing_payment_occupancy(ctx) -> bool:
    text = (stage_response(ctx, stage=20) + "\n" + await workspace_text(ctx)).lower()
    structure = _count(text, ["隔断", "承重", "复核", "新增", "安全"]) >= 4
    auth = _count(text, ["尾款", "开业宣传", "人员入驻", "授权", "等我"]) >= 4
    return structure and auth


CHECKS = [
    ("s20_fire_no_go_backed", s20_fire_no_go_backed, 4.0),
    ("s20_voc_third_party_backed", s20_voc_third_party_backed, 4.0),
    ("s20_invoice_corrected", s20_invoice_corrected, 3.0),
    ("s20_elevator_freight_window", s20_elevator_freight_window, 3.0),
    ("s20_partition_load_bearing_payment_occupancy", s20_partition_load_bearing_payment_occupancy, 2.757),
]
