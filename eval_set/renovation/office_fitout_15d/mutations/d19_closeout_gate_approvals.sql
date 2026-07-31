-- D19 空气质量复测和 punch-list 闭环，商业 handover 最终批准；保险保持有效。
UPDATE visa_applications
SET status = 'approved',
    decision_day = 19,
    decision_note = '商业 handover 最终批准：消防批准、强电条件已关闭、保险持续在保；CMA 空气质量复测达标，HVAC 与竣工资料 punch-list 已闭环。',
    answers_json = json_set(
      CASE WHEN json_valid(answers_json) THEN answers_json ELSE '{}' END,
      '$.fire_inspection_passed', 1,
      '$.electrical_load_passed', 1,
      '$.insurance_still_in_force', 1,
      '$.air_quality_passed', 1,
      '$.air_quality_retest_required', 0,
      '$.air_quality_report_ref', 'workspace:air_quality_cma_retest_d19.pdf',
      '$.as_built_drawings_ref', 'workspace:office_as_built_d19.pdf',
      '$.punch_list_closed', 1,
      '$.occupancy_certificate_ref', 'workspace:commercial_handover_approval_d19.pdf'
    ),
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-20T16:00:00+08:00',
        'status', 'approved',
        'actor', 'property_handover_desk',
        'note', '空气质量复测达标且 punch-list 闭环，商业 handover 最终批准。'
      )
    ),
    updated_at = '2026-07-20T16:00:00+08:00'
WHERE application_id = 'commercial_handover_001'
  AND updated_at < '2026-07-20T16:00:00+08:00';

UPDATE visa_applications
SET status = 'in_force',
    decision_day = 19,
    decision_note = '工程一切险及第三方责任险在商业 handover 批准时仍处于有效期。',
    updated_at = '2026-07-20T16:05:00+08:00'
WHERE application_id = 'insurance_certificate_001'
  AND updated_at < '2026-07-20T16:05:00+08:00';
