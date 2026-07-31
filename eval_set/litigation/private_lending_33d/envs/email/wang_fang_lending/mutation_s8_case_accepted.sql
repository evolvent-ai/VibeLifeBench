BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<lending-s8-acceptance@hzxihu-court.gov.cn>', '电子送达：（2026）浙0106民初08812号受理通知书',
       '杭州市西湖区人民法院电子送达 <service@hzxihu-court.gov.cn>', '["wang.fang@gmail.com"]', '[]', '[]',
       '2026-06-01T09:32:00+08:00',
       '王芳：你诉陈强民间借贷纠纷一案已立案受理，案号（2026）浙0106民初08812号。本次送达包含受理通知、诉讼权利义务告知和电子送达确认，请核对当事人信息并关注后续通知。',
       NULL, 0, 1, 1, NULL, NULL, '{"document":"受理通知书","case_no":"（2026）浙0106民初08812号"}', NULL, 480,
       '2026-06-01T09:32:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<lending-s8-acceptance@hzxihu-court.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
