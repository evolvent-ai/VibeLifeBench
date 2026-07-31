BEGIN;
DELETE FROM messages WHERE message_id = 'mail_exam_notice_20261007';
INSERT INTO messages (
  folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json,
  date, body_text, body_html, is_read, is_important, is_flagged, headers_json, uid, size, created_at
) VALUES (
  (SELECT id FROM folders WHERE name = 'INBOX'),
  'mail_exam_notice_20261007',
  '校内模拟面试与冲刺周安排',
  'training.center@example.edu',
  '["lin.yu@example.com"]', '[]', '[]',
  '2026-10-07T12:02:00+08:00',
  '11 月 5 日举行校内模拟面试；10 月 28 日后进入冲刺周。家长沟通事项请学生本人转达，机构不会代替学生确认报名或付款。',
  NULL, 0, 1, 0, '{}', 2401, 196,
  '2026-10-07T12:02:00+08:00'
);
UPDATE folders
SET message_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id),
    unread_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id AND is_read = 0)
WHERE name = 'INBOX';
COMMIT;
