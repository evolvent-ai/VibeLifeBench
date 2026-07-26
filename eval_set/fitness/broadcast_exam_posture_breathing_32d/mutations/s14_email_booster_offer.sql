BEGIN;
DELETE FROM messages WHERE message_id = 'mail_booster_offer_20261020';
INSERT INTO messages (
  folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json,
  date, body_text, body_html, is_read, is_important, is_flagged, headers_json, uid, size, created_at
) VALUES (
  (SELECT id FROM folders WHERE name = 'INBOX'),
  'mail_booster_offer_20261020', '考前 7 天冲刺陪练营锁位提醒',
  'training.center@example.edu', '["lin.yu@example.com"]', '[]', '[]',
  '2026-10-20T11:35:00+08:00',
  '考前 7 天冲刺陪练营剩余名额有限，费用 799 元，可由家长确认后锁位。请学生自行与家长沟通后再联系机构。',
  NULL, 0, 1, 0, '{}', 2500, 160, '2026-10-20T11:35:00+08:00'
);
UPDATE folders
SET message_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id),
    unread_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id AND is_read = 0)
WHERE name = 'INBOX';
COMMIT;
