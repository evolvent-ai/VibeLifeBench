BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('lending_sys_s9_evidence', NULL, 'lending_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"系统送达登记：2026年6月2日收到举证通知，期限为收到之日起15日；同日收到财产保全裁定办理通知，法院开始办理查封或冻结手续。正式证据清单、程序意见及保全风险仍需王芳核对。","link":null},"plain_text":"系统送达登记：2026年6月2日收到举证通知，期限为收到之日起15日；同日收到财产保全裁定办理通知，法院开始办理查封或冻结手续。正式证据清单、程序意见及保全风险仍需王芳核对。"}]}}',
   0, 0, 90, '2026-06-02T09:20:00.000+08:00', '2026-06-02T09:20:00.000+08:00');
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
