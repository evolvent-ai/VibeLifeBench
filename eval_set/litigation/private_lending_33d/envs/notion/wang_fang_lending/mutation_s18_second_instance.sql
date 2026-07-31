BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('lending_sys_s18_appeal', NULL, 'lending_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"二审状态：陈强不服一审判决并提起上诉，杭州市中级人民法院已受理。王芳为被上诉人，将另行收到上诉状副本、答辩和举证期限通知。","link":null},"plain_text":"二审状态：陈强不服一审判决并提起上诉，杭州市中级人民法院已受理。王芳为被上诉人，将另行收到上诉状副本、答辩和举证期限通知。"}]}}',
   0, 0, 180, '2026-06-18T13:50:00.000+08:00', '2026-06-18T13:50:00.000+08:00');
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
