-- S23：门店盘点导致换班，与晚间复习块冲突。
INSERT INTO messages (folder_id,message_id,subject,from_addr,to_addr_json,date,body_text,is_read,is_important,is_flagged,created_at)
VALUES (1,'msg_inventory_shift','盘点换班通知','manager@anmin.example','["zhou.yun@example.test"]',
        '2026-09-26T17:05:00+08:00',
        '9 月 28 日全店盘点，当日班次统一调整为 14:00-22:00，中西成药区由你负责，请提前与同事对数。',
        0,0,0,'2026-09-26T17:05:00+08:00');
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id),
                   unread_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id AND is_read=0);
