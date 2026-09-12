INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3001,1,'<photo-rule@factory>','Temporary factory no-photography rule','security@factory.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-12T08:20:00+08:00','Photography is prohibited throughout the customer prototype area; only the lobby group-photo point is allowed.','',0,1,0,'{}',3001,100,'2026-07-12T00:20:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3001)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<photo-rule@factory>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<photo-rule@factory>','Temporary factory no-photography rule','security@factory.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-12T08:20:00+08:00','Photography is prohibited throughout the customer prototype area; only the lobby group-photo point is allowed.','',0,1,0,'{}',3001,100,'2026-07-12T00:20:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<photo-rule@factory>');
