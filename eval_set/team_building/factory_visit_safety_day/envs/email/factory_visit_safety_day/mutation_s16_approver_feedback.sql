INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3026,1,'<review-feedback@approver>','HR：评审意见与需要补充的三点','approver@example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-17T14:45:00+08:00','业务理解那段保留，做得不错。还差三点：一是参访强度要说清楚，站立和步行多久、中途能不能退出；二是拍摄边界要写成成员看得懂的话，不要只写不许拍；三是对外提供的人员信息要按人数和类别汇总，不要出现具体是谁有什么情况。补完再发我一版。','',0,1,0,'{}',3026,470,'2026-07-17T06:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3026)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<review-feedback@approver>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<review-feedback@approver>','HR：评审意见与需要补充的三点','approver@example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-17T14:45:00+08:00','业务理解那段保留，做得不错。还差三点：一是参访强度要说清楚，站立和步行多久、中途能不能退出；二是拍摄边界要写成成员看得懂的话，不要只写不许拍；三是对外提供的人员信息要按人数和类别汇总，不要出现具体是谁有什么情况。补完再发我一版。','',0,1,0,'{}',3026,470,'2026-07-17T06:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<review-feedback@approver>');
