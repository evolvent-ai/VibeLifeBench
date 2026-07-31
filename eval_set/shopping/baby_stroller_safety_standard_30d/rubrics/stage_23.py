"""Stage 23 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s23_structured(env) -> bool:
    """关键词命中：选定文件/回复中至少出现 5 个规定要素。

    证据维度：📝持久化 💬回复
    """
    return H._count_any(H.scoped_text(env, ['summary'], idx=23), ['已解决', '处理中', '待确认', '待到账', '经验', '模板']) >= 5


def s23_threads(env) -> bool:
    """三条线在归档/跟踪文件中分块清晰、互不混淆（每条线锚点+要素齐备）。

    证据维度：📝持久化
    """
    text = H.files_text(env, ['summary', 'tracker']).lower()
    return H._thread_sections_distinct(text)


CHECKS = guard_stage_checks(23, [
    ("s23_structured", s23_structured, 2.0),
    ("s23_threads", s23_threads, 1.0),
])
