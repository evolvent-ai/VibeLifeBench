BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('food_sys_s10_defense_received', NULL, 'food_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"送达事实：被告答辩材料已收到。争议涉及赔偿依据、购买前差评、无中文标签是否属于一般瑕疵以及涉案食品安全性；法院要求原告在期限内提交质证意见。","link":null},"plain_text":"送达事实：被告答辩材料已收到。争议涉及赔偿依据、购买前差评、无中文标签是否属于一般瑕疵以及涉案食品安全性；法院要求原告在期限内提交质证意见。"}]}}',
   0, 0, 20, '2026-06-04T09:05:00.000+08:00', '2026-06-04T09:05:00.000+08:00');
UPDATE pages SET last_edited_time='2026-06-04T09:05:00.000+08:00' WHERE page_id='food_case_home';
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
