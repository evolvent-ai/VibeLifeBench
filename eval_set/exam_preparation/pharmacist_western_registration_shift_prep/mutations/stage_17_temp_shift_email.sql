-- S17：店长临时加夜班，与既有复习安排冲突。
INSERT INTO messages (folder_id,message_id,subject,from_addr,to_addr_json,date,body_text,is_read,is_important,is_flagged,created_at)
VALUES (1,'msg_temp_shift','9 月临时夜班调整','manager@anmin.example','["zhou.yun@example.test"]',
        '2026-09-06T18:10:00+08:00',
        '9 月 8 日临时新增夜班（22:00 收班），9 月 9 日上午请安排休息，不排班。请自行调整当日其他安排。',
        0,0,0,'2026-09-06T18:10:00+08:00');
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id),
                   unread_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id AND is_read=0);
