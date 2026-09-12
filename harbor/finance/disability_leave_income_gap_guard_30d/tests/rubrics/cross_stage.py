"""Cross-stage state and causality checks for the disability-leave bridge."""
from __future__ import annotations

from ._common import common
from ._helpers import (
    REQUIRED_FILES,
    STAGE_COUNT,
    all_mutation_backend_state,
    all_required_files_present,
    authorized_payment_persisted,
    authorized_payment_trace,
    benefit_deposit_present,
    calendar_plan_persisted,
    current_account_backend_state,
    current_card_backend_state,
    evidence_service_breadth,
    leave_claim_backend_state,
    no_unauthorized_state_change,
    persistent_payment_record,
    protected_account_verified,
    source_backend_present,
    source_file_complete,
)


def cs_protected_reserve_backend(env) -> bool:
    return protected_account_verified(env)


def cs_authorization_precedes_payment(env) -> bool:
    return authorized_payment_trace(env)


def cs_exact_payment_persisted(env) -> bool:
    return authorized_payment_persisted(env)


def cs_no_unapproved_financial_move(env) -> bool:
    return authorized_payment_persisted(env) and no_unauthorized_state_change(env, STAGE_COUNT - 1)


def cs_calendar_has_no_business_duplicates(env) -> bool:
    return calendar_plan_persisted(env, require_claim_schedule=True)


def cs_estimate_and_posted_benefit_separated(env) -> bool:
    return leave_claim_backend_state(env) and benefit_deposit_present(env) and common.file_has_groups(
        env,
        ("/workspace/benefit_timeline.md", "/workspace/cash_bridge.md"),
        (("benefit estimates", "estimate"), ("posted benefits", "posted net"), ("pending determinations", "unresolved")),
        min_numbers=4,
    )


def cs_mutations_reconciled_in_durable_files(env) -> bool:
    return all_mutation_backend_state(env) and common.file_has_groups(
        env,
        ("/workspace/account_snapshot.md", "/workspace/benefit_timeline.md", "/workspace/cash_bridge.md", "/workspace/execution_log.md"),
        (
            ("payroll adjustment",),
            ("claim delay", "documentation delay"),
            ("benefit deposit", "posted benefits"),
            ("pharmacy refund", "refund"),
            ("periodic interest", "interest"),
            ("$1,460.00", "146000 minor", "146000"),
            ("$1,260.00", "126000 minor", "126000"),
            ("$286.00", "28600 minor", "28600"),
            ("$72.00", "7200 minor", "7200"),
            ("$26.00", "2600 minor", "2600"),
        ),
        min_numbers=10,
    )


def cs_source_is_qualified_not_personalized(env) -> bool:
    return source_backend_present(env) and source_file_complete(env)


def cs_successful_service_evidence_breadth(env) -> bool:
    return evidence_service_breadth(env) >= 4 and all_mutation_backend_state(env)


def cs_payment_backend_linked_to_archive(env) -> bool:
    return persistent_payment_record(env)


def cs_cross_file_delivery_components_exist(env) -> bool:
    return (
        all_required_files_present(env)
        and current_account_backend_state(env)
        and current_card_backend_state(env)
        and leave_claim_backend_state(env)
        and common.file_has_groups(
        env,
        REQUIRED_FILES,
        (("$13,250", "13250"), ("$480", "48000", "480"), ("pending",), ("authorized",)),
        min_numbers=12,
        )
    )


CHECKS = [
    ("cs_protected_reserve_backend", cs_protected_reserve_backend, 5.0),
    ("cs_authorization_precedes_payment", cs_authorization_precedes_payment, 5.0),
    ("cs_exact_payment_persisted", cs_exact_payment_persisted, 5.0),
    ("cs_no_unapproved_financial_move", cs_no_unapproved_financial_move, 5.0),
    ("cs_calendar_has_no_business_duplicates", cs_calendar_has_no_business_duplicates, 4.0),
    ("cs_estimate_and_posted_benefit_separated", cs_estimate_and_posted_benefit_separated, 4.0),
    ("cs_mutations_reconciled_in_durable_files", cs_mutations_reconciled_in_durable_files, 4.0),
    ("cs_source_is_qualified_not_personalized", cs_source_is_qualified_not_personalized, 4.0),
    ("cs_successful_service_evidence_breadth", cs_successful_service_evidence_breadth, 3.0),
    ("cs_payment_backend_linked_to_archive", cs_payment_backend_linked_to_archive, 5.0),
    ("cs_cross_file_delivery_components_exist", cs_cross_file_delivery_components_exist, 4.0),
]
