from ._helpers import notion_page_contains, notion_write_used, official_post_contains, tool_used_with_args, workspace_contains

STAGE = 9

def s9_template_update_logged(env) -> bool:
    return (
        tool_used_with_args(env, STAGE, "notification_hub", "get_account_feed", ["cdr_exam_updates"])
        and notion_write_used(env, STAGE)
        and official_post_contains(env, "post_template_matrix_20260820", ["1200", "eligibility", "hours actually completed"])
        and notion_page_contains(
            env,
            ["department competency", "hours", "tracker"],
            [["post_template_matrix_20260820"], ["1200"], ["eligibility"], ["preceptor"], ["confirmation", "approved"]],
        )
        and workspace_contains(env, "official_evidence_log.md", [["post_template_matrix_20260820"], ["status"], ["stage"]], 220)
    )

CHECKS = [("s9_template_update_logged", s9_template_update_logged, 1.5)]
