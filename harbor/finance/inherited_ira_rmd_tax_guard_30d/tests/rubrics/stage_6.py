"""Stage 6: official guidance and account-specific facts remain separate."""
from ._helpers import any_successful_tool, artifact_has

def s6_official_sources(env): return artifact_has(env,"source_evidence.md",stage=6,any_terms=("irs","publication 590-b","estimated-tax"))
def s6_source_query(env): return any_successful_tool(env,6,(("email",("search_emails","read_email")),("notion",("API-post-search",))))
def s6_scope_limit(env): return artifact_has(env,"source_evidence.md",stage=6,any_terms=("general guidance","account-specific","custodian"))
def s6_open_fact(env): return artifact_has(env,"decision_ledger.md",stage=6,any_terms=("beneficiary category","year-of-death","unconfirmed"))
CHECKS=[("s6_official_sources",s6_official_sources,1.25),("s6_source_query",s6_source_query,1.0),("s6_scope_limit",s6_scope_limit,1.5),("s6_open_fact",s6_open_fact,1.0)]
