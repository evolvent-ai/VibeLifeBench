"""Scenario constants for anc_earphone_presale_30d."""
from __future__ import annotations

STAGE_COUNT = 24
ALL_SERVERS = ('ecommerce', 'delivery_logistics', 'credit_card', 'email', 'calendar', 'notification_hub', 'listing_platform', 'weather')
OUTPUT_PATHS = ('/workspace/gear_plan.md', '/workspace/budget.md', '/workspace/decision_log.md', '/workspace/risk_register.md', '/workspace/order_tracker.md', '/workspace/evidence_log.md', '/workspace/final_summary.md', '/workspace/HEARTBEAT.md')
THREAD_IDS = ['ord_psea_0001', 'ord_psea_0002', 'lst_psea_0001']
THREAD_LABELS = {
    'ord_psea_0001': ['ord_psea_0001', 'workstream 1', 'deposit price-lock verification'],
    'ord_psea_0002': ['ord_psea_0002', 'workstream 2', 'final-payment workstream', 'window workstream'],
    'lst_psea_0001': ['lst_psea_0001', 'workstream 3', 'price protection and marketplace payout', 'marketplace-payout funds workstream'],
}
THREAD_TERMS = {
    'ord_psea_0001': ['audio-video', 'presale price', 'deposit bonus', 'presale verification code', 'sonicpod', 'misleading'],
    'ord_psea_0002': ['final payment', 'window', 'deposit bonus', 'presale-page screenshot', 'marketplace review', 'deposit refund after deadline', 'deadline', 'customer support', 'evidence', 'ruling'],
    'lst_psea_0001': ['price protection', 'price difference', 'full amount', 'recover', 'deposit deduction', 'refund', 'funds arrival', 'listing', 'marketplace escrow', 'sale', 'settlement', 'marketplace payout'],
}
THREAD_EVIDENCE = {
    'ord_psea_0001': ['model', 'presale verification code', 'deposit receipt', 'deposit bonus', 'invoice', 'threshold-discount rules'],
    'ord_psea_0002': ['presale-page screenshot', 'deposit receipt', 'order number', 'chat record', 'deposit-refund record', 'deadline'],
    'lst_psea_0001': ['price-protection refund', 'deposit deduction', 'refund reference', 'recovered amount', 'funds-arrival record', 'invoice', 'condition', 'listing ID', 'marketplace escrow', 'sale record', 'settlement record', 'marketplace payout'],
}
STAGE_EXPECTED_SERVERS = {
    0: ['ecommerce', 'delivery_logistics', 'credit_card', 'calendar'],
    1: ['ecommerce', 'delivery_logistics', 'credit_card', 'listing_platform'],
    2: ['ecommerce', 'notification_hub'],
    3: ['ecommerce', 'notification_hub'],
    4: ['email'],
    5: ['notification_hub'],
    6: ['credit_card'],
    7: ['notification_hub'],
    9: ['ecommerce'],
    10: ['credit_card'],
    12: ['email'],
    14: ['credit_card'],
    15: ['ecommerce', 'weather'],
    17: ['ecommerce', 'listing_platform'],
    18: ['credit_card'],
    20: ['credit_card'],
    21: ['calendar', 'ecommerce', 'credit_card', 'notification_hub', 'listing_platform'],
    22: ['ecommerce', 'delivery_logistics', 'credit_card', 'notification_hub'],
}

BUNDLE = {
    'user_id': 'usr_teng_qi',
    'candidate_groups': {
        'a': ('prod_psea_kit_a1', 'prod_psea_kit_a2', 'prod_psea_kit_a3'),
        'b': ('prod_psea_kit_b1', 'prod_psea_kit_b2', 'prod_psea_kit_b3'),
        'c': ('prod_psea_kit_c1', 'prod_psea_kit_c2', 'prod_psea_kit_c3'),
    },
    'coupon_codes': ('PSEA_ACC_15', 'PSEA_ACC_85', 'PSEA_ACC_120'),
    'comparison_date': '2026-06-22',
    'event_discovery_terms': ('Max 适配耳塞', 'Max 便携收纳', 'Max 音频转接'),
    'seed_order_ids': (
        'EC-20251220-N6W2', 'JD-20260106-H4V8', 'JD-20260518-7K2Q',
        'SF-20260422-M8D4', 'YT-20260309-P5R7', 'ZT-20260214-C9L3',
        'ord_psea_0001', 'ord_psea_0002',
    ),
    'original_cart': {
        'cart_psea_01': ('prod_psea_036', 'sku_prod_psea_036', 1, 24900),
        'cart_psea_02': ('prod_psea_042', 'sku_prod_psea_042', 1, 16900),
        'cart_psea_03': ('BENQ-SBH-2W7R', 'sku_BENQ-SBH-2W7R', 1, 129900),
        'cart_psea_04': ('prod_psea_040', 'sku_prod_psea_040', 1, 89900),
    },
}

REPORT = {
    'message_id': '<psea-price-report-0625@priceproof.cn>',
    'report_id': 'PSEA-COMP-0625',
    'partial_offer_minor': 189900,
    'full_amount_minor': 229900,
    'decision_terms': ('full price protection', 'marketplace review', 'continue submitting evidence'),
}

STATE = {
    'user_id': 'usr_teng_qi', 'product_id': 'prod_psea_main', 'sku_id': 'sku_psea_main',
    'primary_order': 'ord_psea_0001', 'secondary_order': 'ord_psea_0002', 'listing_id': 'lst_psea_0001',
    'refund_id': 'ref_psea_b', 'card_id': 'card_psea_01', 'fx_tx_id': 'tx_psea_fx',
    'dup_tx_id': 'tx_psea_dup', 'dispute_id': 'disp_psea_01', 'reversal_tx_id': 'tx_psea_rev',
    'funds_tx_id': 'tx_psea_pp', 'phish_message_id': '<20260618-tax@cn-earpresale-refund.com>',
    'offplatform_message_id': '<psea-deposit@trade.net>', 'weather_alert_id': 'alr_psea_stage15_storm',
    'geo_key': 'geo_psea', 'stage2_post': 'post_psea_terms_0616',
    'stage2_notification': 'ntf_psea_terms_0616', 'stage3_notification': 'ntf_psea_b1',
    'stage5_post': 'post_psea_evidence_0619', 'stage5_notification': 'ntf_psea_evidence_0619',
    'stage7_notification': 'ntf_psea_cp', 'stage9_notification': 'ntf_psea_b2',
    'stage10_notification': 'ntf_psea_dup', 'stage14_notification': 'ntf_psea_disp',
    'stage18_notification': 'ntf_psea_rev', 'stage19_notification': 'ntf_psea_ship',
    'stage20_notification': 'ntf_psea_funds',
}
