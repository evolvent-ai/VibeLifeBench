BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('lending_sys_s8_docket', NULL, 'lending_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"系统送达登记：2026年6月1日，杭州市西湖区人民法院受理王芳诉陈强民间借贷纠纷，案号（2026）浙0106民初08812号。待核对举证通知、程序事项和后续开庭安排。","link":null},"plain_text":"系统送达登记：2026年6月1日，杭州市西湖区人民法院受理王芳诉陈强民间借贷纠纷，案号（2026）浙0106民初08812号。待核对举证通知、程序事项和后续开庭安排。"}]}}',
   0, 0, 80, '2026-06-01T09:30:00.000+08:00', '2026-06-01T09:30:00.000+08:00');
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
