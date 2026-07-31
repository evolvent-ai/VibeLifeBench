INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3011,1,'<goal-detail@approver>','HR：团建方案评审要点与提交时限','approver@example.invalid','["wei.ran@example.invalid"]','["admin.support@example.invalid"]','[]','2026-07-02T09:45:00+08:00','评审会我先占在七月十七日下午。方案要能说清三件事：业务理解环节怎么设计、参观过程中的安全边界怎么控制、以及参与自愿如何落实到报名和退出安排上。候选方案请在评审会前给我，不用等全部谈妥。','',0,1,0,'{}',3011,400,'2026-07-02T01:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3011)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<goal-detail@approver>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<goal-detail@approver>','HR：团建方案评审要点与提交时限','approver@example.invalid','["wei.ran@example.invalid"]','["admin.support@example.invalid"]','[]','2026-07-02T09:45:00+08:00','评审会我先占在七月十七日下午。方案要能说清三件事：业务理解环节怎么设计、参观过程中的安全边界怎么控制、以及参与自愿如何落实到报名和退出安排上。候选方案请在评审会前给我，不用等全部谈妥。','',0,1,0,'{}',3011,400,'2026-07-02T01:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<goal-detail@approver>');
