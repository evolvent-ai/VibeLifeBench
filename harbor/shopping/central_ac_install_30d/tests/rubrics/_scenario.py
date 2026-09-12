"""Scenario constants for the central-AC installation and after-sales task."""
from __future__ import annotations

STAGE_COUNT = 24
ALL_SERVERS = (
    'ecommerce', 'delivery_logistics', 'credit_card', 'email',
    'calendar', 'notification_hub', 'weather',
)
OUTPUT_PATHS = (
    '/workspace/gear_plan.md', '/workspace/budget.md', '/workspace/decision_log.md',
    '/workspace/risk_register.md', '/workspace/order_tracker.md', '/workspace/evidence_log.md',
    '/workspace/final_summary.md', '/workspace/HEARTBEAT.md',
)
THREAD_IDS = ['ord_iscac_0001', 'ord_iscac_0002', 'funds_iscac']
THREAD_LABELS = {
    'ord_iscac_0001': ['ord_iscac_0001', 'thread 1', 'line 1', 'model and credentials', 'installation verification'],
    'ord_iscac_0002': ['ord_iscac_0002', 'thread 2', 'line 2', 'rework work order', 'work-order thread'],
    'funds_iscac': ['funds_iscac', 'thread 3', 'line 3', 'fees and refund adjustments', 'funds thread'],
}
THREAD_TERMS = {
    'ord_iscac_0001': ['model', 'installer credentials', 'home-visit service code', 'coolmax', 'fee rules', 'acceptance'],
    'ord_iscac_0002': ['work order', 'installation quality', 'evidence', 'on-site video', 'platform review', 'quality inspection', 'deadline', 'rework'],
    'funds_iscac': ['installation fee', 'floor charges', 'materials charges', 'refund', 'refund adjustment', 'dispute', 'reversal', 'credited', 'funds'],
}
THREAD_EVIDENCE = {
    'ord_iscac_0001': ['model', 'home-visit service code', 'purchase receipt', 'installer credentials', 'fee rules'],
    'ord_iscac_0002': ['on-site video', 'problem photos', 'work-order id', 'chat record', 'quality report', 'deadline'],
    'funds_iscac': ['installation fee', 'floor charges', 'refund id', 'refund adjustment amount', 'reversal', 'credited'],
}
STAGE_EXPECTED_SERVERS = {
    0: ['ecommerce', 'delivery_logistics', 'credit_card'],
    1: ['ecommerce', 'delivery_logistics', 'credit_card'],
    2: ['ecommerce', 'notification_hub'],
    3: ['ecommerce', 'notification_hub'],
    4: ['email'],
    6: ['credit_card'],
    7: ['notification_hub'],
    9: ['ecommerce', 'notification_hub'],
    10: ['credit_card'],
    11: ['email'],
    12: ['email'],
    13: ['notification_hub'],
    14: ['credit_card'],
    15: ['weather', 'notification_hub'],
    18: ['credit_card'],
    19: ['ecommerce', 'notification_hub'],
    20: ['credit_card', 'notification_hub'],
}

STAGE_DATES = {
    0: '2026-06-15', 1: '2026-06-15', 2: '2026-06-16', 3: '2026-06-17',
    4: '2026-06-18', 5: '2026-06-19', 6: '2026-06-20', 7: '2026-06-21',
    8: '2026-06-22', 9: '2026-06-23', 10: '2026-06-24', 11: '2026-06-25',
    12: '2026-06-26', 13: '2026-06-28', 14: '2026-06-30', 15: '2026-07-02',
    16: '2026-07-04', 17: '2026-07-06', 18: '2026-07-08', 19: '2026-07-10',
    20: '2026-07-11', 21: '2026-07-12', 22: '2026-07-13', 23: '2026-07-14',
}
STAGE_THREADS = {
    0: THREAD_IDS, 1: THREAD_IDS, 2: [THREAD_IDS[0]], 3: [THREAD_IDS[1]],
    4: [], 5: THREAD_IDS, 6: [THREAD_IDS[2]], 7: [THREAD_IDS[1], THREAD_IDS[2]],
    8: [THREAD_IDS[1], THREAD_IDS[2]], 9: [THREAD_IDS[1]], 10: [THREAD_IDS[2]],
    11: [THREAD_IDS[1]], 12: [], 13: [THREAD_IDS[2]], 14: [THREAD_IDS[2]],
    15: [THREAD_IDS[1]], 16: THREAD_IDS, 17: [THREAD_IDS[1], THREAD_IDS[2]],
    18: [THREAD_IDS[2]], 19: [THREAD_IDS[1], THREAD_IDS[2]], 20: [THREAD_IDS[2]],
    21: THREAD_IDS, 22: THREAD_IDS, 23: THREAD_IDS,
}
CROSS_TRANSITION_STAGES = (3, 9, 11, 14, 18, 19, 20)
CROSS_MUTATION_EVENT_IDS = {
    3: ('S03_mut',), 9: ('S09_mut',), 11: ('S11_inspection_report_mutation',),
    14: ('S14_mut',), 18: ('S18_mut',), 19: ('S19_mut',), 20: ('S20_mut',),
}
FINAL_THREAD_REQUIREMENTS = {
    THREAD_IDS[0]: (
        ('ord_iscac_0001',), ('cmx-3r1-2074',), ('2025q4',),
        ('vrf-iscac-2074g',), ('installer credentials', 'licensed'), ('fee rules', 'floor charges'),
    ),
    THREAD_IDS[1]: (
        ('ord_iscac_0002',), ('ref_iscac_b',), ('approved', 'approved'),
        ('224', '22400'), ('qi-sz-0625',), ('platform review', 'quality report'),
    ),
    THREAD_IDS[2]: (
        ('funds_iscac',), ('disp_iscac_01',), ('approved', 'dispute approved'),
        ('tx_iscac_rev',), ('-216', '21600', 'reversal'),
        ('tx_iscac_pp',), ('-224', '22400', 'refund adjustment credited'),
    ),
}
STAGE_OBJECTS = {
    0: ('ord_iscac_0001', 'ord_iscac_0002', 'card_iscac_01'),
    1: ('ord_iscac_0001', 'ord_iscac_0002', 'card_iscac_01'),
    2: ('prod_iscac_main', 'cmx-3r1-2074', 'vrf-iscac-2074g', '2025q4'),
    3: ('ord_iscac_0002', 'ref_iscac_b', 'ntf_iscac_b1'),
    4: ('coolmax-refund.example', '15', '48'),
    5: ('ord_iscac_0001', 'ord_iscac_0002', 'funds_iscac'),
    6: ('card_iscac_01', 'tx_iscac_fx'),
    7: ('ord_iscac_0002', 'ntf_iscac_cp', '140'),
    8: ('ord_iscac_0002', 'bsk_iscac_a2', 'bsk_iscac_b2', 'bsk_iscac_c3'),
    9: ('ord_iscac_0002', 'ref_iscac_b', 'ntf_iscac_b2'),
    10: ('card_iscac_01', 'tx_iscac_dup'),
    11: ('ord_iscac_0002', 'qi-sz-0625', '224'),
    12: ('installer@service-mail.example', '500'),
    13: ('780', '450', '600', '224', '216'),
    14: ('disp_iscac_01', 'tx_iscac_dup'),
    15: ('alr_iscac_storm_20260702', 'ref_iscac_b', 'ord_iscac_0002'),
    16: ('ord_iscac_0001', 'ord_iscac_0002', 'qi-sz-0625', '780', '450', '600'),
    17: ('ord_iscac_0002', 'ref_iscac_b', 'qi-sz-0625'),
    18: ('disp_iscac_01', 'tx_iscac_rev'),
    19: ('ord_iscac_0002', 'ref_iscac_b', '224'),
    20: ('card_iscac_01', 'tx_iscac_pp', '224'),
    21: ('ord_iscac_0001', 'ord_iscac_0002', 'funds_iscac'),
    22: ('ord_iscac_0001', 'ord_iscac_0002', 'funds_iscac'),
    23: ('ord_iscac_0001', 'ord_iscac_0002', 'funds_iscac'),
}
STAGE_EXPECTED_STATES = {
    3: (('submitted',),),
    9: (('rejected', 'need_more_evidence', 'additional evidence'),),
    14: (('under_review', 'under review'),),
    18: (('approved', 'dispute approved'), ('tx_iscac_rev', 'reversal')),
    19: (('approved', 'approved'), ('refund_pending', 'credit pending', 'not credited')),
    20: (('refunded', 'credited', 'refunded'), ('tx_iscac_pp', '224')),
}

STAGE_RESULT_REQUIREMENTS = {
    2: (('cmx-3r1-2074',), ('2025q4',), ('vrf-iscac-2074g',)),
    3: (('ref_iscac_b',), ('submitted',)),
    7: (('ntf_iscac_cp',), ('140',)),
    9: (('ref_iscac_b',), ('rejected',)),
    10: (('tx_iscac_dup',),),
    11: (('qi-sz-0625',), ('224',)),
    14: (('disp_iscac_01',), ('under_review',)),
    15: (('alr_iscac_storm_20260702',),),
    18: (('disp_iscac_01',), ('approved',), ('tx_iscac_rev',)),
    19: (('ref_iscac_b',), ('approved',), ('22400', '224')),
    20: (('tx_iscac_pp',), ('-22400', '-224', '22400')),
}
