from __future__ import annotations

from ._helpers import (
    email_result_seen,
    official_status_seen,
    persistent_record,
    remediation_verified_stage16,
    successful_result_contains,
)


def r28_rejection_found_by_scheduled(env) -> bool:
    return bool(
        official_status_seen(env, "rejected_need_sealed_cert")
        and successful_result_contains(
            env, "notification_hub", None, 16, "rejected_need_sealed_cert"
        )
    )


def r29_sealed_cert_packet_prepared(env) -> bool:
    return bool(
        r28_rejection_found_by_scheduled(env)
        and email_result_seen(env, 16, "msg_hr_cert")
        and email_result_seen(env, 16, "cert_sealed_v1.pdf")
        and persistent_record(env, 16, "盖章", "补正", "真实", min_hits=1)
    )


def r30_resubmission_status_verified(env) -> bool:
    return remediation_verified_stage16(env)


# Compatibility aliases for older local scripts.
def r29_sealed_cert_uploaded(env) -> bool:
    return r29_sealed_cert_packet_prepared(env)


def r30_progress_resubmitted(env) -> bool:
    return r30_resubmission_status_verified(env)


CHECKS = [
    ("r28_rejection_found_by_scheduled", r28_rejection_found_by_scheduled, 2.0),
    ("r29_sealed_cert_packet_prepared", r29_sealed_cert_packet_prepared, 2.0),
    ("r30_resubmission_status_verified", r30_resubmission_status_verified, 1.5),
]
