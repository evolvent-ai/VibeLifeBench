-- D14 消防已通过、强电附条件通过且保险在保，商业 handover 进入附条件批准。
UPDATE visa_applications
SET status = 'approved_with_conditions',
    decision_day = 14,
    decision_note = '商业 handover 附条件批准：消防复审已通过、强电取得附条件批准、保险持续在保。剩余条件包括关闭 HVAC punch-list、提交竣工图及入驻前空气质量复测。',
    answers_json = json_set(
      CASE WHEN json_valid(answers_json) THEN answers_json ELSE '{}' END,
      '$.fire_inspection_passed', 1,
      '$.electrical_load_passed', 1,
      '$.insurance_still_in_force', 1,
      '$.punch_list_closed', 0
    ),
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-15T09:00:00+08:00',
        'status', 'approved_with_conditions',
        'actor', 'property_handover_desk',
        'note', '消防、强电和保险 Gate 已满足，handover 附条件批准。'
      )
    ),
    updated_at = '2026-07-15T09:00:00+08:00'
WHERE application_id = 'commercial_handover_001'
  AND updated_at < '2026-07-15T09:00:00+08:00';
