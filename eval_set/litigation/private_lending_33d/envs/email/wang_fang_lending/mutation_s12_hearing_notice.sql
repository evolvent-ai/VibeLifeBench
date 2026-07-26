BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<lending-s12-hearing@hzxihu-court.gov.cn>', '电子送达：6月12日开庭传票',
       '杭州市西湖区人民法院电子送达 <service@hzxihu-court.gov.cn>', '["wang.fang@gmail.com"]', '[]', '[]',
       '2026-06-08T09:42:00+08:00',
       '（2026）浙0106民初08812号定于2026年6月12日9:30在西湖区人民法院第五法庭开庭。请携带身份证、借条原件、银行回单、微信记录及已提交证据的原件。',
       NULL, 0, 1, 1, NULL, NULL, '{"document":"开庭传票","hearing_at":"2026-06-12T09:30:00+08:00","courtroom":"第五法庭"}', NULL, 490,
       '2026-06-08T09:42:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<lending-s12-hearing@hzxihu-court.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
