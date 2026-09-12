INSERT OR IGNORE INTO messages
  (id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
VALUES
  (8005,1,'msg_biscuit_discount_0710','evidence record','sales.majun@example.invalid','["aygul.store@example.invalid"]','[]','[]','2026-07-10T09:05:00+08:00','SN-0728 evidence record；evidence record 4200.00 evidence record，evidence record。',NULL,0,1,1,'{"source":"supplier_discount_proposal"}',8005,75,'2026-07-10T09:05:00+08:00');
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id), unread_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id AND is_read=0);
