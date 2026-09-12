"""Stage 18: custodian processing prerequisites are evidence, not settlement."""
from ._helpers import any_successful_tool, artifact_has


def s18_email_requery(env):
    return any_successful_tool(env, 18, (("email", ("search_emails", "read_email")),))


def s18_prerequisites_recorded(env):
    return artifact_has(env, "source_evidence.md", stage=18, all_terms=("signed election", "withholding"), any_terms=("northstar", "custodian"))


def s18_not_distribution_confirmation(env):
    return artifact_has(env, "decision_ledger.md", stage=18, all_terms=("distribution",), any_terms=("not confirmed", "not settled", "pending"))


def s18_timeline_risk(env):
    return artifact_has(env, "risk_register.md", stage=18, any_terms=("processing", "prerequisite", "timing", "settlement"))


CHECKS = [
    ("s18_email_requery", s18_email_requery, 1.25),
    ("s18_prerequisites_recorded", s18_prerequisites_recorded, 1.5),
    ("s18_not_distribution_confirmation", s18_not_distribution_confirmation, 1.75),
    ("s18_timeline_risk", s18_timeline_risk, 1.0),
]
