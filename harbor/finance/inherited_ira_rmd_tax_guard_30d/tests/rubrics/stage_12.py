"""Stage 12: custodian classification is recorded without inventing an election."""
from ._helpers import any_successful_tool, artifact_has


def s12_nonspouse_fact(env):
    return artifact_has(env, "source_evidence.md", stage=12, all_terms=("non-spouse",), any_terms=("northstar", "custodian"))


def s12_election_separate(env):
    return artifact_has(env, "decision_ledger.md", stage=12, all_terms=("election",), any_terms=("separate", "not authorized", "pending"))


def s12_withholding_irreversible(env):
    return artifact_has(env, "risk_register.md", stage=12, all_terms=("withholding",), any_terms=("settled", "cannot", "irreversible"))


def s12_source_requery(env):
    return any_successful_tool(env, 12, (("email", ("search_emails", "read_email")), ("notion", ("post_search", "api-post-search"))))


CHECKS = [
    ("s12_nonspouse_fact", s12_nonspouse_fact, 1.5),
    ("s12_election_separate", s12_election_separate, 1.5),
    ("s12_withholding_irreversible", s12_withholding_irreversible, 1.25),
    ("s12_source_requery", s12_source_requery, 1.0),
]
