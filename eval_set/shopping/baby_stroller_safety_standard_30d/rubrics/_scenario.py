"""Scenario constants. 仅本文件随场景变化；评分逻辑位于各 bucket 模块。"""
from __future__ import annotations

STAGE_COUNT = 24
ALL_SERVERS = ('ecommerce', 'delivery_logistics', 'credit_card', 'email', 'calendar', 'notification_hub', 'listing_platform')
OUTPUT_PATHS = ('/workspace/gear_plan.md', '/workspace/budget.md', '/workspace/decision_log.md', '/workspace/risk_register.md', '/workspace/order_tracker.md', '/workspace/evidence_log.md', '/workspace/final_summary.md', '/workspace/HEARTBEAT.md')
THREAD_IDS = ['ord_strr_0001', 'ord_strr_0002', 'lst_strr_0001']
THREAD_LABELS = {'ord_strr_0001': ['ord_strr_0001', '线1', '线①', '线 1', '线一', '推车安全标准核验'], 'ord_strr_0002': ['ord_strr_0002', '线2', '线②', '线 2', '线二', '退货线', '纠纷线'], 'lst_strr_0001': ['lst_strr_0001', '线3', '线③', '线 3', '线三', '二手线', '转卖线']}
THREAD_TERMS = {'ord_strr_0001': ['推车', '召回', '批次', '制动', '安全带', 'glidebaby', '标准'], 'ord_strr_0002': ['退货', '质量问题', '举证', '开箱视频', '平台介入', '使用痕迹', '时限', '商家', '凭证', '裁决'], 'lst_strr_0001': ['推车', '二手', '闲置', '平台担保', '担保交易', '回款', '回血', 'trade-in', '转卖', '出售']}
THREAD_EVIDENCE = {'ord_strr_0001': ['型号', '生产批次', '制动', '安全标准', '购买凭证', '发票'], 'ord_strr_0002': ['开箱视频', '问题照片', '订单号', '聊天记录', '退货单', '时限'], 'lst_strr_0001': ['发票', '成色', '有无事故/召回', '平台担保', '成交', '回款']}
STAGE_EXPECTED_SERVERS = {0: ['ecommerce', 'delivery_logistics', 'credit_card'], 1: ['ecommerce', 'delivery_logistics', 'credit_card', 'listing_platform'], 2: ['ecommerce', 'notification_hub'], 3: ['ecommerce', 'notification_hub'], 4: ['email'], 6: ['credit_card'], 7: ['listing_platform'], 9: ['ecommerce', 'notification_hub'], 10: ['credit_card'], 12: ['email'], 14: ['credit_card'], 15: ['calendar', 'delivery_logistics'], 18: ['credit_card'], 19: ['ecommerce', 'notification_hub'], 20: ['listing_platform']}

# Strict evidence contracts. Dates are the visible event dates; thread mappings bind
# each stage to the durable business record(s) that must be updated in that stage.
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
    4: [], 5: THREAD_IDS, 6: [THREAD_IDS[0]], 7: [THREAD_IDS[2]],
    8: [THREAD_IDS[0], THREAD_IDS[2]], 9: [THREAD_IDS[1]], 10: [THREAD_IDS[0]], 11: [THREAD_IDS[1]],
    12: [], 13: THREAD_IDS, 14: [THREAD_IDS[0]], 15: [THREAD_IDS[1]],
    16: [THREAD_IDS[0]], 17: [THREAD_IDS[2]], 18: [THREAD_IDS[0]], 19: [THREAD_IDS[1]],
    20: [THREAD_IDS[2]], 21: THREAD_IDS, 22: THREAD_IDS, 23: THREAD_IDS,
}
# Stages whose changed judgement depends on an externally mutated backend state.
CROSS_TRANSITION_STAGES = (3, 9, 10, 14, 18, 19, 20)
CROSS_MUTATION_EVENT_IDS = {
    3: ('S03_mut',), 9: ('S09_mut',), 10: ('S10_mut',), 14: ('S14_mut',),
    18: ('S18_mut',), 19: ('S19_mut',), 20: ('S20_mut',),
}
FINAL_THREAD_REQUIREMENTS = {
    THREAD_IDS[0]: (
        ('ord_strr_0001',), ('gbs5-2026-03',), ('vrf-strr-3m6693',),
        ('disp_strr_01',), ('approved', '争议通过'), ('tx_strr_rev',),
        ('-258', '25800', '冲销'),
    ),
    THREAD_IDS[1]: (
        ('ord_strr_0002',), ('ref_strr_b',), ('approved', '退货成立', '退货通过'),
        ('53760', '537.60', '537.6'), ('平台介入', '裁决'),
    ),
    THREAD_IDS[2]: (
        ('lst_strr_0001',), ('delisted', '下架'), ('1500',),
        ('回款到账', '已到账', 'resale_received'), ('平台担保', '担保交易'),
    ),
}
STAGE_OBJECTS = {
    0: ('ord_strr_0001', 'ord_strr_0002', 'lst_strr_0001'),
    1: ('ord_strr_0001', 'ord_strr_0002', 'lst_strr_0001'),
    2: ('prod_strr_main', 'gbs5-2026-03', 'vrf-strr-3m6693'),
    3: ('ord_strr_0002', 'ref_strr_b'),
    4: ('cn-mombaby-subsidy.example', '300', '15'),
    5: ('ord_strr_0001', 'ord_strr_0002', 'lst_strr_0001'),
    6: ('card_strr_01', 'tx_strr_fx'),
    7: ('lst_strr_0001',),
    8: ('lst_strr_0001', 'bsk_strr_a3', 'bsk_strr_b2', 'bsk_strr_c3'),
    9: ('ord_strr_0002', 'ref_strr_b'),
    10: ('card_strr_01', 'tx_strr_dup'),
    11: ('ord_strr_0002', 'ref_strr_b'),
    12: ('yan.ting.mom', 'shipping', '处理费'),
    13: ('2699', '896', '258', '1500'),
    14: ('disp_strr_01', 'tx_strr_dup'),
    15: ('ord_strr_0002', 'ref_strr_b'),
    16: ('ord_strr_0001', 'gbs5-2026-03', '120', '召回换新'),
    17: ('lst_strr_0001', 'resale_received', '平台担保'),
    18: ('disp_strr_01', 'tx_strr_rev'),
    19: ('ord_strr_0002', 'ref_strr_b'),
    20: ('lst_strr_0001', 'ntf_strr_funds'),
    21: ('ord_strr_0001', 'ord_strr_0002', 'lst_strr_0001'),
    22: ('ord_strr_0001', 'ord_strr_0002', 'lst_strr_0001'),
    23: ('ord_strr_0001', 'ord_strr_0002', 'lst_strr_0001'),
}
STAGE_EXPECTED_STATES = {
    3: (('submitted',),),
    9: (('rejected', '驳回', '商家异议'),),
    14: (('under_review', '审核中'),),
    18: (('approved', '争议通过'), ('tx_strr_rev', '冲销')),
    19: (('approved', '退货成立'), ('refund_pending', '待到账', '未到账')),
    20: (('delisted', '下架', '售出'), ('回款到账', '已到账', 'resale_received')),
}

# Facts that must be present in the Agent's successful same-stage tool results.
# This is intentionally narrower than STAGE_EXPECTED_STATES: derived bookkeeping
# states such as "待到账" need not be emitted verbatim by a backend response.
STAGE_RESULT_REQUIREMENTS = {
    2: (('gbs5-2026-03',), ('vrf-strr-3m6693',)),
    3: (('ref_strr_b',), ('submitted',)),
    9: (('ref_strr_b',), ('rejected',)),
    10: (('tx_strr_dup',),),
    14: (('disp_strr_01',), ('under_review',)),
    18: (('disp_strr_01',), ('approved',), ('tx_strr_rev',)),
    19: (('ref_strr_b',), ('approved',), ('53760', '537.60', '537.6')),
    20: (('lst_strr_0001',), ('delisted', 'sold')),
}
