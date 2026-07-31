BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('food_sys_s8_docket', NULL, 'food_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"法院送达事实：浦东法院已受理案件，案号（2026）沪0115民初18426号；已收到受理通知和举证说明，后续需关注检验、举证和开庭安排。","link":null},"plain_text":"法院送达事实：浦东法院已受理案件，案号（2026）沪0115民初18426号；已收到受理通知和举证说明，后续需关注检验、举证和开庭安排。"}]}}',
   0, 0, 10, '2026-06-01T09:33:00.000+08:00', '2026-06-01T09:33:00.000+08:00');
UPDATE pages SET last_edited_time='2026-06-01T09:33:00.000+08:00' WHERE page_id='food_case_home';
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
