"""Stage 9: calendar controls for pending decisions."""
from ._helpers import artifact_has, calendar_review_events_created

def s9_calendar_plan(env): return artifact_has(env,"calendar_plan.md",stage=9,any_terms=("cpa","custodian","card","estimated-tax"))
def s9_calendar_tool(env): return calendar_review_events_created(env)
def s9_pending_label(env): return artifact_has(env,"calendar_plan.md",stage=9,any_terms=("pending","review","not authorized"))
def s9_calendar_ids(env): return calendar_review_events_created(env) and artifact_has(env,"calendar_plan.md",stage=9,all_terms=("event_id",),any_terms=("cpa","custodian","card","estimated-tax"))
CHECKS=[("s9_calendar_plan",s9_calendar_plan,1.25),("s9_calendar_tool",s9_calendar_tool,1.0),("s9_pending_label",s9_pending_label,1.25),("s9_calendar_ids",s9_calendar_ids,1.0)]
