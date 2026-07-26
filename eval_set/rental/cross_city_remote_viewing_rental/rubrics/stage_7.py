from __future__ import annotations
from ._helpers import *


def s7_email_fee_draft(env) -> bool:
    return (
        tool_stage(env, 7, "email", None, ("rent-c",))
        and stage_draft_has(env, 7, ("锁房款",))
        and draft_has_parts(env, ("退还",))
    )


def s7_no_oral_commitment_as_fact(env) -> bool:
    return stage7_written_commitment_guard(env)


CHECKS = [
    ("s7_email_fee_draft", s7_email_fee_draft, 1.5),
    ("s7_no_oral_commitment_as_fact", s7_no_oral_commitment_as_fact, 2.0),
]
