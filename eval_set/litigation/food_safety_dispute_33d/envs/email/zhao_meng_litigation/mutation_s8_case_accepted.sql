BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<food-s8-acceptance@pudongcourt.gov.cn>', '电子送达：（2026）沪0115民初18426号受理通知书',
       '上海市浦东新区人民法院电子送达 <service@pudongcourt.gov.cn>', '["zhao.meng@gmail.com"]', '[]', '[]',
       '2026-06-01T09:32:00+08:00',
       '赵萌：你诉杭州环球优选食品有限公司等网络购物合同纠纷一案已立案受理，案号（2026）沪0115民初18426号。本次送达包含受理通知书、举证通知和电子送达确认说明，请核对当事人信息并关注后续检验与开庭安排。',
       NULL, 0, 1, 1, NULL, NULL, '{"case_no":"（2026）沪0115民初18426号","document":"受理通知书"}', NULL, 520,
       '2026-06-01T09:32:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<food-s8-acceptance@pudongcourt.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
