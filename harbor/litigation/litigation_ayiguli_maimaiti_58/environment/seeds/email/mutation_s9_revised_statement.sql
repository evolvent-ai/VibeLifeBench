INSERT OR IGNORE INTO messages (id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
VALUES (9001,1,'email_supplier_statement_0712_v2','evidence record：evidence record','finance@tianshan-herun.example','["aygul.store@example.invalid"]','[]','[]','2026-07-12T08:05:00+08:00','evidence record，evidence record；evidence record。',NULL,0,1,1,'{"source":"supplier_reconciliation_v2"}',9001,146,'2026-07-12T08:05:00+08:00');
INSERT OR IGNORE INTO attachments (id,message_id,filename,content_type,size,content_b64,content_id)
VALUES (9101,9001,'supplier_statement_v2.csv','text/csv',64,'cmVjb3JkZWRfcGF5bWVudHMsNjAwMDAuMDAKbWlzc2luZ19jYW5kaWRhdGUsMTUwMDAuMDAK','cid_9101');
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id), unread_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id AND is_read=0);
