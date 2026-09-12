"""Rubric predicate documentation."""
from __future__ import annotations

STAGE_COUNT = 24
ALL_SERVERS = ('ecommerce', 'delivery_logistics', 'credit_card', 'email', 'calendar', 'notification_hub', 'listing_platform', 'weather')
OUTPUT_PATHS = ('/workspace/gear_plan.md', '/workspace/budget.md', '/workspace/decision_log.md', '/workspace/risk_register.md', '/workspace/order_tracker.md', '/workspace/evidence_log.md', '/workspace/final_summary.md', '/workspace/HEARTBEAT.md')
THREAD_IDS = ['ord_camp_0001', 'ord_camp_0002', 'lst_camp_0001']
THREAD_LABELS = {'ord_camp_0001': ['ord_camp_0001', 'line 1', 'procurement optimum within budget'], 'ord_camp_0002': ['ord_camp_0002', 'line 2', 'price comparison line', 'delivery line'], 'lst_camp_0001': ['lst_camp_0001', 'line 3', 'discount line', 'price protection line']}
THREAD_TERMS = {'ord_camp_0001': ['tent', 'waterproof rating', 'fabric', 'verification number', 'Yecheng', 'model'], 'ord_camp_0002': ['price comparison', 'platform', 'price difference', 'shipping', 'gift', 'net price', 'delivery', 'timing', 'reroute', 'pickup'], 'lst_camp_0001': ['folding table-and-chair set', 'coupon', 'threshold discount', 'discount', 'price protection', 'price difference', 'validity period', 'refund', 'credited', 'promotion']}
THREAD_EVIDENCE = {'ord_camp_0001': ['model', 'verification number', 'waterproof rating', 'proof of purchase', 'invoice', 'specification'], 'ord_camp_0002': ['platform', 'platform prices', 'shipping', 'gift', 'delivery timing', 'reroute record'], 'lst_camp_0001': ['coupon code', 'discount threshold', 'validity period', 'price-protection claim number', 'price difference', 'credited']}
STAGE_EXPECTED_SERVERS = {0: ['ecommerce', 'delivery_logistics', 'credit_card'], 1: ['ecommerce', 'delivery_logistics', 'credit_card', 'listing_platform'], 2: ['ecommerce', 'notification_hub'], 3: ['ecommerce', 'notification_hub'], 4: ['email'], 6: ['credit_card'], 7: ['ecommerce'], 9: ['delivery_logistics'], 10: ['credit_card'], 12: ['email'], 14: ['credit_card'], 15: ['weather', 'delivery_logistics'], 18: ['credit_card'], 20: ['credit_card']}
