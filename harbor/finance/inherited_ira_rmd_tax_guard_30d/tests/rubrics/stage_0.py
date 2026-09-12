"""Stage 0: scope, reserve boundary, and initial archive."""
from ._helpers import any_successful_tool, artifact_has

def s0_scope(env): return artifact_has(env,"decision_ledger.md",stage=0,any_terms=("inherited","beneficiary","reserve"))
def s0_initial_query(env): return any_successful_tool(env,0,(("banking",("list_accounts","get_account")),("email",("search_emails","get_emails"))))
def s0_reserve_boundary(env): return artifact_has(env,"decision_ledger.md",stage=0,all_terms=("reserve",),any_terms=("protected","restricted","forbidden"))
def s0_trace_link(env): return artifact_has(env,"tool_audit_matrix.md",stage=0,any_terms=("banking","email","notion"))
CHECKS=[("s0_scope",s0_scope,1.0),("s0_initial_query",s0_initial_query,1.0),("s0_reserve_boundary",s0_reserve_boundary,1.5),("s0_trace_link",s0_trace_link,1.0)]
