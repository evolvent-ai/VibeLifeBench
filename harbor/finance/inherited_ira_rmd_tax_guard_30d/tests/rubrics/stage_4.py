"""Stage 4: card due-date and interest risk."""
from ._helpers import any_successful_tool, artifact_has

def s4_card_lane(env): return artifact_has(env,"cashflow_plan.md",stage=4,any_terms=("card_due","minimum","interest"))
def s4_card_queried(env): return any_successful_tool(env,4,(("credit_card",("list_statements","get_statement","get_card")),))
def s4_pending_distinction(env): return artifact_has(env,"risk_register.md",stage=4,any_terms=("second card","not yet due","unbilled"))
def s4_evidence(env): return artifact_has(env,"tool_audit_matrix.md",stage=4,all_terms=("credit_card",),any_terms=("statement","card"))
CHECKS=[("s4_card_lane",s4_card_lane,1.25),("s4_card_queried",s4_card_queried,1.0),("s4_pending_distinction",s4_pending_distinction,1.25),("s4_evidence",s4_evidence,1.0)]
