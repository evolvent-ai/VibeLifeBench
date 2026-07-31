INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3019,1,'<charter-quote@bus>','沪嘉包车：七月二十一日往返报价','ops@bus.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-10T15:10:00+08:00','两台四十九座大巴，徐汇总部到嘉兴南湖工业园往返，含高速与司机餐补，一万两千八百元，可开公司抬头发票。当天出车司机与车辆信息我们会在出发前三天报备。','',0,0,0,'{}',3019,380,'2026-07-10T07:10:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3019)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<charter-quote@bus>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<charter-quote@bus>','沪嘉包车：七月二十一日往返报价','ops@bus.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-10T15:10:00+08:00','两台四十九座大巴，徐汇总部到嘉兴南湖工业园往返，含高速与司机餐补，一万两千八百元，可开公司抬头发票。当天出车司机与车辆信息我们会在出发前三天报备。','',0,0,0,'{}',3019,380,'2026-07-10T07:10:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<charter-quote@bus>');
