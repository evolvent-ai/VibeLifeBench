BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<food-s10-defense@pudongcourt.gov.cn>', '电子送达：被告答辩状及证据目录',
       '上海市浦东新区人民法院电子送达 <service@pudongcourt.gov.cn>', '["zhao.meng@gmail.com"]', '[]', '[]',
       '2026-06-04T09:03:00+08:00',
       '本院向你送达被告答辩状及证据目录。答辩内容涉及惩罚性赔偿依据、购买前差评、中文标签问题是否影响食品安全以及涉案商品安全性。请在举证期限内核对附件并提交质证意见。',
       NULL, 0, 1, 1, '<food-s8-acceptance@pudongcourt.gov.cn>', '<food-s8-acceptance@pudongcourt.gov.cn>',
       '{"case_no":"（2026）沪0115民初18426号","document":"答辩状及证据目录"}', NULL, 610,
       '2026-06-04T09:03:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<food-s10-defense@pudongcourt.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
