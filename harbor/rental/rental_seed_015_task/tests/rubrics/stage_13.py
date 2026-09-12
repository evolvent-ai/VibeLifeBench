from __future__ import annotations
from ._helpers import *


def s13_sister_dates_in_calendar(env) -> bool:
    return (
        stage_ok(env, 13, "s13")
        and sister_dates_backend_ready(env)
        and e_question_draft_backend_ready(env)
        and notion_has_any(env, (["July 28", "July 30", "August 4", "August 6", "sister"], ["Lily Li", "limited assistance", "four dates"]))
        and no_sensitive_attachments(env)
        and non_h_viewings_absent(env)
    )


CHECKS = [("s13_sister_dates_in_calendar", s13_sister_dates_in_calendar, 1.25)]
