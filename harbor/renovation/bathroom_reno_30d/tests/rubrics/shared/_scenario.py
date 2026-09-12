"""Scenario constants for bathroom_reno_30d."""
from __future__ import annotations

STAGE_COUNT = 24
ALL_SERVERS = ('ecommerce', 'delivery_logistics', 'credit_card', 'email', 'calendar', 'notification_hub', 'listing_platform', 'weather')
OUTPUT_PATHS = ('/workspace/gear_plan.md', '/workspace/budget.md', '/workspace/decision_log.md', '/workspace/risk_register.md', '/workspace/order_tracker.md', '/workspace/evidence_log.md', '/workspace/final_summary.md', '/workspace/HEARTBEAT.md')
THREAD_IDS = ['ord_r2bth_0001', 'ord_r2bth_0002', 'lst_r2bth_0001']
THREAD_LABELS = {
    'ord_r2bth_0001': ['ord_r2bth_0001', 'workstream 1', 'workstream 1', 'workstream 1', 'workstream 1', 'qualification verification'],
    'ord_r2bth_0002': ['ord_r2bth_0002', 'workstream 2', 'workstream 2', 'workstream 2', 'workstream 2', 'acceptance track', 'construction track'],
    'lst_r2bth_0001': ['lst_r2bth_0001', 'workstream 3', 'workstream 3', 'workstream 3', 'workstream 3', 'settlement track', 'funds track'],
}
THREAD_TERMS = {
    'ord_r2bth_0001': ['qualification', 'contract', 'contract verification code', 'licensed electrician', 'material batch', 'grab-bar backing'],
    'ord_r2bth_0002': ['work order', 'stage acceptance', 'threshold waterproofing', 'grab-bar backing', 'third-party quality inspection', 'rework', 'reinspection'],
    'lst_r2bth_0001': ['project payment', 'warranty retention', 'change order', 'refund', 'dispute', 'reversal', 'received'],
}
THREAD_EVIDENCE = {
    'ord_r2bth_0001': ['contract', 'contract verification code', 'qualification certificate', 'material batch', 'sku', 'payment receipt'],
    'ord_r2bth_0002': ['acceptance video', 'issue photos', 'threshold waterproofing', 'grab-bar backing', 'third-party quality inspection', 'reinspection'],
    'lst_r2bth_0001': ['refund option', 'refund ID', 'dispute ID', 'reversal transaction', 'refund posting', 'warranty retention'],
}
STAGE_EXPECTED_SERVERS = {
    0: ['ecommerce', 'delivery_logistics', 'credit_card'],
    1: ['ecommerce', 'delivery_logistics', 'credit_card', 'listing_platform'],
    2: ['ecommerce', 'notification_hub'],
    3: ['ecommerce', 'notification_hub'],
    4: ['email'],
    5: ['calendar', 'delivery_logistics', 'listing_platform'],
    6: ['credit_card'],
    7: ['notification_hub', 'ecommerce'],
    8: ['notification_hub', 'ecommerce', 'listing_platform'],
    9: ['ecommerce', 'notification_hub'],
    10: ['credit_card'],
    11: ['email'],
    12: ['email'],
    13: ['ecommerce', 'credit_card'],
    14: ['credit_card'],
    15: ['weather'],
    16: ['listing_platform', 'ecommerce'],
    17: ['ecommerce', 'notification_hub', 'listing_platform'],
    18: ['credit_card'],
    19: ['ecommerce', 'credit_card', 'notification_hub'],
    20: ['credit_card'],
    21: ['ecommerce', 'credit_card', 'email', 'calendar'],
    22: ['ecommerce', 'credit_card', 'email', 'calendar', 'notification_hub'],
    23: ['ecommerce', 'credit_card'],
}
