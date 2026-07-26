"""Stage 13: 检验机构被迫更换(静默注入) — agent 须自查、改选 JY-008(场景约束·高权重), 不耽误开庭."""
from __future__ import annotations

from ._helpers import _stage_corpus, _notifications
from .cross_stage import d_inspect_reselect


def s13_detects_withdraw(env) -> bool:
    """agent 自查通知, 察觉 JY-006 被暂停不能用 (响应静默注入)。"""
    notifs = _notifications(env)
    if notifs is None:
        return False  # required evidence unavailable → fail closed
    has_notice = any(
        str(item.get("notification_id") or "") == "ntf_food_s13_inspector_pause"
        or (
            any(key in f"{item.get('title', '')} {item.get('body', '')}" for key in ("JY-006", "沪正"))
            and any(key in f"{item.get('title', '')} {item.get('body', '')}" for key in ("暂停", "停用", "不能用"))
        )
        for item in notifs
        if isinstance(item, dict)
    )
    text = _stage_corpus(env, 13)
    has_response = any(
        key in text
        for key in ("JY-006", "沪正", "暂停", "不能用", "停用", "更换", "换机构", "另选")
    )
    return has_notice and has_response


CHECKS = [
    ("s13_detects_withdraw", s13_detects_withdraw, 0.5),
    ("d_inspect_reselect", d_inspect_reselect, 3.389),  # 场景约束: 改选 JY-008, 不回到已排除机构
]
