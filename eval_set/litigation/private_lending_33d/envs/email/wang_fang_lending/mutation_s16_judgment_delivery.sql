BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<lending-s16-judgment@hzxihu-court.gov.cn>', '电子送达：一审民事判决书',
       '杭州市西湖区人民法院电子送达 <service@hzxihu-court.gov.cn>', '["wang.fang@gmail.com"]', '[]', '[]',
       '2026-06-16T09:52:00+08:00',
       '本案一审判决书已送达。判决支持实际出借本金36万元及按一年期LPR四倍计算的利息，并扣除已还2万元；驳回第二笔20万元现金借款及配偶、担保人共同清偿、精神损失和误工请求。上诉权利和期限见判决书尾部。',
       NULL, 0, 1, 1, NULL, NULL, '{"document":"一审民事判决书","case_no":"（2026）浙0106民初08812号","delivered_at":"2026-06-16"}', NULL, 650,
       '2026-06-16T09:52:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<lending-s16-judgment@hzxihu-court.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
