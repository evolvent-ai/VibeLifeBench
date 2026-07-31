BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<lending-s10-defense@hzxihu-court.gov.cn>', '电子送达：陈强答辩状及证据目录',
       '杭州市西湖区人民法院电子送达 <service@hzxihu-court.gov.cn>', '["wang.fang@gmail.com"]', '[]', '[]',
       '2026-06-04T09:02:00+08:00',
       '陈强答辩称：第一笔借条写40万元，但王芳实际仅转账36万元，差额系预扣利息；第二笔20万元现金从未实际收到。附件包括答辩状、银行账户说明和证据目录，请原告准备质证意见。',
       NULL, 0, 1, 1, NULL, NULL, '{"document":"被告答辩状","issues":["实际到账36万元","现金20万元交付"]}', NULL, 560,
       '2026-06-04T09:02:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<lending-s10-defense@hzxihu-court.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
