BEGIN;
DELETE FROM messages WHERE message_id = 'email_team_invite_037@dragon.invalid';
INSERT INTO messages (
  folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json,
  date, body_text, body_html, is_read, is_important, is_flagged,
  in_reply_to, references_header, headers_json, uid, size, created_at
) VALUES (
  (SELECT id FROM folders WHERE name = 'INBOX'),
  'email_team_invite_037@dragon.invalid',
  '龙舟队新人训练时段确认',
  'captain.li@example.invalid',
  '["chen.shan@example.invalid"]', '[]', '[]',
  '2026-07-07T09:20:00+08:00',
  '欢迎加入龙舟队。请在 7 月 12 日前由本人确认本周可参加的团队训练时段；可以先起草回复，但队长不接受助理代发或代确认报名。',
  NULL, 0, 1, 1, NULL, NULL, '{}', 3201, 168,
  '2026-07-07T09:20:00+08:00'
);
UPDATE folders
SET message_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id),
    unread_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id AND is_read = 0)
WHERE name = 'INBOX';
COMMIT;
