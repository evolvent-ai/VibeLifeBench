-- D4 同层其他办公室投诉噪音，物业收紧噪音作业窗口。advisory 级别 1 → 2。
UPDATE advisories
SET level = 2,
    text = '陆家嘴金融中心写字楼装修合规通告（更新）：本层已收到相邻租户噪音投诉，噪音作业窗口收紧为工作日 09:00-11:30 与 14:00-17:00，其余时段仅可进行无噪音工序。装修备案须先于任何拆除或施工日程；业主、施工方与物业须共同签署装修管理协议。依据 rule_property_001、rule_property_006、rule_property_016。',
    updated_at = '2026-07-05T08:00:00+08:00'
WHERE country_code = 'CN'
  AND updated_at < '2026-07-05T08:00:00+08:00';
