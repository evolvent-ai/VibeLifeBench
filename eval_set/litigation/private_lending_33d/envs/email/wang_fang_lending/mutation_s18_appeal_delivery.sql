BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<lending-s18-appeal@hz-intermediate-court.gov.cn>', '应诉通知：陈强已提起上诉',
       '杭州市中级人民法院电子送达 <service@hz-intermediate-court.gov.cn>', '["wang.fang@gmail.com"]', '[]', '[]',
       '2026-06-18T13:52:00+08:00',
       '陈强不服（2026）浙0106民初08812号一审判决并提起上诉，本院已受理。王芳为被上诉人，上诉状副本、答辩和举证期限将另行送达。',
       NULL, 0, 1, 1, NULL, NULL, '{"document":"二审应诉通知","appellant":"陈强","respondent":"王芳"}', NULL, 470,
       '2026-06-18T13:52:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<lending-s18-appeal@hz-intermediate-court.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
