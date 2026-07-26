-- D6 一件事平台补正材料核验完成，商业 fit-up 备案批准。
UPDATE visa_applications
SET status = 'approved',
    decision_day = 6,
    decision_note = '静安装饰装修一件事平台已核验 LOD400 BIM、机电碰撞检查、盖章负荷计算书及消防平面图；commercial fit-up 备案批准，可在保险持续有效及物业时段约束下施工。',
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-07T08:30:00+08:00',
        'status', 'approved',
        'actor', 'jingan_one_stop_portal',
        'note', '补正材料核验完成，商业 fit-up 备案批准。'
      )
    ),
    updated_at = '2026-07-07T08:30:00+08:00'
WHERE application_id = 'commercial_fit_up_filing_001'
  AND updated_at < '2026-07-07T08:30:00+08:00';
