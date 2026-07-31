-- Stage 12 mutation: 表弟陈雨确认宁波接站时间。
--
-- 与 stage 10 的余款邮件同因：原本预置在 Stage 0 seed（date=2026-04-12），
-- 使得 s12 才应首次可见的接站时间在任务一开始就能查到。
-- 该事实是 check_s12_elder_friendly_ningbo_train 的判定依据之一，
-- 提前可见会让「按接站时间反推车次」的推理链在 s0 即可完成。
INSERT OR REPLACE INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html, is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at) VALUES (1012, 1, 'msg_cousin_pickup', '宁波接站时间', 'chen.yu@example.test', '["lin.che@example.test"]', '[]', '[]', '2026-04-12T20:18:00+08:00', '我 4 月 16 日 19:00 后能到宁波站北广场接姨妈，太晚的话老人会累，发车次和到站口即可。', NULL, 0, 0, 0, NULL, NULL, NULL, 1012, 49, '2026-04-12T20:18:00+08:00');
