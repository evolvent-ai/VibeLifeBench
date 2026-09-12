from . import _helpers as h

EXPECTED_SERVICES = ('job_board', 'email', 'calendar', 'notion', 'notification_hub')


def _calls(env):
    loader = getattr(h, "tool_calls", None) or getattr(h, "trace_calls", None)
    return list(loader(env)) if callable(loader) else []


def _successful_calls(env):
    return [call for call in _calls(env) if call.get("success") is True]


def tq_successful_tool_result_coverage(env):
    calls = _calls(env)
    successful = _successful_calls(env)
    return (
        len(successful) >= 24
        and len(successful) / max(len(calls), 1) >= 0.9
        and all(isinstance(call.get("arguments") or {}, dict) for call in successful)
    )


def tq_required_service_coverage(env):
    requirements = {
        "job_board": (("search_jobs", "get_job"),),
        "email": (("get_emails", "read_email", "search_emails"), ("save_draft", "update_draft")),
        "calendar": (("list_events", "get_event", "search_events"), ("create_event", "update_event")),
        "notion": (
            ("API-post-search", "API-retrieve-a-page", "API-get-block-children"),
            ("API-post-page", "API-patch-page", "API-patch-block-children", "API-update-a-block"),
        ),
        "notification_hub": (
            ("list_notifications", "get_notification", "mark_read"),
            ("create_subscription", "pause_subscription", "delete_subscription"),
        ),
    }
    calls = _successful_calls(env)
    return all(
        all(
            any(
                any(h.tool_name_matches(str(call.get("name") or ""), server, tool) for tool in alternatives)
                for call in calls
            )
            for alternatives in groups
        )
        for server, groups in requirements.items()
    )


CHECKS = [
    ("tq_successful_tool_result_coverage", tq_successful_tool_result_coverage, 1.5),
    ("tq_required_service_coverage", tq_required_service_coverage, 1.5),
]
