BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<food-s12-hearing@pudongcourt.gov.cn>', '开庭传票：（2026）沪0115民初18426号',
       '上海市浦东新区人民法院电子送达 <service@pudongcourt.gov.cn>', '["zhao.meng@gmail.com"]', '[]', '[]',
       '2026-06-08T09:42:00+08:00',
       '本案定于2026年6月12日9时30分在上海市浦东新区人民法院第六法庭公开开庭。请携带身份证明、订单支付材料、商品页面和沟通记录、医疗票据、涉案食品实物及已经取得的检验材料原件。',
       NULL, 0, 1, 1, '<food-s8-acceptance@pudongcourt.gov.cn>', '<food-s8-acceptance@pudongcourt.gov.cn>',
       '{"case_no":"（2026）沪0115民初18426号","document":"开庭传票"}', NULL, 530,
       '2026-06-08T09:42:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<food-s12-hearing@pudongcourt.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
