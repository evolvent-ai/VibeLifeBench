from __future__ import annotations
from . import _helpers as h


def r29_mock_scores_recorded(env) -> bool:
    return bool(
        h.any_tool(env, 15, ("notion",))
        and h.durable_evidence_contains(env, "wrong question", "wrong_question_ledger.md", "法律法规", "56", "个人理财", "62")
    )


def r30_error_categories_created(env) -> bool:
    return bool(
        h.any_tool(env, 15, ("notion",))
        and h.durable_evidence_contains(
            env, "wrong question", "wrong_question_ledger.md",
            "反洗钱", "消费者权益保护", "年金现值", "风险匹配",
        )
    )


CHECKS = [
    ("r29_mock_scores_recorded", r29_mock_scores_recorded, 1.5),
    ("r30_error_categories_created", r30_error_categories_created, 1.25),
]
