-- D13 双复审前，物业明确 handover 仍受消防、强电和保险三项 Gate 约束。
UPDATE advisories
SET level = 3,
    text = '陆家嘴金融中心交付 Gate 通告：商业 handover 只有在消防复审通过、强电复测至少取得附条件批准、工程一切险持续在保后方可启动；任何一项未闭环均不得安排正式入驻。复审证据须保存至项目台账。',
    updated_at = '2026-07-14T09:00:00+08:00'
WHERE country_code = 'CN'
  AND updated_at < '2026-07-14T09:00:00+08:00';
