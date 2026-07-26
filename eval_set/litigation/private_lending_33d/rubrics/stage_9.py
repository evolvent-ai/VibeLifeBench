"""Stage 9: 排程序期限进日历 + 管辖权异议反驳."""
from __future__ import annotations

from ._helpers import _assistant_calendar_events, _assistant_calendar_text, _event_text
from .cross_stage import d_jurisdiction_objection_rebuttal


# 程序期限类关键词 (诉讼节点)。刻意不含 "缴费" —— 种子噪声事件 "水电燃气提醒"
# 的描述含 "缴费"; 也不含 "还款" —— 种子 "信用卡还款" 会误命中。这些词只出现在
# agent 新建的程序期限事件里, 而 ~205 个种子事件(律师咨询/家长会/还款/进货/对款/
# 直播/水电燃气/复诊…)均不匹配。
_PROC_DEADLINE_KEYWORDS = [
    "举证", "开庭", "立案", "上诉", "答辩", "保全", "期限", "质证", "听证",
]


def s9_deadlines_on_calendar(env) -> bool:
    """把程序期限建成日历事件 (side effect)。0 事件≠完成。"""
    text = _assistant_calendar_text(env)
    if text is None:
        return False  # required evidence unavailable → fail closed
    # 须有 agent 新建的程序类事件 (举证/开庭/期限/上诉), 而非仅种子里的律师咨询/家长会/还款
    return any(k in text for k in ["举证", "开庭", "立案", "期限", "上诉", "庭审", "保全"])


def s9_enough_deadlines(env) -> bool:
    """场景约束·执行: 关键程序期限须真建够 (≥4 个 agent 新建的程序期限事件), 不能只口头说。

    日历被种子塞了 ~205 个事件(3 个案件相关 + 202 个 evt_bg_* 噪声), 且噪声落在
    2026-05-01..2026-09-30 查询窗内, 故 raw len 恒 ≥100 —— 用总数判定是死 True。
    改为只统计 summary/description 命中程序期限关键词(举证/开庭/立案/上诉/答辩/保全/
    期限/质证/听证)的事件: 种子噪声事件(进货/对款/直播/水电燃气/复诊…)与 3 个案件
    种子(律师咨询/家长会/信用卡还款)均不匹配, 唯有 agent 新建的程序期限事件命中。
    要求 ≥4 个不同(按 event id 去重, 无 id 则按文本去重)程序期限事件。
    """
    evs = _assistant_calendar_events(env)
    if evs is None:
        return False  # required evidence unavailable → fail closed
    seen: set[str] = set()
    count = 0
    for ev in evs:
        if not isinstance(ev, dict):
            continue
        text = _event_text(ev)
        if not any(k in text for k in _PROC_DEADLINE_KEYWORDS):
            continue
        key = str(ev.get("id") or ev.get("event_id") or text)
        if key in seen:
            continue
        seen.add(key)
        count += 1
    return count >= 4


CHECKS = [
    ("s9_deadlines_on_calendar", s9_deadlines_on_calendar, 0.5),
    ("s9_enough_deadlines", s9_enough_deadlines, 0.5),
    ("d_jurisdiction_objection_rebuttal", d_jurisdiction_objection_rebuttal, 0.5),
]
