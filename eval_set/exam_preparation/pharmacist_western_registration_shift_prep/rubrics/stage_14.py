from __future__ import annotations

from ._helpers import email_result_seen, persistent_record


def r27_hr_cert_tracked(env) -> bool:
    cert_seen = bool(
        email_result_seen(env, 14, "msg_hr_cert")
        and email_result_seen(env, 14, "cert_sealed_v1.pdf")
    )
    return bool(
        cert_seen
        and persistent_record(env, 14, "sealed_work_cert", "盖章", "真实", min_hits=1)
    )


CHECKS = [
    ("r27_hr_cert_tracked", r27_hr_cert_tracked, 1.0),
]
