from __future__ import annotations

from ._helpers import email_has, no_sent_email, stage_record


def chk_s02_schedule_email_used(env) -> bool:
    source = email_has(env, "early-July teaching schedule", (("7/4",), ("7/11",), ("10:00-14:00",)))
    progress = stage_record(env, "stage_progress.md", 2, (("teaching schedule",), ("Saturday long class",), ("email",), ("read-only", "no reply needed")), ("Facts read", "Decision", "Action/result"))
    return source and progress and no_sent_email(env)


def chk_s02_schedule_context_logged(env) -> bool:
    return stage_record(env, "schedule_context_log.md", 2, (("Saturday long class",), ("10:00", "14:00"), ("between-class", "break window"), ("personal reminder",)), ("Schedule object", "Date/time/location", "Source", "Available break", "Personal-reminder impact", "Verified at"))


CHECKS = [
    ("chk_s02_schedule_email_used", chk_s02_schedule_email_used, 1.5),
    ("chk_s02_schedule_context_logged", chk_s02_schedule_context_logged, 1.25),
]
