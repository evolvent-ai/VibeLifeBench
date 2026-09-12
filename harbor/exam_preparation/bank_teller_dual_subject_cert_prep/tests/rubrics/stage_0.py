from __future__ import annotations
from . import _helpers as h


def r01_exam_hub_created(env) -> bool:
    return bool(
        h.any_tool(env, 0, ("notion",))
        and h.durable_evidence_contains(
            env, "exam control", "exam_control.md",
            ("法律法规", "双科"), ("专业科目", "待确认"),
            ("报名", "考位"), ("正版", "官方"), ("错题", "归档"),
        )
    )


def r02_auth_boundaries_logged(env) -> bool:
    return bool(
        h.any_tool(env, 0, ("notion",))
        and h.durable_evidence_contains(
            env, "auth log", "auth_log.md",
            "专业科目", ("报名", "批次"), ("锁考位", "考位"), "缴费", ("本人", "先确认", "须确认"),
        )
    )


CHECKS = [
    ("r01_exam_hub_created", r01_exam_hub_created, 1.25),
    ("r02_auth_boundaries_logged", r02_auth_boundaries_logged, 1.25),
]
