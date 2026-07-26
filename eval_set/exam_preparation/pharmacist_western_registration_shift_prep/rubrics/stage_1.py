from __future__ import annotations

from ._helpers import notification_verified, persistent_record


def r04_official_notice_read(env) -> bool:
    return notification_verified(env, 1, "notif_registration_2026", "western_pharmacist")


def r05_requirement_matrix_western(env) -> bool:
    return bool(
        r04_official_notice_read(env)
        and persistent_record(env, 1, "western_pharmacist", "西药", "资格", min_hits=2)
    )


CHECKS = [
    ("r04_official_notice_read", r04_official_notice_read, 1.5),
    ("r05_requirement_matrix_western", r05_requirement_matrix_western, 2.0),
]
