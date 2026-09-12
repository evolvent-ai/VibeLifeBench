INSERT OR IGNORE INTO messages
  (id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
VALUES
  (8002,1,'msg_supplier_contract_invoice_0704','evidence record：5-7evidence record','sales.majun@example.invalid','["aygul.store@example.invalid"]','[]','[]','2026-07-04T10:30:00+08:00','evidence record、evidence record。evidence record；evidence record、evidence record。',NULL,0,1,1,'{"source":"supplier_documents"}',8002,67,'2026-07-04T10:30:00+08:00');
INSERT OR IGNORE INTO messages
  (id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
VALUES
  (8003,1,'msg_supplier_statement_v1_0704','evidence record：evidence record7evidence record4evidence record','finance@tianshan-herun.example','["aygul.store@example.invalid"]','[]','[]','2026-07-04T10:45:00+08:00','evidence record5evidence record7evidence record，evidence record；evidence record、evidence record。',NULL,0,1,1,'{"source":"supplier_reconciliation_v1"}',8003,61,'2026-07-04T10:45:00+08:00');
INSERT OR IGNORE INTO attachments
  (id,message_id,filename,content_type,size,content_b64,content_id)
VALUES
  (8102,8002,'contract_invoice_pack.txt','text/plain',97,'5Y+R56Wo5ZCI6K6hIDEyNjg0MC4wMCDlhYPjgIJJTlYtVFMtMDcyOC1EVVAg5LiOIFNOLTA3Mjgg5Lu35beuL+mHjeWkjemHkeminSAyNzgwLjAwIOWFg+W+heaguOOAgg==','cid_supplier_contract_0704');
INSERT OR IGNORE INTO attachments
  (id,message_id,filename,content_type,size,content_b64,content_id)
VALUES
  (8103,8003,'supplier_statement_v1.csv','text/csv',54,'cmVjb3JkZWRfcGF5bWVudHMsNjAwMDAuMDAKbWlzc2luZ19jYW5kaWRhdGUsMTUwMDAuMDAK','cid_supplier_statement_v1');
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id), unread_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id AND is_read=0);
