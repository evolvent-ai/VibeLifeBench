"""Scenario constants (generated). ； checks.py"""
from __future__ import annotations

STAGE_COUNT = 24
ALL_SERVERS = ('ecommerce', 'delivery_logistics', 'credit_card', 'email', 'calendar', 'notification_hub', 'listing_platform', 'weather')
OUTPUT_PATHS = ('/workspace/gear_plan.md', '/workspace/budget.md', '/workspace/decision_log.md', '/workspace/risk_register.md', '/workspace/order_tracker.md', '/workspace/evidence_log.md', '/workspace/final_summary.md', '/workspace/HEARTBEAT.md')
THREAD_IDS = ['ord_rscam_0001', 'ord_rscam_0002', 'lst_rscam_0001']
THREAD_LABELS = {'ord_rscam_0001': ['ord_rscam_0001', 'track 1', 'valuation listing'], 'ord_rscam_0002': ['ord_rscam_0002', 'track 2', 'sale track', 'negotiation track'], 'lst_rscam_0001': ['lst_rscam_0001', 'track 3', 'payout track', 'funds track']}
THREAD_TERMS = {'ord_rscam_0001': ['imaging', 'condition', 'listing price', 'listing verification code', 'sonar', 'low offer'], 'ord_rscam_0002': ['sale', 'condition', 'evidence submission', 'inspection video', 'platform review', 'low offer', 'deadline', 'buyer', 'proof'], 'lst_rscam_0001': ['Sonar A7M3 resale', 'payout', 'low offer', 'full-price', 'recover', 'service fee', 'difference', 'return', 'deposited', 'funds']}
THREAD_EVIDENCE = {'ord_rscam_0001': ['model', 'listing verification code', 'purchase proof', 'condition grade', 'invoice', 'listing rules'], 'ord_rscam_0002': ['inspection video', 'condition photos', 'listing number', 'sale order', 'deadline'], 'lst_rscam_0001': ['sale payout', 'service fee', 'payout number', 'recovered amount', 'difference', 'deposited']}

# The checkers use this map to bind a stage's server evidence to the tool that
# actually supplies it.  A server-only prefix is insufficient: many mocks expose
# several unrelated read channels under one service name.
STAGE_EXPECTED_TOOLS = {
    0: {'ecommerce': ('get_order',), 'delivery_logistics': ('track_package',), 'credit_card': ('get_card',)},
    1: {'ecommerce': ('get_order',), 'delivery_logistics': ('track_package',), 'credit_card': ('get_card',), 'listing_platform': ('get_listing_detail',)},
    2: {'ecommerce': ('get_product',), 'notification_hub': ('get_account_feed',)},
    3: {'ecommerce': ('get_order',), 'notification_hub': ('get_notification',), 'listing_platform': ('get_listing_detail',)},
    4: {'email': ('search_emails',)},
    6: {'credit_card': ('list_unbilled',)},
    7: {'notification_hub': ('get_notification',), 'listing_platform': ('get_listing_detail',)},
    9: {'ecommerce': ('get_order',)},
    10: {'credit_card': ('list_unbilled',)},
    12: {'email': ('search_emails',)},
    14: {'credit_card': ('list_disputes',)},
    15: {'ecommerce': ('get_order',), 'weather': ('get_forecast_daily',)},
    18: {'credit_card': ('list_disputes',)},
    20: {'credit_card': ('list_unbilled',)},
}
STAGE_EXPECTED_SERVERS = {0: ['ecommerce', 'delivery_logistics', 'credit_card'], 1: ['ecommerce', 'delivery_logistics', 'credit_card', 'listing_platform'], 2: ['ecommerce', 'notification_hub'], 3: ['ecommerce', 'notification_hub'], 4: ['email'], 6: ['credit_card'], 7: ['notification_hub', 'listing_platform'], 9: ['ecommerce'], 10: ['credit_card'], 12: ['email'], 14: ['credit_card'], 15: ['ecommerce', 'weather'], 18: ['credit_card'], 20: ['credit_card']}
