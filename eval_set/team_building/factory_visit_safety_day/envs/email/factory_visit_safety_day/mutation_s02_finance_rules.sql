INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3012,1,'<invoice-rule@finance>','财务：活动类支出的发票与收款方要求','finance@example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-03T10:45:00+08:00','三类支出必须拿到公司抬头增值税发票才能入账：包车、餐饮、保险。工厂如果只收押金不收活动费，押金也要走对公账户并留存收据。另外提醒一句，收款户名必须和合同主体一致；如果对方中途改口说换账户，一律先停下来找合同上的联系人核实，不要凭邮件就付。','',0,1,0,'{}',3012,460,'2026-07-03T02:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3012)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<invoice-rule@finance>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<invoice-rule@finance>','财务：活动类支出的发票与收款方要求','finance@example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-03T10:45:00+08:00','三类支出必须拿到公司抬头增值税发票才能入账：包车、餐饮、保险。工厂如果只收押金不收活动费，押金也要走对公账户并留存收据。另外提醒一句，收款户名必须和合同主体一致；如果对方中途改口说换账户，一律先停下来找合同上的联系人核实，不要凭邮件就付。','',0,1,0,'{}',3012,460,'2026-07-03T02:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<invoice-rule@finance>');
