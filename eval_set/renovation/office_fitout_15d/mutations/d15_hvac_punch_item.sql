-- D15 空调新风系统遗留缺陷进入 punch-list。
UPDATE advisories
SET level = 2,
    text = '陆家嘴金融中心交付前通告：本层空调新风系统在试运行中发现风量分配不均与冷凝水管坡度不足，已列入交付 punch-list，须在质保期内由施工方整改并复测。交付验收不因该项自动通过，需保留复测记录。依据 rule_property_009、rule_property_020。',
    updated_at = '2026-07-16T10:00:00+08:00'
WHERE country_code = 'CN'
  AND updated_at < '2026-07-16T10:00:00+08:00';
