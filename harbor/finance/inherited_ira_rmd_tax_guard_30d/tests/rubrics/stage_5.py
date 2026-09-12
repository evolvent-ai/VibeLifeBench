"""Stage 5: posted consulting income is ordinary taxable cash."""
from ._helpers import any_successful_tool, artifact_has, record_exists

def s5_income_lane(env): return artifact_has(env,"cashflow_plan.md",stage=5,any_terms=("consulting","ordinary_cash","146000"))
def s5_banking_query(env): return any_successful_tool(env,5,(("banking",("list_transactions","get_account")),))
def s5_backend_income(env): return s5_banking_query(env) and record_exists(env,"banking","list_transactions",list_keys=("transactions","items"),predicates={"tx_id":"tx_mut_iirtg_income"},account_id="acct_checking_main")
def s5_not_ira(env): return artifact_has(env,"decision_ledger.md",stage=5,all_terms=("not",),any_terms=("ira distribution","inherited distribution"))
CHECKS=[("s5_income_lane",s5_income_lane,1.0),("s5_banking_query",s5_banking_query,1.0),("s5_backend_income",s5_backend_income,1.5),("s5_not_ira",s5_not_ira,1.25)]
