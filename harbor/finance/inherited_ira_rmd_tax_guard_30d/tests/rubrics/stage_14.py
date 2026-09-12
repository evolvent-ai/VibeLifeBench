"""Stage 14: CPA tax estimate remains distinct from obligation and authorization."""
from ._helpers import any_successful_tool, artifact_has


def s14_taxable_estimate(env):
    return artifact_has(env, "source_evidence.md", stage=14, all_terms=("taxable", "withholding"), any_terms=("cpa", "estimate"))


def s14_no_immediate_requirement(env):
    return artifact_has(env, "decision_ledger.md", stage=14, any_terms=("not confirmed", "not required immediately", "open question"))


def s14_no_amount_authorized(env):
    return artifact_has(env, "decision_ledger.md", stage=14, all_terms=("distribution",), any_terms=("not authorized", "deferred", "estimate"))


def s14_source_checked(env):
    return any_successful_tool(env, 14, (("email", ("search_emails", "read_email")), ("notion", ("post_search", "retrieve_a_page"))))


CHECKS = [
    ("s14_taxable_estimate", s14_taxable_estimate, 1.5),
    ("s14_no_immediate_requirement", s14_no_immediate_requirement, 1.25),
    ("s14_no_amount_authorized", s14_no_amount_authorized, 1.5),
    ("s14_source_checked", s14_source_checked, 1.0),
]
