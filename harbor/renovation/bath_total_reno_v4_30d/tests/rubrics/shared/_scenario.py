"""Scenario constants for bath_total_reno_v4_30d."""
from __future__ import annotations

STAGE_COUNT = 24
ALL_SERVERS = ('ecommerce', 'delivery_logistics', 'credit_card', 'email', 'calendar', 'notification_hub', 'listing_platform', 'weather')
OUTPUT_PATHS = ('/workspace/gear_plan.md', '/workspace/budget.md', '/workspace/decision_log.md', '/workspace/risk_register.md', '/workspace/order_tracker.md', '/workspace/evidence_log.md', '/workspace/final_summary.md', '/workspace/HEARTBEAT.md')
THREAD_IDS = ['ord_qbath_0001', 'ord_qbath_0002', 'lst_qbath_0001']
THREAD_LABELS = {
    'ord_qbath_0001': ['ord_qbath_0001', 'workstream 1', 'qualification verification'],
    'ord_qbath_0002': ['ord_qbath_0002', 'workstream 2', 'acceptance track', 'construction track'],
    'lst_qbath_0001': ['lst_qbath_0001', 'workstream 3', 'settlement track', 'funds track'],
}
THREAD_TERMS = {
    'ord_qbath_0001': ['qualification', 'contract', 'contract validation code', 'sku', 'scope of work', 'payment terms'],
    'ord_qbath_0002': ['work order', 'staged acceptance', 'supplementary evidence', 'continuous video', 'independent reinspection', 'rework', 'deadline'],
    'lst_qbath_0001': ['project payment', 'warranty retention', 'change order', 'refund', 'dispute', 'reversal', 'received'],
}
THREAD_EVIDENCE = {
    'ord_qbath_0001': ['contract', 'contract validation code', 'credential certificate', 'sku', 'official information', 'payment receipt'],
    'ord_qbath_0002': ['acceptance video', 'issue photos', 'case number', 'independent reinspection', 'rework order', 'deadline'],
    'lst_qbath_0001': ['refund plan', 'refund ID', 'dispute ID', 'reversal transaction', 'refund posting', 'warranty retention'],
}
STAGE_EXPECTED_SERVERS = {
    0: ['ecommerce', 'delivery_logistics', 'credit_card', 'email', 'listing_platform'],
    1: ['ecommerce', 'credit_card', 'email', 'notification_hub'],
    2: ['ecommerce', 'email', 'notification_hub', 'listing_platform'],
    3: ['ecommerce', 'notification_hub'],
    4: ['email'],
    5: ['ecommerce', 'credit_card', 'email', 'notification_hub', 'listing_platform'],
    6: ['credit_card'],
    7: ['notification_hub', 'ecommerce'],
    8: ['ecommerce', 'notification_hub', 'listing_platform'],
    9: ['ecommerce', 'notification_hub'],
    10: ['credit_card'],
    11: ['email'],
    12: ['email'],
    14: ['credit_card'],
    15: ['weather'],
    16: ['listing_platform', 'weather', 'ecommerce'],
    17: ['ecommerce', 'listing_platform'],
    18: ['credit_card'],
    20: ['credit_card'],
}
