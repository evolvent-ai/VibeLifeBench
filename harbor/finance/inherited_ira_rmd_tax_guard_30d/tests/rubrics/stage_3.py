"""Stage 3: CPA fact gaps."""
from ._helpers import any_successful_tool, artifact_has

def s3_questions(env): return artifact_has(env,"decision_ledger.md",stage=3,any_terms=("date of death","beneficiary","year-of-death","rmd"))
def s3_records_checked(env): return any_successful_tool(env,3,(("email",("search_emails","read_email")),("notion",("API-post-search",))))
def s3_no_guessed_amount(env): return artifact_has(env,"risk_register.md",stage=3,any_terms=("missing","unconfirmed","do not guess"))
def s3_next_action(env): return artifact_has(env,"decision_ledger.md",stage=3,all_terms=("next_action",),any_terms=("cpa","custodian"))
CHECKS=[("s3_questions",s3_questions,1.25),("s3_records_checked",s3_records_checked,1.0),("s3_no_guessed_amount",s3_no_guessed_amount,1.5),("s3_next_action",s3_next_action,1.0)]
