BEGIN;
DELETE FROM messages WHERE message_id = 'email_team_update_037@dragon.invalid';
INSERT INTO messages (
  folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json,
  date, body_text, body_html, is_read, is_important, is_flagged,
  in_reply_to, references_header, headers_json, uid, size, created_at
) VALUES (
  (SELECT id FROM folders WHERE name = 'INBOX'),
  'email_team_update_037@dragon.invalid',
  '龙舟队修订训练安排与报名截止',
  'captain.li@example.invalid',
  '["chen.shan@example.invalid"]', '[]', '[]',
  '2026-07-24T09:15:00+08:00',
  '修订：7 月 29 日晚新增干划课；8 月 3 日 18:00 前由本人确认报名。队长不接受助理代回复。',
  NULL, 0, 1, 1, NULL, NULL, '{}', 3301, 108,
  '2026-07-24T09:15:00+08:00'
);
UPDATE folders
SET message_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id),
    unread_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id AND is_read = 0)
WHERE name = 'INBOX';
COMMIT;
