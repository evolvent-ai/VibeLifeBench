INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3033,1,'<inv-bus@bus>','沪嘉包车：七月二十一日包车发票已开','ops@bus.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-24T08:45:00+08:00','包车费一万两千八百元的公司抬头发票已开具并寄出，发票号尾号4471，行程单随票附上。','',0,0,0,'{}',3033,300,'2026-07-24T00:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3033)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<inv-bus@bus>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<inv-bus@bus>','沪嘉包车：七月二十一日包车发票已开','ops@bus.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-24T08:45:00+08:00','包车费一万两千八百元的公司抬头发票已开具并寄出，发票号尾号4471，行程单随票附上。','',0,0,0,'{}',3033,300,'2026-07-24T00:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<inv-bus@bus>');
INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3034,1,'<inv-lunch@lunch>','禾城协作：午餐发票与结算单','service@lunch.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-24T08:50:00+08:00','四十二人实际用餐，按合同就低结算一万一千三百四十元，公司抬头发票已开，素食三份与清真两份单独计价已并入总额。','',0,0,0,'{}',3034,320,'2026-07-24T00:50:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3034)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<inv-lunch@lunch>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<inv-lunch@lunch>','禾城协作：午餐发票与结算单','service@lunch.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-24T08:50:00+08:00','四十二人实际用餐，按合同就低结算一万一千三百四十元，公司抬头发票已开，素食三份与清真两份单独计价已并入总额。','',0,0,0,'{}',3034,320,'2026-07-24T00:50:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<inv-lunch@lunch>');
INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3035,1,'<inv-insure@insure>','安泰保险：团体意外险保单与发票','broker@insure.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-24T08:55:00+08:00','团体意外险已按报名与出单时确认的四十四人于活动当日生效并正常到期；两人临时缺席不影响已生效保单，保费一千七百六十元的公司抬头发票同步开出，保单号尾号0721。','',0,0,0,'{}',3035,300,'2026-07-24T00:55:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3035)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<inv-insure@insure>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<inv-insure@insure>','安泰保险：团体意外险保单与发票','broker@insure.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-24T08:55:00+08:00','团体意外险已按报名与出单时确认的四十四人于活动当日生效并正常到期；两人临时缺席不影响已生效保单，保费一千七百六十元的公司抬头发票同步开出，保单号尾号0721。','',0,0,0,'{}',3035,300,'2026-07-24T00:55:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<inv-insure@insure>');
