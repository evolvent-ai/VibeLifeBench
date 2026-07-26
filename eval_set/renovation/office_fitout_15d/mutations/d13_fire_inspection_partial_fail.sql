-- D13 早间消防初检部分未通过：应急照明数量不足，等待当日整改复审。
UPDATE visa_applications
SET status = 'rfi',
    decision_day = 13,
    decision_note = '消防初检部分未通过：应急照明灯具实装 18 盏，规范要求 24 盏，疏散通道与紧急出口尚缺 6 盏。须完成加装、照度与间距复测后再放行。依据 rule_property_v3_013。',
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-14T07:00:00+08:00',
        'status', 'rfi',
        'actor', 'fire_authority',
        'note', '消防初检发现应急照明缺 6 盏，要求整改并复审。'
      )
    ),
    updated_at = '2026-07-14T07:00:00+08:00'
WHERE application_id = 'fire_inspection_app_001'
  AND updated_at < '2026-07-14T07:00:00+08:00';
