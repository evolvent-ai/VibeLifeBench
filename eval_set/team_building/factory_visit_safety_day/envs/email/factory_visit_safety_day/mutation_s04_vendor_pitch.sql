INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3014,1,'<pitch@factory>','嘉兴智造：44人参访档期与报价','sales@factory.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-05T13:45:00+08:00','七月二十一日的档期还留着。四十四人按两组错峰进车间，含讲解和基础防护，参访费一万八千元，可开公司抬头发票。押金五千元在确认档期后交，参访结束十五个工作日退回。耳塞和防尘口罩属于升级包，要不要单独加。','',0,0,0,'{}',3014,430,'2026-07-05T05:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3014)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<pitch@factory>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<pitch@factory>','嘉兴智造：44人参访档期与报价','sales@factory.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-05T13:45:00+08:00','七月二十一日的档期还留着。四十四人按两组错峰进车间，含讲解和基础防护，参访费一万八千元，可开公司抬头发票。押金五千元在确认档期后交，参访结束十五个工作日退回。耳塞和防尘口罩属于升级包，要不要单独加。','',0,0,0,'{}',3014,430,'2026-07-05T05:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<pitch@factory>');
