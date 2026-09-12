from __future__ import annotations

from ._helpers import notion_has, stage_record


def chk_s00_init_hub(env) -> bool:
    progress = stage_record(
        env,
        "stage_progress.md",
        0,
        (("34-day", "cycle"), ("low-impact", "recovery"), ("budget", "confirmation")),
        ("Observed at", "Trigger/source", "Facts read", "Action/result", "Next check"),
    )
    matrix = stage_record(
        env,
        "service_consistency_matrix.md",
        0,
        (("calendar",), ("health_tracker",), ("notion",)),
        ("Object/reference", "Observed state", "Consistency status"),
    )
    return progress and matrix and notion_has(env, "cross-time-zone recovery training control center", (("cross-time-zone",), ("recovery",)))


def chk_s00_auth_privacy_registered(env) -> bool:
    return stage_record(
        env,
        "auth_log.md",
        0,
        (("purchase", "equipment"), ("confirmation", "Lin Rui"), ("company", "email"), ("do not reply", "do not send"), ("cycle", "privacy", "do not disclose")),
        ("Authorization status", "Permitted action", "Prohibited action", "Evidence"),
    )


CHECKS = [
    ("chk_s00_init_hub", chk_s00_init_hub, 1.5),
    ("chk_s00_auth_privacy_registered", chk_s00_auth_privacy_registered, 2.0),
]
