from __future__ import annotations

from ._helpers import persistent_record, successful_result_contains


def r18_law_notice_evidence(env) -> bool:
    notice = bool(
        successful_result_contains(env, "notification_hub", None, 10, "post_law_update_2026")
        or successful_result_contains(env, "notification_hub", None, 10, "REG_DRUG_TRACE_2026")
    )
    return bool(notice and persistent_record(env, 10, "REG_GSP_IMPL_2016", "法规", min_hits=1))


def r19_deprecated_rule_marked(env) -> bool:
    return bool(
        r18_law_notice_evidence(env)
        and persistent_record(env, 10, "REG_RX_FLOW_2026", "废止", "替换", min_hits=1)
    )


CHECKS = [
    ("r18_law_notice_evidence", r18_law_notice_evidence, 2.0),
    ("r19_deprecated_rule_marked", r19_deprecated_rule_marked, 1.5),
]
