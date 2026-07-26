INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3010,1,'<roster-open@admin>','行政：团建报名通道已开，分组人数初稿','admin.support@example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-01T08:45:00+08:00','报名通道今天开放。按现有编制先给你一版分组人数：采购组12人、质量组10人、物流组14人、计划组8人，合计44人。个别同事的出行限制我们会单独收集，汇总时只给你人数和类别，不放到全员可见的表里。','',0,0,0,'{}',3010,420,'2026-07-01T00:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3010)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<roster-open@admin>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<roster-open@admin>','行政：团建报名通道已开，分组人数初稿','admin.support@example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-01T08:45:00+08:00','报名通道今天开放。按现有编制先给你一版分组人数：采购组12人、质量组10人、物流组14人、计划组8人，合计44人。个别同事的出行限制我们会单独收集，汇总时只给你人数和类别，不放到全员可见的表里。','',0,0,0,'{}',3010,420,'2026-07-01T00:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<roster-open@admin>');
