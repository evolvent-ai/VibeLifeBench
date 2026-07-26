BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<food-s16-judgment@pudongcourt.gov.cn>', '判决书电子送达：（2026）沪0115民初18426号',
       '上海市浦东新区人民法院电子送达 <service@pudongcourt.gov.cn>', '["zhao.meng@gmail.com"]', '[]', '[]',
       '2026-06-16T09:52:00+08:00',
       '本院向你电子送达一审判决书。判决对涉案奶粉中文标签、代用茶成分、退款、惩罚性赔偿、就医损失和案件受理费分别作出认定。判决书末页载明上诉法院和上诉期间，请查收完整文书。',
       NULL, 0, 1, 1, '<food-s8-acceptance@pudongcourt.gov.cn>', '<food-s8-acceptance@pudongcourt.gov.cn>',
       '{"case_no":"（2026）沪0115民初18426号","document":"一审判决书"}', NULL, 580,
       '2026-06-16T09:52:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<food-s16-judgment@pudongcourt.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
