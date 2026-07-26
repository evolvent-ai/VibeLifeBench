BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('lending_sys_s13_lawyer', NULL, 'lending_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"系统状态：原代理律师周敏（LD-006）因所在律所合并后与陈强常年顾问所在律所产生利益冲突，已通知退出代理。2026年6月12日开庭安排不变，需尽快完成材料交接和代理选择确认。","link":null},"plain_text":"系统状态：原代理律师周敏（LD-006）因所在律所合并后与陈强常年顾问所在律所产生利益冲突，已通知退出代理。2026年6月12日开庭安排不变，需尽快完成材料交接和代理选择确认。"}]}}',
   0, 0, 130, '2026-06-10T09:00:00.000+08:00', '2026-06-10T09:00:00.000+08:00');
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
