from ._helpers import _call_json,_tool_call_matches,_workspace_file_text,text_has
OID='of_kansai_daytime_refundable_hold'
def s10_expiring_offer_exact(env):
 d=_call_json(env,'flight_booking','get_flight_offer',offer_id=OID)
 return _tool_call_matches(env,['flight_booking__get_flight_offer'],lambda a:a.get('offer_id')==OID,10) and d.get('offer_id')==OID and (d.get('total_price') or {}).get('amount')==12840 and d.get('expires_at')=='2026-09-18T16:00:00+08:00'
def s10_durable_old_quote(env): return text_has(_workspace_file_text(env,'booking_register.md'),[[OID],['12840'],['2026-09-18'],['not ticketed','ticket not issued'],['expires','expiration']])
CHECKS=[('s10_expiring_offer_exact',s10_expiring_offer_exact,1.0),('s10_durable_old_quote',s10_durable_old_quote,1.0)]
