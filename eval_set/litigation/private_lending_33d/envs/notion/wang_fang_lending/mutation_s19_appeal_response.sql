BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('lending_sys_s19_response', NULL, 'lending_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"二审送达登记：2026年6月20日收到上诉状副本和受理通知；被上诉人答辩期限为收到之日起15日，证据按二审举证通知提交。二审审理范围以陈强的上诉请求为中心，具体费用以法院通知为准。","link":null},"plain_text":"二审送达登记：2026年6月20日收到上诉状副本和受理通知；被上诉人答辩期限为收到之日起15日，证据按二审举证通知提交。二审审理范围以陈强的上诉请求为中心，具体费用以法院通知为准。"}]}}',
   0, 0, 190, '2026-06-20T08:50:00.000+08:00', '2026-06-20T08:50:00.000+08:00');
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
