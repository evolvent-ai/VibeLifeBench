BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<food-s18-appeal@sh1court.gov.cn>', '二审电子送达：（2026）沪01民终09651号上诉事项通知',
       '上海市第一中级人民法院电子送达 <service@sh1court.gov.cn>', '["zhao.meng@gmail.com"]', '[]', '[]',
       '2026-06-18T13:52:00+08:00',
       '环球优选不服（2026）沪0115民初18426号民事判决提出上诉，本院已登记为（2026）沪01民终09651号。你为被上诉人，上诉状副本、答辩说明和二审举证事项将随本邮件送达。',
       NULL, 0, 1, 1, '<food-s16-judgment@pudongcourt.gov.cn>', '<food-s16-judgment@pudongcourt.gov.cn>',
       '{"appeal_no":"（2026）沪01民终09651号","document":"上诉事项通知"}', NULL, 560,
       '2026-06-18T13:52:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<food-s18-appeal@sh1court.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
