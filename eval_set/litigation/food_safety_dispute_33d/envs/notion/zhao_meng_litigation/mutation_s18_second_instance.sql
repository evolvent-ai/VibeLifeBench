BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('food_sys_s18_appeal', NULL, 'food_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"二审送达事实：环球优选提出上诉，上海市第一中级人民法院登记案号（2026）沪01民终09651号；赵萌为被上诉人，待核对上诉状副本、答辩期限和二审举证事项。","link":null},"plain_text":"二审送达事实：环球优选提出上诉，上海市第一中级人民法院登记案号（2026）沪01民终09651号；赵萌为被上诉人，待核对上诉状副本、答辩期限和二审举证事项。"}]}}',
   0, 0, 50, '2026-06-18T13:54:00.000+08:00', '2026-06-18T13:54:00.000+08:00');
UPDATE pages SET last_edited_time='2026-06-18T13:54:00.000+08:00' WHERE page_id='food_case_home';
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
