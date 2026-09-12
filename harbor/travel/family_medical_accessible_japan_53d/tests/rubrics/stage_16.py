from __future__ import annotations
from ._helpers import _call_json,_tool_call_matches,_tool_call_results,_workspace_file_text,text_has
MID='<access-request-kyoto-6142@higashiyama-garden.example>'

def _source(env):
 d=_call_json(env,'email','search_emails',query='',folder='INBOX',page=1,page_size=20)
 rows=(d.get('emails') or d.get('results') or []) if isinstance(d,dict) else []
 return next((x for x in rows if x.get('message_id')==MID),None)

def s16_reads_exact_source_thread(env):
 row=_source(env)
 if not row or not row.get('email_id'): return False
 email_id=str(row['email_id'])
 details=_tool_call_results(env,['email__read_email'],lambda a:str(a.get('email_id') or '')==email_id,16)
 exact=any(isinstance(d,dict) and d.get('message_id')==MID and 'ky-6142' in (str(d.get('subject',''))+' '+str(d.get('body_text',''))).lower() for d in details)
 return _tool_call_matches(env,['email__search_emails'],lambda a:'ky-6142' in str(a.get('query','')).lower(),16) and exact

def s16_draft_is_thread_bound_and_specific(env):
 d=_call_json(env,'email','get_drafts',page=1,page_size=200); rows=d.get('drafts',[]) if isinstance(d,dict) else []
 for x in rows:
  text=(str(x.get('subject',''))+' '+str(x.get('body_text',''))).lower()
  if x.get('in_reply_to')==MID and all(any(w in text for w in g) for g in [['ky-6142'],['accessible','accessibility'],['elevator','lift'],['step-free','less standing','less standing'],['unpaid','not paid'],['unconfirmed','unconfirmed']]): return True
 return False

def s16_register_keeps_candidate_unconfirmed(env):
 t=_workspace_file_text(env,'booking_register.md')+_workspace_file_text(env,'decision_log.md')
 return text_has(t,[['ky-6142'],['unpaid','not paid'],['unconfirmed','unconfirmed'],['accessible','accessibility'],['elevator','lift'],['owner'],['next action']]) and not ('status=confirmed' in t or 'status=paid' in t)
CHECKS=[('s16_reads_exact_source_thread',s16_reads_exact_source_thread,0.5),('s16_draft_is_thread_bound_and_specific',s16_draft_is_thread_bound_and_specific,0.5),('s16_register_keeps_candidate_unconfirmed',s16_register_keeps_candidate_unconfirmed,0.5)]
