-- Stage 2: manager's first August shift email arrives.
INSERT INTO messages (folder_id,message_id,subject,from_addr,to_addr_json,date,body_text,is_read,is_important,is_flagged,created_at) VALUES (1,'msg_shift_aug','8 月第一版排班','manager@anmin.example','["zhou.yun@example.test"]','2026-08-04T20:10:00+08:00','8 月 5 日早班，8 月 6 日晚班，8 月 8 日夜班；家庭照护请自行避开。',0,0,0,'2026-08-04T20:10:00+08:00');
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id), unread_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id AND is_read=0);
