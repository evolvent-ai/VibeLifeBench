BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<food-s13-inspector-pause@jianyan-sh.cn>', '检验委托状态变更：JY-006暂不能继续承接',
       '上海法律服务平台检验名录 <notice@jianyan-sh.cn>', '["zhao.meng@gmail.com"]', '[]', '[]',
       '2026-06-10T09:04:00+08:00',
       '名录资质状态更新：沪正检测技术有限公司（JY-006）的食品检验CMA资质暂停。该机构尚未出具你的委托报告，原定受理和报告安排无法继续，请及时确认样品交接及后续机构安排。',
       NULL, 0, 1, 1, NULL, NULL, '{"provider_id":"JY-006","status":"paused","report_status":"not_issued"}', NULL, 480,
       '2026-06-10T09:04:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<food-s13-inspector-pause@jianyan-sh.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
