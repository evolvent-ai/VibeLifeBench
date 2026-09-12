INSERT OR IGNORE INTO messages
  (id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
VALUES
  (8004,1,'msg_milk_cold_chain_0708','evidence record','sales.majun@example.invalid','["aygul.store@example.invalid"]','[]','[]','2026-07-08T12:00:00+08:00','ML-0705 evidence record，evidence record。evidence record；evidence record。',NULL,0,1,1,'{"source":"supplier_batch_communication"}',8004,71,'2026-07-08T12:00:00+08:00');
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id), unread_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id AND is_read=0);
