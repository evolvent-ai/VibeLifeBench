BEGIN;
INSERT OR IGNORE INTO pages
  (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('lending_case_home', 'page', 'wang_fang_workspace_root', '陈强借款追偿·案件台账', 0,
   '2026-05-20T08:30:00.000+08:00', '2026-05-20T08:30:00.000+08:00',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"陈强借款追偿·案件台账","link":null},"plain_text":"陈强借款追偿·案件台账"}]}}', NULL, NULL);
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('lending_sys_s0_facts', NULL, 'lending_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"起始事实：王芳持有两张借条。第一笔借条载明40万元，2023年6月10日银行实际转账36万元；第二笔借条载明2023年9月15日现金20万元，暂无银行交付记录。两笔约定月息2分，借款到期后陈强于2025年2月归还2万元，其余未清偿。现有材料包括借条、转账、微信催收、还款和相关联系人信息。当前状态：准备核对程序、诉求与证据。","link":null},"plain_text":"起始事实：王芳持有两张借条。第一笔借条载明40万元，2023年6月10日银行实际转账36万元；第二笔借条载明2023年9月15日现金20万元，暂无银行交付记录。两笔约定月息2分，借款到期后陈强于2025年2月归还2万元，其余未清偿。现有材料包括借条、转账、微信催收、还款和相关联系人信息。当前状态：准备核对程序、诉求与证据。"}]}}',
   0, 0, 0, '2026-05-20T08:30:00.000+08:00', '2026-05-20T08:30:00.000+08:00');
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key IN ('page_seq','block_seq');
COMMIT;
