BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('food_sys_s16_judgment', NULL, 'food_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"判决送达事实：一审判决书已收到。法院对奶粉中文标签、代用茶成分、退款、惩罚性赔偿、就医损失和案件受理费作出裁判；完整判项和上诉权利以送达文书为准。","link":null},"plain_text":"判决送达事实：一审判决书已收到。法院对奶粉中文标签、代用茶成分、退款、惩罚性赔偿、就医损失和案件受理费作出裁判；完整判项和上诉权利以送达文书为准。"}]}}',
   0, 0, 40, '2026-06-16T09:54:00.000+08:00', '2026-06-16T09:54:00.000+08:00');
UPDATE pages SET last_edited_time='2026-06-16T09:54:00.000+08:00' WHERE page_id='food_case_home';
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
