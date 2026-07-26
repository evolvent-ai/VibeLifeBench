-- D13 双复核放行：消防复审通过；强电复测临界通过（附整改条件）。
UPDATE visa_applications
SET status = 'approved',
    decision_day = 13,
    decision_note = '消防复审通过（2026-07-14 12:00）：应急照明补装完成；西侧主疏散间距 27.5m、东侧紧急出口 28m，均 ≤30m；实测照度疏散 6.2 Lx、出口 12 Lx，均达标。消防大队与验收科已签章。',
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-14T12:00:00+08:00',
        'status', 'approved',
        'actor', 'fire_authority',
        'note', '消防复审通过，应急照明补装完成，间距与照度均达标。'
      )
    ),
    updated_at = '2026-07-14T12:00:00+08:00'
WHERE application_id = 'fire_inspection_app_001'
  AND updated_at < '2026-07-14T12:00:00+08:00';

UPDATE visa_applications
SET status = 'approved_with_conditions',
    decision_day = 13,
    decision_note = '强电复测附条件通过（2026-07-14 12:30）：第三方 CMA 实测 3.95 kW/100㎡。条件：入驻后 30 日内完成主线升级至 4.2+ kW/100㎡并提交复测报告，计入售后 punch-list。',
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-14T12:30:00+08:00',
        'status', 'approved_with_conditions',
        'actor', 'power_authority',
        'note', '强电复测附条件通过，须在入驻后 30 日内升级至 4.2+ kW/100㎡。'
      )
    ),
    updated_at = '2026-07-14T12:30:00+08:00'
WHERE application_id = 'electrical_load_app_001'
  AND updated_at < '2026-07-14T12:30:00+08:00';
