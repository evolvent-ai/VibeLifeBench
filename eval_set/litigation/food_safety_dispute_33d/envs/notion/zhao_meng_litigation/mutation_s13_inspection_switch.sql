BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('food_sys_s13_inspector_status', NULL, 'food_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"检验委托状态：JY-006食品检验CMA资质暂停，报告尚未出具，原委托安排无法继续。样品交接、费用处理和是否另行委托均待赵萌确认。","link":null},"plain_text":"检验委托状态：JY-006食品检验CMA资质暂停，报告尚未出具，原委托安排无法继续。样品交接、费用处理和是否另行委托均待赵萌确认。"}]}}',
   0, 0, 30, '2026-06-10T09:06:00.000+08:00', '2026-06-10T09:06:00.000+08:00');
UPDATE pages SET last_edited_time='2026-06-10T09:06:00.000+08:00' WHERE page_id='food_case_home';
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
