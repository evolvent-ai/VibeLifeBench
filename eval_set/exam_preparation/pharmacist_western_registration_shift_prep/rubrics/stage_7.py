from __future__ import annotations

from ._helpers import notification_verified, persistent_record


def r12_schema_change_found(env) -> bool:
    return notification_verified(env, 7, "schema_v2", "employer_unified_social_credit_code")


def r13_org_code_added(env) -> bool:
    return bool(
        r12_schema_change_found(env)
        and persistent_record(
            env,
            7,
            "employer_unified_social_credit_code",
            "统一社会信用代码",
            "信用代码",
            min_hits=1,
        )
    )


CHECKS = [
    ("r12_schema_change_found", r12_schema_change_found, 1.5),
    ("r13_org_code_added", r13_org_code_added, 1.5),
]
