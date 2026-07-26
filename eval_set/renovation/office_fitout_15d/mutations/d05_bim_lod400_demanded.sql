-- D5 平台二次补正：BIM 精度不足，要求 LOD400 并补机电综合管线碰撞检查。
UPDATE visa_applications
SET status = 'rfi',
    decision_day = 5,
    decision_note = '二次补正：已收 BIM 模型精度不足，要求 LOD400 并补交机电综合管线碰撞检查报告；强弱电负荷计算书需设计单位盖章。补正截止 2026-07-08 18:00。依据 rule_property_v3_005。',
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-06T09:00:00+08:00',
        'status', 'rfi',
        'actor', 'jingan_one_stop_portal',
        'note', '二次补正：BIM 需达 LOD400，附管线碰撞检查报告与盖章负荷计算书。'
      )
    ),
    updated_at = '2026-07-06T09:00:00+08:00'
WHERE application_id = 'commercial_fit_up_filing_001'
  AND updated_at < '2026-07-06T09:00:00+08:00';
