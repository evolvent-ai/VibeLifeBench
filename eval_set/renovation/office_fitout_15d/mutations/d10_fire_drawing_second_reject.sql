-- D10 消防图纸二次退回：应急照明布点与疏散指示间距不满足规范。
UPDATE visa_applications
SET status = 'rfi',
    decision_day = 10,
    decision_note = '消防图纸二次退回：应急照明布点密度与疏散指示灯间距不满足规范要求，疏散通道净宽标注缺失。请补正后重新提交。',
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-11T10:00:00+08:00',
        'status', 'rfi',
        'actor', 'fire_authority',
        'note', '消防图纸二次退回：应急照明布点、疏散指示间距、通道净宽标注需补正。'
      )
    ),
    updated_at = '2026-07-11T10:00:00+08:00'
WHERE application_id = 'fire_inspection_app_001'
  AND updated_at < '2026-07-11T10:00:00+08:00';
