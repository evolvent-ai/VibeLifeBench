from ._helpers import notion_mock_log_ready, notion_write_used, workspace_contains

STAGE = 15

def s15_mock_log_maintained(env) -> bool:
    return (
        notion_write_used(env, STAGE)
        and notion_mock_log_ready(env)
        and workspace_contains(
            env,
            "mock_score_log.md",
            [["taken_at"], ["score"], ["domain"], ["error_categories"], ["fatigue_signal"], ["source"], ["follow_up"]],
            100,
        )
    )

CHECKS = [("s15_mock_log_maintained", s15_mock_log_maintained, 1.25)]
