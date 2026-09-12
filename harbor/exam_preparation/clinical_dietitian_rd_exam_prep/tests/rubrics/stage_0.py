from ._helpers import future_study_event_exists, notion_tracker_ready, notion_write_used, task_subscription_active, tool_used_with_args, workspace_contains

STAGE = 0

def s0_notion_started(env) -> bool:
    return notion_write_used(env, STAGE) and notion_tracker_ready(env)

def s0_calendar_seeded(env) -> bool:
    trace_bound = (
        tool_used_with_args(env, STAGE, "calendar", "create_event", ["rdn", "review"])
        or tool_used_with_args(env, STAGE, "calendar", "create_event", ["registration examination", "review"])
        or tool_used_with_args(env, STAGE, "calendar", "create_event", ["nutrition", "mock exam"])
    )
    return trace_bound and future_study_event_exists(env)

def s0_official_watch_created(env) -> bool:
    return (
        tool_used_with_args(env, STAGE, "notification_hub", "create_subscription", ["cdr_exam_updates", "policy_update", "authorization to test"])
        and task_subscription_active(env)
        and workspace_contains(
            env,
            "official_evidence_log.md",
            [["source_type"], ["source_id"], ["cdr_exam_updates"], ["authorization to test"], ["pending", "active"]],
            80,
        )
    )

CHECKS = [
    ("s0_notion_started", s0_notion_started, 1.5),
    ("s0_calendar_seeded", s0_calendar_seeded, 1.25),
    ("s0_official_watch_created", s0_official_watch_created, 1.25),
]
