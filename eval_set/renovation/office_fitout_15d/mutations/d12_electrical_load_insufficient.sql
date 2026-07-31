-- D12 现场实测供电容量不足，退回要求扩容方案。
-- 注意：实测数值只落在后端 decision_note，Stage 0 的任何位置都不得预告。
UPDATE visa_applications
SET status = 'rfi',
    decision_day = 12,
    decision_note = '现场实测：既有供电容量 3kW/100㎡，低于本次 fit-up 办公场景所需 4kW/100㎡，缺口需通过增容或负荷重分配解决。请提交扩容方案与费用测算后复审。',
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-13T11:00:00+08:00',
        'status', 'rfi',
        'actor', 'power_authority',
        'note', '现场实测供电容量 3kW/100㎡，不满足 4kW/100㎡ 要求，需提交扩容方案。'
      )
    ),
    updated_at = '2026-07-13T11:00:00+08:00'
WHERE application_id = 'electrical_load_app_001'
  AND updated_at < '2026-07-13T11:00:00+08:00';
