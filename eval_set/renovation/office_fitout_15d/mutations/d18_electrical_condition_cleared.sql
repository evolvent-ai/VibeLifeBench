-- D18 主线升级与复测完成，解除强电附加条件。
UPDATE visa_applications
SET status = 'approved',
    decision_day = 18,
    decision_note = '强电主线升级已完成，第三方 CMA 复测为 4.25 kW/100㎡，达到 ≥4 kW/100㎡ 要求；D+30 条件提前闭环。',
    answers_json = json_set(
      CASE WHEN json_valid(answers_json) THEN answers_json ELSE '{}' END,
      '$.kW_per_100sqm_existing', 4.25,
      '$.load_test_report_ref', 'workspace:electrical_retest_cma_d18.pdf',
      '$.condition_closed_at', '2026-07-19T14:00:00+08:00'
    ),
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-19T14:00:00+08:00',
        'status', 'approved',
        'actor', 'power_authority',
        'note', '主线升级完成，CMA 复测 4.25 kW/100㎡，附加条件关闭。'
      )
    ),
    updated_at = '2026-07-19T14:00:00+08:00'
WHERE application_id = 'electrical_load_app_001'
  AND updated_at < '2026-07-19T14:00:00+08:00';
