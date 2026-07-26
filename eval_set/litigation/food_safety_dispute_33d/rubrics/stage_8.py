"""Stage 8: 法院立案受理(world + 注入) — 响应受理, 提示后续举证/检验/抗辩准备."""
from __future__ import annotations

from ._helpers import _stage_corpus, _notifications


def s8_responds_acceptance(env) -> bool:
    """响应立案受理, 提示后续举证/检验/开庭。"""
    text = _stage_corpus(env, 8)
    has_accept = any(k in text for k in ["受理", "立案", "案号", "民初"])
    has_next = sum(
        1 for k in ["举证", "检验", "开庭", "抗辩", "准备意见", "后续安排"] if k in text
    ) >= 2
    return has_accept and has_next


def s8_detects_acceptance_notice(env) -> bool:
    """agent 自查通知中心可见受理通知(响应注入)。"""
    notifs = _notifications(env)
    if notifs is None:
        return False  # required evidence unavailable → fail closed
    has_notice = any(
        (n.get("notification_id") == "ntf_food_s8_case_accepted")
        or ("立案受理" in str(n.get("title") or "") and "(2026)沪0115民初" in str(n.get("body") or ""))
        for n in notifs
    )
    text = _stage_corpus(env, 8)
    mentions_notice = any(k in text for k in ["(2026)沪0115民初", "案号", "受理通知", "立案受理"])
    return has_notice and mentions_notice


CHECKS = [
    ("s8_detects_acceptance_notice", s8_detects_acceptance_notice, 0.5),
]
