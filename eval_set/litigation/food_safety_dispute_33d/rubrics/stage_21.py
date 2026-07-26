"""Stage 21: 复盘 — 总结、成本与二审方向须写入案件台账。"""
from __future__ import annotations

from ._helpers import _food_journal_text


def s21_retro_in_notion(env) -> bool:
    text = _food_journal_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_retro = any(key in text for key in ("复盘", "总结", "经验", "教训"))
    has_process = sum(key in text for key in ("节点", "证据", "法条", "判例", "检验")) >= 3
    has_cost = any(key in text for key in ("成本", "诉讼费", "检验费", "时间成本"))
    return has_retro and has_process and has_cost


def s21_second_instance_direction(env) -> bool:
    text = _food_journal_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_second = any(key in text for key in ("二审", "被上诉人", "答辩"))
    has_focus = sum(key in text for key in ("检验报告", "一审判决", "证据", "上诉请求", "维持原判")) >= 2
    return has_second and has_focus


CHECKS = [
    ("s21_persisted_retrospective", s21_retro_in_notion, 0.75),
    ("s21_persisted_second_instance_direction", s21_second_instance_direction, 0.5),
]
