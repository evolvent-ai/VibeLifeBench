"""Stage 24 — validate audit references against real banking/legal/job_board backend objects。"""
from __future__ import annotations

from ._helpers import audit_domain_count, norm_num, stage_write_used, validated_audit_refs, wfile


def s24_audit_trace_has_transaction_ids(env) -> bool:
    text = wfile(env, "audit_journal.md")
    if not text.strip() or not stage_write_used(env, 24):
        return False
    return len(validated_audit_refs(env, text)["transactions"]) >= 3


def s24_reconciliation_sources_linked(env) -> bool:
    text = wfile(env, "audit_journal.md")
    normalized = norm_num(text.lower())
    if not normalized.strip() or not stage_write_used(env, 24):
        return False
    valid = validated_audit_refs(env, text)
    values = all(value in normalized for value in ("33600", "302400", "205400", "97000"))
    legal = len(valid["cases"] | valid["articles"]) >= 2
    employment = bool(valid["jobs"] or valid["applications"])
    return len(valid["transactions"]) >= 3 and legal and employment and audit_domain_count(valid) == 3 and values


CHECKS = [
    ("s24_audit_trace_has_transaction_ids", s24_audit_trace_has_transaction_ids, 3.0),
    ("s24_reconciliation_sources_linked", s24_reconciliation_sources_linked, 3.0),
]
