"""Stage 1: custodian packet and source lineage."""
from ._helpers import any_successful_tool, artifact_has

def s1_packet_recorded(env): return artifact_has(env,"source_evidence.md",stage=1,any_terms=("custodian","beneficiary","distribution election"))
def s1_email_read(env): return any_successful_tool(env,1,(("email",("search_emails","read_email","get_emails")),))
def s1_source_separated(env): return artifact_has(env,"source_evidence.md",stage=1,all_terms=("publisher","source_status"),any_terms=("account-specific","custodian"))
def s1_audit_link(env): return artifact_has(env,"tool_audit_matrix.md",stage=1,all_terms=("email",),any_terms=("success","ok","completed"))
CHECKS=[("s1_packet_recorded",s1_packet_recorded,1.0),("s1_email_read",s1_email_read,1.0),("s1_source_separated",s1_source_separated,1.5),("s1_audit_link",s1_audit_link,1.0)]
