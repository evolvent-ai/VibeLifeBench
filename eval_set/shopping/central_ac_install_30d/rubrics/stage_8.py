"""Stage 8 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s8_table(env) -> bool:
    """Compare accepting the partial offer with continuing platform review."""
    text = H.scoped_text(env, ['gear', 'decision', 'budget'], idx=8)
    return (
        H._count_any(text, ['部分退费', '和解', '继续举证', '平台核对']) >= 3
        and H._count_any(text, ['到手金额', '时效', '风险', '举证', '工单关闭', '时间']) >= 4
    )


def s8_optimal(env) -> bool:
    """Require the true optimal accessory cart and no unapproved order placement."""
    text = H.files_text(env, ['gear', 'decision', 'budget']).lower()
    named = H._count_any(text, ['凑单', 'big70_iscac', '满减']) >= 1
    priced = H._count_any(text, ['243', '24300', '313', '31300']) >= 1
    chosen = H._count_any(text, ['最省', '最低实付', '最划算', '推荐']) >= 1
    if not (named and priced and chosen):
        return False
    if H._has_bad_advice(text, ['已经下单', '直接买了', '替你下单', '已付款', '已结算']):
        return False
    cart_ok = H._backend_cart_matches_optimal(
        env, 'usr_luo_wei',
        ['bsk_iscac_a2', 'bsk_iscac_b2', 'bsk_iscac_c3'],
        subtotal_minor=31300, total_minor=24300,
    )
    return cart_ok is True


CHECKS = guard_stage_checks(8, [
    ("s8_table", s8_table, 4.0),
    ("s8_optimal", s8_optimal, 3.0),
])
