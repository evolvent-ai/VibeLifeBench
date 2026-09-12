"""Stage 22: source hierarchy stays explicit at closeout."""
from ._helpers import any_successful_tool, artifact_has


def s22_irs_general_rule(env):
    return artifact_has(env, "source_evidence.md", stage=22, all_terms=("irs",), any_terms=("general guidance", "590-b", "beneficiary"))


def s22_estimated_tax_source(env):
    return artifact_has(env, "source_evidence.md", stage=22, all_terms=("estimated-tax",), any_terms=("irs", "due date"))


def s22_custodian_specific(env):
    return artifact_has(env, "source_evidence.md", stage=22, all_terms=("custodian",), any_terms=("account-specific", "election", "processing"))


def s22_source_requery(env):
    return any_successful_tool(env, 22, (("email", ("search_emails", "read_email")), ("notion", ("post_search", "retrieve_a_page"))))


CHECKS = [
    ("s22_irs_general_rule", s22_irs_general_rule, 1.25),
    ("s22_estimated_tax_source", s22_estimated_tax_source, 1.25),
    ("s22_custodian_specific", s22_custodian_specific, 1.5),
    ("s22_source_requery", s22_source_requery, 1.0),
]
