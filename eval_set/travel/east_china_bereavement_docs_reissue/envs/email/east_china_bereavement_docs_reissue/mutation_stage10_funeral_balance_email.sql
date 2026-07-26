-- Stage 10 mutation: 殡仪馆在告别仪式次日发出余款结算提醒。
--
-- 该邮件此前不存在于任何 stage。原实现把它预置在 Stage 0 seed 中（date=2026-04-10，
-- 却在 2026-04-03 起就可被 ID 直查、search 和 list 读到），违反手册 §3.8.10 第 1/2 类泄露：
-- 后续记录直接写进 init.sql，且未提醒也已能查到。
-- 现改为在对应 stage 由事件注入，Stage 0 起该行物理不存在。
INSERT OR REPLACE INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html, is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at) VALUES (1010, 1, 'msg_funeral_balance', '殡仪馆余款提醒', 'funeral.home@example.test', '["lin.che@example.test"]', '[]', '[]', '2026-04-10T14:55:00+08:00', '尚有 4200 元余款待结清，可次日或分拆处理；如需今天付款请确认授权和收款信息。', NULL, 0, 0, 0, NULL, NULL, NULL, 1010, 41, '2026-04-10T14:55:00+08:00');
