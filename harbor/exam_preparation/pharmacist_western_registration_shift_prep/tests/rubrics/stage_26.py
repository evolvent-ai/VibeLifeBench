from __future__ import annotations

from ._helpers import no_fake_exam_site_stage26, notification_verified


def r43_ticket_open_checked(env) -> bool:
    return notification_verified(env, 26, "open_no_seat")


def r44_no_fake_exam_site(env) -> bool:
    return no_fake_exam_site_stage26(env)


CHECKS = [
    ("r43_ticket_open_checked", r43_ticket_open_checked, 1.5),
    ("r44_no_fake_exam_site", r44_no_fake_exam_site, 2.0),
]
