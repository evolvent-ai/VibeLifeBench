BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<food-s7-store-status@youxiangou.com>', '优鲜购工单更新：环球优选店铺暂停营业',
       '优鲜购消费者服务 <service@youxiangou.com>', '["zhao.meng@gmail.com"]', '[]', '[]',
       '2026-05-30T09:02:00+08:00',
       '赵萌您好，关于订单YX20260418的经营者联系工单：环球优选店铺当前处于暂停营业状态，在线客服和登记电话暂时无法接通。平台正在复核经营者名称、地址和有效联系方式，后续结果将继续通过本工单发送。',
       NULL, 0, 1, 1, NULL, NULL, '{"case_ref":"food_2026_zm","ticket":"YX-RISK-0529"}', NULL, 460,
       '2026-05-30T09:02:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<food-s7-store-status@youxiangou.com>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
