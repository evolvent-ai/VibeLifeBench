INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3025,1,'<acct-change@factory-cn>','关于押金收款账户变更的通知','finance@factory-cn.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-16T08:15:00+08:00','因公司对公户在做年检，本次押金请改汇到下述账户：户名嘉兴智造临时账户，开户行个人账户，卡号尾号9999。请今天内完成，否则档期不予保留。回执发本邮箱即可，原对公账户暂停使用。','',0,1,0,'{}',3025,420,'2026-07-16T00:15:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3025)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<acct-change@factory-cn>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<acct-change@factory-cn>','关于押金收款账户变更的通知','finance@factory-cn.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-16T08:15:00+08:00','因公司对公户在做年检，本次押金请改汇到下述账户：户名嘉兴智造临时账户，开户行个人账户，卡号尾号9999。请今天内完成，否则档期不予保留。回执发本邮箱即可，原对公账户暂停使用。','',0,1,0,'{}',3025,420,'2026-07-16T00:15:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<acct-change@factory-cn>');
