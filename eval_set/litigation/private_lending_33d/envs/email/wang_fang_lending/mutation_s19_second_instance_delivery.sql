BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<lending-s19-response@hz-intermediate-court.gov.cn>', '电子送达：上诉状副本与二审答辩通知',
       '杭州市中级人民法院电子送达 <service@hz-intermediate-court.gov.cn>', '["wang.fang@gmail.com"]', '[]', '[]',
       '2026-06-20T08:52:00+08:00',
       '现送达陈强上诉状副本。王芳应在收到之日起15日内提交答辩状，并在举证期限内提交证据。二审围绕上诉请求范围审理；诉讼费用事项以本院后续通知为准。',
       NULL, 0, 1, 1, NULL, NULL, '{"document":"上诉状副本及答辩通知","received_at":"2026-06-20","response_days":15}', NULL, 510,
       '2026-06-20T08:52:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<lending-s19-response@hz-intermediate-court.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
