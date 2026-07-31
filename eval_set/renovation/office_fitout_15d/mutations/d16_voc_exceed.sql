-- D16 入驻前空气检测 TVOC 超标；通告升级并将 handover 退回补正，等待复测。
UPDATE advisories
SET level = 3,
    text = '陆家嘴金融中心入驻前空气质量通告：本层入驻前检测 TVOC 超出办公场所限值，甲醛在限值内。须持续机械通风并在复测达标后方可安排员工入驻；复测报告须由具备 CMA 资质的第三方出具。不得以“已通风数日”替代复测结论。依据 rule_property_009、rule_property_021。',
    updated_at = '2026-07-17T09:00:00+08:00'
WHERE country_code = 'CN'
  AND updated_at < '2026-07-17T09:00:00+08:00';

UPDATE visa_applications
SET status = 'rfi',
    decision_day = 16,
    decision_note = 'Handover 暂停：入驻前 CMA 空气检测显示 TVOC 超限。须完成机械通风、提交复测达标报告并关闭相关 punch-list 后重新放行。',
    answers_json = json_set(
      CASE WHEN json_valid(answers_json) THEN answers_json ELSE '{}' END,
      '$.air_quality_passed', 0,
      '$.air_quality_retest_required', 1
    ),
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-17T09:05:00+08:00',
        'status', 'rfi',
        'actor', 'property_handover_desk',
        'note', 'TVOC 超限，handover 暂停并要求 CMA 复测。'
      )
    ),
    updated_at = '2026-07-17T09:05:00+08:00'
WHERE application_id = 'commercial_handover_001'
  AND updated_at < '2026-07-17T09:05:00+08:00';
