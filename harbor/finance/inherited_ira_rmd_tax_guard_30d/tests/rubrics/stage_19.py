"""Stage 19: misinformation is compared with official and account-specific evidence."""
from ._helpers import any_successful_tool, artifact_has


def s19_claims_logged(env):
    return artifact_has(env, "risk_register.md", stage=19, any_terms=("empty immediately", "withholding settles", "spreadsheet", "misinformation"))


def s19_official_comparison(env):
    return artifact_has(env, "source_evidence.md", stage=19, all_terms=("irs",), any_terms=("beneficiary", "590-b", "10-year"))


def s19_account_specific_boundary(env):
    return artifact_has(env, "decision_ledger.md", stage=19, any_terms=("custodian-specific", "beneficiary facts", "not universal", "not confirmed"))


def s19_sources_requeried(env):
    return any_successful_tool(env, 19, (("email", ("search_emails", "read_email")), ("notion", ("post_search", "retrieve_a_page"))))


CHECKS = [
    ("s19_claims_logged", s19_claims_logged, 1.0),
    ("s19_official_comparison", s19_official_comparison, 1.5),
    ("s19_account_specific_boundary", s19_account_specific_boundary, 1.5),
    ("s19_sources_requeried", s19_sources_requeried, 1.0),
]
