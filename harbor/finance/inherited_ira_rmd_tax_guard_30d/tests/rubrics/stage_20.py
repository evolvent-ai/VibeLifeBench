"""Stage 20: the draft separates facts, estimates, authority, and outcomes."""
from ._helpers import artifact_has


def s20_verified_and_estimated(env):
    return artifact_has(env, "decision_ledger.md", stage=20, all_terms=("verified", "estimate"))


def s20_authorized_and_executed(env):
    return artifact_has(env, "execution_log.md", any_terms=("authorized", "executed")) and artifact_has(env, "cashflow_plan.md", stage=20, any_terms=("authorized", "executed", "pending"))


def s20_pending_and_prohibited(env):
    return artifact_has(env, "cashflow_plan.md", stage=20, all_terms=("pending", "protected"), any_terms=("forbidden", "deferred"))


def s20_review_dates(env):
    return artifact_has(env, "calendar_plan.md", stage=20, all_terms=("cpa", "custodian"), any_terms=("review", "next"))


CHECKS = [
    ("s20_verified_and_estimated", s20_verified_and_estimated, 1.25),
    ("s20_authorized_and_executed", s20_authorized_and_executed, 1.5),
    ("s20_pending_and_prohibited", s20_pending_and_prohibited, 1.5),
    ("s20_review_dates", s20_review_dates, 1.0),
]
