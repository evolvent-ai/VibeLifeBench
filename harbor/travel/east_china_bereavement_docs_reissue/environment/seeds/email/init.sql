-- Reviewed Stage 0 mailbox: only historical messages; story emails enter via event mutations.
INSERT INTO account_config(id,email,name,created_at) VALUES (1,'lin.che@example.test','Lin Che','2024-01-01T00:00:00+08:00');
INSERT INTO folders(id,name,delimiter,flags_json,message_count,unread_count) VALUES
 (1,'INBOX','/','[]',60,8),(2,'Sent','/','[]',0,0),(3,'Archive','/','[]',0,0),(4,'Trip Archive','/','[]',0,0);

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<60)
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at)
SELECT 1,printf('msg_archive_%03d',n),
       CASE n%12 WHEN 0 THEN 'property quarterly maintenance notice' WHEN 1 THEN 'department meeting minutes' WHEN 2 THEN 'family health-check appointment confirmation' WHEN 3 THEN 'rail membership points reminder' WHEN 4 THEN 'community event registration receipt' WHEN 5 THEN 'library loan due notice' WHEN 6 THEN 'utility bill notice' WHEN 7 THEN 'annual insurance policy summary' WHEN 8 THEN 'classmate reunion time poll' WHEN 9 THEN 'parcel locker pickup notice' WHEN 10 THEN 'course material update' ELSE 'monthly bank statement' END,
       printf('sender%02d@records.example.test',n),
       '["lin.che@example.test"]','[]','[]',
       strftime('%Y-%m-%dT%H:%M:00+08:00','2026-01-20 08:00:00','+'||(n-1)||' days','+'||(n%9)||' hours'),
       CASE n%12 WHEN 0 THEN 'property will inspect fire and water systems by building，scenario text。' WHEN 1 THEN 'scenario text，scenario text、scenario text。' WHEN 2 THEN 'scenario text，scenario text。' WHEN 3 THEN 'scenario text，scenario text。' WHEN 4 THEN 'scenario text，scenario textplacesscenario text。' WHEN 5 THEN 'scenario text，scenario texttimescenario textServicescenario text。' WHEN 6 THEN 'scenario text，scenario textverifyscenario text、scenario text。' WHEN 7 THEN 'scenario text，scenario text。' WHEN 8 THEN 'scenario texttime，scenario text。' WHEN 9 THEN 'scenario text，scenario text。' WHEN 10 THEN 'scenario text，scenario text。' ELSE 'monthly account statementscenario text，scenario textverifyscenario text。' END
       || CASE n%5 WHEN 0 THEN ' scenario text。' WHEN 1 THEN ' scenario text。' WHEN 2 THEN ' scenario text。' WHEN 3 THEN ' scenario text。' ELSE ' scenario texttimescenario text。' END,
       NULL,CASE WHEN n%7=0 THEN 0 ELSE 1 END,CASE WHEN n%17=0 THEN 1 ELSE 0 END,0,NULL,NULL,'{"source":"historical_mail"}',1000+n,220+n,
       strftime('%Y-%m-%dT%H:%M:00+08:00','2026-01-20 08:00:00','+'||(n-1)||' days','+'||(n%9)||' hours')
FROM seq;
