from __future__ import annotations

from ._helpers import _check


def stage_21_archive_and_onboarding_reminders_created(env) -> bool:
    return _check("final_archive_and_onboarding_reminders_created", env)


CHECKS = [
    ("stage_21_archive_and_onboarding_reminders_created", stage_21_archive_and_onboarding_reminders_created, 1.75),
]
