-- D5 工程一切险及第三方责任险生效，满足进场前置条件。
UPDATE visa_applications
SET status = 'in_force',
    decision_day = 5,
    decision_note = '工程一切险商业 fit-out 专项及第三方责任险已核验生效，保障期覆盖 2026-07-06 至 2026-08-31，可作为物业进场准入凭证。',
    answers_json = json_set(
      CASE WHEN json_valid(answers_json) THEN answers_json ELSE '{}' END,
      '$.policy_ref', 'ins_v3_011:office-fitout-20260706',
      '$.coverage_verified_at', '2026-07-06T06:30:00+08:00'
    ),
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-06T06:30:00+08:00',
        'status', 'in_force',
        'actor', 'property_insurance_desk',
        'note', '商业 fit-out 工程一切险及第三方责任险已核验生效。'
      )
    ),
    updated_at = '2026-07-06T06:30:00+08:00'
WHERE application_id = 'insurance_certificate_001'
  AND updated_at < '2026-07-06T06:30:00+08:00';
