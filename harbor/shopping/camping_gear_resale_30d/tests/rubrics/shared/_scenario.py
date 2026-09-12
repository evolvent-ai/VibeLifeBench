"""Generated scenario constants; scoring logic lives in checks.py."""
from __future__ import annotations

STAGE_COUNT = 24
ALL_SERVERS = ('ecommerce', 'delivery_logistics', 'credit_card', 'email', 'calendar', 'notification_hub', 'listing_platform', 'weather')
OUTPUT_PATHS = ('/workspace/gear_plan.md', '/workspace/budget.md', '/workspace/decision_log.md', '/workspace/risk_register.md', '/workspace/order_tracker.md', '/workspace/evidence_log.md', '/workspace/final_summary.md', '/workspace/HEARTBEAT.md')
THREAD_IDS = ['ord_rstent_0001', 'ord_rstent_0002', 'lst_rstent_0001']
THREAD_LABELS = {
    'ord_rstent_0001': ['ord_rstent_0001', 'timeline 1', 'physical item', 'valuation listing'],
    'ord_rstent_0002': ['ord_rstent_0002', 'timeline 2', 'transaction', 'sale line', 'negotiation line'],
    'lst_rstent_0001': ['lst_rstent_0001', 'timeline 3', 'funds', 'payout line', 'money line'],
}
THREAD_TERMS = {
    'ord_rstent_0001': ['outdoor', 'condition', 'listing price', 'listing verification code', 'wildnest', 'price reduction'],
    'ord_rstent_0002': ['sale', 'condition', 'evidence', 'inspection video', 'platform review', 'price reduction', 'deadline', 'buyer', 'proof', 'adjudication'],
    'lst_rstent_0001': ['WildNest 4P tent set', 'payout', 'price reduction', 'full amount', 'recovery', 'service fee', 'difference', 'refund', 'received', 'funds'],
}
THREAD_EVIDENCE = {
    'ord_rstent_0001': ['model', 'listing verification code', 'purchase proof', 'condition grade', 'invoice', 'listing rules'],
    'ord_rstent_0002': ['inspection video', 'condition photos', 'listing number', 'chat record', 'sale order', 'deadline'],
    'lst_rstent_0001': ['sale payout', 'service fee', 'payout reference', 'recovered amount', 'difference', 'received'],
}
STAGE_EXPECTED_SERVERS = {0: ['ecommerce', 'delivery_logistics', 'credit_card', 'listing_platform'], 1: ['ecommerce', 'delivery_logistics', 'credit_card', 'listing_platform'], 2: ['ecommerce', 'notification_hub'], 3: ['ecommerce', 'notification_hub'], 4: ['email'], 6: ['credit_card'], 7: ['ecommerce', 'listing_platform', 'notification_hub'], 9: ['ecommerce'], 10: ['credit_card'], 12: ['email'], 14: ['credit_card', 'calendar'], 15: ['ecommerce', 'weather'], 18: ['credit_card'], 20: ['credit_card']}
