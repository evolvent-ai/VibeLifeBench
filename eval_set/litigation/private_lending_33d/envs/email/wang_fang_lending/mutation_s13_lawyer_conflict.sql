BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<lending-s13-lawyer-conflict@zjlegal.example>', '代理关系变更：周敏律师需退出本案',
       '浙江法律服务平台 <case@zjlegal.example>', '["wang.fang@gmail.com"]', '[]', '[]',
       '2026-06-10T09:02:00+08:00',
       '周敏律师（LD-006）所在求是律师事务所与陈强常年顾问所在律所合并，形成利益冲突，周敏不能继续代理。平台已启动材料交接，请尽快确认后续代理安排；6月12日开庭时间不变。',
       NULL, 0, 1, 1, NULL, NULL, '{"event":"lawyer_withdraw","lawyer_id":"LD-006","reason":"利益冲突"}', NULL, 500,
       '2026-06-10T09:02:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<lending-s13-lawyer-conflict@zjlegal.example>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
