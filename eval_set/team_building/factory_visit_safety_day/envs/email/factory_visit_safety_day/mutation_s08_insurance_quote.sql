INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3018,1,'<quote@insure>','安泰保险：44人一日团体意外险报价','broker@insure.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-09T08:45:00+08:00','按四十四人、单日、含工厂参观场景投保，保费合计一千七百六十元，可开公司抬头发票。投保只需要提供人数和活动日期，不需要逐人证件信息。生效前一个工作日截止。','',0,0,0,'{}',3018,390,'2026-07-09T00:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3018)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<quote@insure>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<quote@insure>','安泰保险：44人一日团体意外险报价','broker@insure.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-09T08:45:00+08:00','按四十四人、单日、含工厂参观场景投保，保费合计一千七百六十元，可开公司抬头发票。投保只需要提供人数和活动日期，不需要逐人证件信息。生效前一个工作日截止。','',0,0,0,'{}',3018,390,'2026-07-09T00:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<quote@insure>');
