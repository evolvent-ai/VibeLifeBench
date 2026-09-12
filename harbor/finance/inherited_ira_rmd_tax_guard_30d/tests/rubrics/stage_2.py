"""Stage 2: multi-service household baseline."""
from ._helpers import any_successful_tool, artifact_has

def s2_cash_lanes(env): return artifact_has(env,"cashflow_plan.md",stage=2,any_terms=("ordinary_cash","reserve","card"))
def s2_accounts_queried(env): return any_successful_tool(env,2,(("banking",("list_accounts","get_account")),("credit_card",("list_cards","get_card","list_statements")),("brokerage",("list_accounts","get_portfolio"))))
def s2_reserve_flag(env): return artifact_has(env,"cashflow_plan.md",stage=2,all_terms=("protected",),any_terms=("estate reserve","restricted"))
def s2_backend_links(env): return artifact_has(env,"tool_audit_matrix.md",stage=2,any_terms=("backend_object_id","acct_","card_"))
CHECKS=[("s2_cash_lanes",s2_cash_lanes,1.25),("s2_accounts_queried",s2_accounts_queried,1.0),("s2_reserve_flag",s2_reserve_flag,1.5),("s2_backend_links",s2_backend_links,1.0)]
