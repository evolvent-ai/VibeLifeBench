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
    'ord_iscac_0001': ['ord_iscac_0001', '线1', '线①', '线 1', '线一', '机型与资质', '安装核验'],
    'ord_iscac_0002': ['ord_iscac_0002', '线2', '线②', '线 2', '线二', '返工工单', '工单线'],
    'funds_iscac': ['funds_iscac', '线3', '线③', '线 3', '线三', '费用与退补差', '资金线'],
}
THREAD_TERMS = {
    'ord_iscac_0001': ['机型', '安装资质', '上门服务码', 'coolmax', '收费标准', '验收'],
    'ord_iscac_0002': ['工单', '安装质量', '举证', '上门视频', '平台核对', '质检', '时限', '返工'],
    'funds_iscac': ['安装费', '楼层费', '辅料费', '退费', '退补差', '争议', '冲销', '到账', '资金'],
}
THREAD_EVIDENCE = {
    'ord_iscac_0001': ['机型', '上门服务码', '购机凭证', '安装资质', '收费标准'],
    'ord_iscac_0002': ['上门视频', '问题照片', '工单号', '聊天记录', '质检报告', '时限'],
    'funds_iscac': ['安装费', '楼层费', '退款单号', '退补差金额', '冲销', '到账'],
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
        ('vrf-iscac-2074g',), ('安装资质', '持证'), ('收费标准', '楼层费'),
    ),
    THREAD_IDS[1]: (
        ('ord_iscac_0002',), ('ref_iscac_b',), ('approved', '获批'),
        ('224', '22400'), ('qi-sz-0625',), ('平台核对', '质检报告'),
    ),
    THREAD_IDS[2]: (
        ('funds_iscac',), ('disp_iscac_01',), ('approved', '争议通过'),
        ('tx_iscac_rev',), ('-216', '21600', '冲销'),
        ('tx_iscac_pp',), ('-224', '22400', '退补差到账'),
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
    9: (('rejected', 'need_more_evidence', '补证'),),
    14: (('under_review', '审核中'),),
    18: (('approved', '争议通过'), ('tx_iscac_rev', '冲销')),
    19: (('approved', '获批'), ('refund_pending', '待到账', '未到账')),
    20: (('refunded', '到账', '已退'), ('tx_iscac_pp', '224')),
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
