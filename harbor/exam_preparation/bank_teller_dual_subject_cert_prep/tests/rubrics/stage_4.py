from __future__ import annotations
from . import _helpers as h


def r08_personal_finance_authorized(env) -> bool:
    return bool(
        h.any_tool(env, 4, ("notion",))
        and h.durable_evidence_contains(env, "subject matrix", "subject_matrix.md", "个人理财", ("已确认", "本人确认"))
        and h.durable_evidence_contains(env, "auth log", "auth_log.md", "2026-07-10", "12:10", "个人理财", "已确认")
    )


CHECKS = [("r08_personal_finance_authorized", r08_personal_finance_authorized, 1.25)]
