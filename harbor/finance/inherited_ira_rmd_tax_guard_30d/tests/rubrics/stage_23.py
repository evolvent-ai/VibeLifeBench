"""Stage 23: concise closeout is backed by the durable archive and final state."""
from ._helpers import artifact_has, object_field, stage_crosslink_strict, workspace_files_present


_REQUIRED = (
    "source_evidence.md", "tool_audit_matrix.md", "decision_ledger.md", "cashflow_plan.md",
    "risk_register.md", "calendar_plan.md", "execution_log.md", "final_summary.md",
)


def s23_all_files_present(env):
    return workspace_files_present(env, _REQUIRED) and all(stage_crosslink_strict(env, stage) for stage in range(24))


def s23_final_sections(env):
    return artifact_has(env, "final_summary.md", all_terms=("verified_facts", "executed_actions", "pending_actions", "forbidden_actions", "protected_assets", "next_review_dates", "open_questions", "evidence_links"))


def s23_reserve_untouched(env):
    value = object_field(env, "banking", "get_account", "balance_minor", account_id="acct_protected")
    return value is not None and int(value) >= 1325000 and artifact_has(env, "final_summary.md", all_terms=("reserve",), any_terms=("untouched", "protected"))


def s23_distribution_open_questions(env):
    return artifact_has(env, "final_summary.md", all_terms=("distribution",), any_terms=("beneficiary", "year-of-death", "election", "withholding"))


CHECKS = [
    ("s23_all_files_present", s23_all_files_present, 1.5),
    ("s23_final_sections", s23_final_sections, 2.0),
    ("s23_reserve_untouched", s23_reserve_untouched, 2.0),
    ("s23_distribution_open_questions", s23_distribution_open_questions, 1.5),
]
