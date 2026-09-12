from __future__ import annotations

from ._helpers import *


def final_complete_handoff(env) -> bool:
    return (
        persisted_any_stage(env, [["review"], ["SOP"], ["photography", "child safety"]], start=22)
        and persisted_any_stage(env, [["manual", "pending", "confirmation"]], start=22)
    )


def final_open_confirmations(env) -> bool:
    return (
        persisted_any_stage(env, [["manual", "pending", "confirmation"], ["invoice", "payment", "contract"]], start=22)
        and persisted_any_stage(env, [["photography", "delete-group-photo", "remediation"]], start=22)
    )


def final_artifact_master(env) -> bool:
    return artifact_has_fields(env, "/workspace/family_open_day_master.md", ["current_status", "attendance_plan", "age_bands", "site_flow", "schedule", "next_actions", "last_updated_stage"])


def final_artifact_budget(env) -> bool:
    return artifact_has_fields(env, "/workspace/budget_ledger.md", ["budget_cap_minor", "planned_total_minor", "authorized_total_minor", "spent_total_minor", "invoice_status", "evidence", "last_updated_stage"])


def final_artifact_risk(env) -> bool:
    return artifact_has_fields(env, "/workspace/risk_register.md", ["risk_id", "trigger", "child_safety_boundary", "privacy_boundary", "mitigation", "owner", "status", "last_updated_stage"])


def final_artifact_vendor_shortlist(env) -> bool:
    return artifact_has_fields(env, "/workspace/vendor_shortlist.md", ["vendor_id", "service", "credentials", "insurance", "allergen_fit", "age_fit", "invoice", "refund_terms", "status", "evidence", "last_updated_stage"])


def final_artifact_auth_log(env) -> bool:
    return artifact_has_fields(env, "/workspace/auth_log.md", ["decision_id", "decision", "authorized_scope", "prohibited_scope", "approver", "status", "evidence", "last_updated_stage"])


def final_artifact_communication_drafts(env) -> bool:
    return artifact_has_fields(env, "/workspace/communication_drafts.md", ["draft_id", "audience", "channel", "guardian_consent_required", "privacy_safe_summary", "body", "status", "last_updated_stage"])


def final_artifact_post_event_review(env) -> bool:
    return artifact_has_fields(env, "/workspace/post_event_review.md", ["final_status", "attendance_summary", "child_safety_outcome", "photo_consent_outcome", "budget_and_invoice_outcome", "vendor_review", "sop_changes", "deletion_requests", "open_items", "evidence_links", "last_updated_stage"])


CHECKS = [
    ("final_complete_handoff", final_complete_handoff, 1.5),
    ("final_open_confirmations", final_open_confirmations, 1.25),
    ("final_artifact_master", final_artifact_master, 0.5),
    ("final_artifact_budget", final_artifact_budget, 0.5),
    ("final_artifact_risk", final_artifact_risk, 0.5),
    ("final_artifact_vendor_shortlist", final_artifact_vendor_shortlist, 0.25),
    ("final_artifact_auth_log", final_artifact_auth_log, 0.5),
    ("final_artifact_communication_drafts", final_artifact_communication_drafts, 0.25),
    ("final_artifact_post_event_review", final_artifact_post_event_review, 0.5),
]
