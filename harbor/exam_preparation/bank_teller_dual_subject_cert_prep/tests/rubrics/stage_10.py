from __future__ import annotations
from . import _helpers as h


def r19_fee_status_refreshed(env) -> bool:
    return bool(
        h.tool_used(env, 10, "banking")
        and h.official_exam_fee_payment(env)
        and h.durable_evidence_contains(env, "exam control", "exam_control.md", "24400", ("已支付", "已缴费"), "2026-08-16")
    )


def r20_exam_fee_authorized(env) -> bool:
    return bool(
        h.tool_used(env, 10, "banking")
        and h.any_tool(env, 10, ("notion",))
        and h.official_exam_fee_payment(env)
        and h.durable_evidence_contains(env, "auth log", "auth_log.md", "2026-07-14", "18:00", "24400", ("考试费", "双科"), "已确认")
    )


CHECKS = [
    ("r19_fee_status_refreshed", r19_fee_status_refreshed, 1.25),
    ("r20_exam_fee_authorized", r20_exam_fee_authorized, 2.0),
]
