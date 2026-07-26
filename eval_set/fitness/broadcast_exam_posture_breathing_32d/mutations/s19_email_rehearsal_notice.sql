BEGIN;
DELETE FROM messages WHERE message_id = 'mail_rehearsal_notice_20261025';
INSERT INTO messages (
  folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json,
  date, body_text, body_html, is_read, is_important, is_flagged, headers_json, uid, size, created_at
) VALUES (
  (SELECT id FROM folders WHERE name = 'INBOX'),
  'mail_rehearsal_notice_20261025', '模拟流程彩排物品提醒',
  'training.center@example.edu', '["lin.yu@example.com"]', '[]', '[]',
  '2026-10-25T15:28:00+08:00',
  '10 月 29 日 16:30-19:30 模拟流程彩排，请穿正式鞋，提前 20 分钟到场，自备稿件、水杯和围巾。',
  NULL, 0, 1, 0, '{}', 2501, 180, '2026-10-25T15:28:00+08:00'
);
UPDATE folders
SET message_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id),
    unread_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id AND is_read = 0)
WHERE name = 'INBOX';
COMMIT;
