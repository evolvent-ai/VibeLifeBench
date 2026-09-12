from ._helpers import official_post_contains, tool_used_with_args, workspace_contains

STAGE = 8

def s8_official_feed_checked(env) -> bool:
    return (
        tool_used_with_args(env, STAGE, "notification_hub", "get_account_feed", ["cdr_exam_updates"])
        and official_post_contains(env, "post_template_matrix_20260820", ["1200", "eligibility", "hours actually completed", "preceptor confirmation"])
        and workspace_contains(
            env,
            "official_evidence_log.md",
            [["post_template_matrix_20260820"], ["cdr_exam_updates"], ["1200"], ["eligibility"], ["2026-08-20"]],
            160,
        )
    )

CHECKS = [("s8_official_feed_checked", s8_official_feed_checked, 1.5)]
