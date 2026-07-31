BEGIN;
DELETE FROM messages WHERE message_id = 'email_water_notice_0716@venue.invalid';
INSERT INTO messages (
  folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json,
  date, body_text, body_html, is_read, is_important, is_flagged,
  in_reply_to, references_header, headers_json, uid, size, created_at
) VALUES (
  (SELECT id FROM folders WHERE name = 'INBOX'),
  'email_water_notice_0716@venue.invalid',
  '苏州河码头水质与慢泳道提醒',
  'dock.ops@venue.invalid',
  '["chen.shan@example.invalid"]', '[]', '[]',
  '2026-07-16T12:00:00+08:00',
  '码头提示近期水质与慢泳道安排可能受天气影响；出发前应查询雷电、阵风和场地开放状态，预约仍需本人确认。',
  NULL, 0, 1, 0, NULL, NULL, '{}', 3202, 154,
  '2026-07-16T12:00:00+08:00'
);
UPDATE folders
SET message_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id),
    unread_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id AND is_read = 0)
WHERE name = 'INBOX';
COMMIT;
