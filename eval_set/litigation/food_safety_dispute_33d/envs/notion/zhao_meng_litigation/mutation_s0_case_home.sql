BEGIN;
INSERT OR IGNORE INTO pages
  (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('food_case_home', 'page', 'zhao_meng_workspace_root', '食品安全维权·案件台账', 0,
   '2026-05-20T08:30:00.000+08:00', '2026-05-20T08:30:00.000+08:00',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"食品安全维权·案件台账","link":null},"plain_text":"食品安全维权·案件台账"}]}}', NULL, NULL);
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('food_sys_s0_facts', NULL, 'food_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"起始事实：2026年4月18日在优鲜购环球优选店购买进口奶粉和代用茶，合计1880元；4月22日收货。奶粉包装无中文信息，代用茶页面存在疾病治疗宣传；赵萌保留订单、支付、开箱、沟通和就医材料。当前状态：准备核对维权路径和证据。","link":null},"plain_text":"起始事实：2026年4月18日在优鲜购环球优选店购买进口奶粉和代用茶，合计1880元；4月22日收货。奶粉包装无中文信息，代用茶页面存在疾病治疗宣传；赵萌保留订单、支付、开箱、沟通和就医材料。当前状态：准备核对维权路径和证据。"}]}}',
   0, 0, 0, '2026-05-20T08:30:00.000+08:00', '2026-05-20T08:30:00.000+08:00');
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key IN ('page_seq','block_seq');
COMMIT;
