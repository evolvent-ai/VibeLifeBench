PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
INSERT INTO users (user_id,name,avatar_url,email,type) VALUES
('usr_zhang_ming','Zhang Ming',NULL,'zhang.ming@company.com','person');
INSERT INTO workspaces (workspace_id,name,owner_user_id) VALUES
('ws_zhang_ming_work','Zhang Ming Work Notes','usr_zhang_ming');
INSERT INTO pages (page_id,parent_type,parent_id,title,archived,created_time,last_edited_time,properties_json,icon,cover) VALUES
('page_shanghai_roadshow_2025','workspace','ws_zhang_ming_work','Shanghai Client Roadshow 2025 Retrospective',0,'2025-11-18T03:00:00Z','2025-11-26T09:15:00Z','{"topic":"sales operations","status":"archived"}','📊',NULL),
('page_travel_checklist_template','workspace','ws_zhang_ming_work','International Travel Checklist Template',0,'2026-02-04T02:20:00Z','2026-06-12T07:40:00Z','{"topic":"travel operations","status":"template"}','🧳',NULL),
('page_q2_campaign_budget','workspace','ws_zhang_ming_work','Q2 Campaign Budget Review',0,'2026-06-16T04:10:00Z','2026-06-29T08:30:00Z','{"topic":"marketing finance","status":"reviewed"}','💹',NULL),
('page_japanese_study_notes','workspace','ws_zhang_ming_work','Japanese Study Notes — Client Greetings',0,'2026-05-03T11:00:00Z','2026-06-21T12:05:00Z','{"topic":"language","status":"active"}','🗣️',NULL);
INSERT INTO blocks (block_id,parent_block_id,parent_page_id,type,content_json,has_children,archived,position,created_time,last_edited_time) VALUES
('blk_roadshow_scope',NULL,'page_shanghai_roadshow_2025','paragraph','{"text":"Three-day domestic roadshow covering Pudong, Xuhui, and Hongqiao; all rail and taxi receipts closed in November 2025."}',0,0,0,'2025-11-18T03:05:00Z','2025-11-26T09:15:00Z'),
('blk_roadshow_lesson',NULL,'page_shanghai_roadshow_2025','bulleted_list_item','{"text":"Keep client-meeting buffers separate from travel time and record the actual settlement reference beside each expense."}',0,0,1,'2025-11-18T03:08:00Z','2025-11-26T09:15:00Z'),
('blk_template_docs',NULL,'page_travel_checklist_template','to_do','{"text":"Passport validity, destination entry rule, insurance policy, itinerary, emergency contact","checked":false}',0,0,0,'2026-02-04T02:25:00Z','2026-06-12T07:40:00Z'),
('blk_template_money',NULL,'page_travel_checklist_template','to_do','{"text":"Separate estimated, authorized, paid, refunded, and reimbursable amounts by currency","checked":false}',0,0,1,'2026-02-04T02:28:00Z','2026-06-12T07:40:00Z'),
('blk_template_security',NULL,'page_travel_checklist_template','callout','{"text":"Do not store passport numbers or payment credentials in general work notes."}',0,0,2,'2026-02-04T02:31:00Z','2026-06-12T07:40:00Z'),
('blk_budget_total',NULL,'page_q2_campaign_budget','paragraph','{"text":"Approved Q2 campaign envelope CNY 480,000; paid media and event production remain separate cost centers."}',0,0,0,'2026-06-16T04:15:00Z','2026-06-29T08:30:00Z'),
('blk_budget_variance',NULL,'page_q2_campaign_budget','table','{"rows":[["Workstream","Budget","Actual"],["Paid media","210000","204600"],["Events","150000","146800"]]}',0,0,1,'2026-06-16T04:18:00Z','2026-06-29T08:30:00Z'),
('blk_language_opening',NULL,'page_japanese_study_notes','heading_2','{"text":"Meeting openings"}',0,0,0,'2026-05-03T11:05:00Z','2026-06-21T12:05:00Z'),
('blk_language_phrase',NULL,'page_japanese_study_notes','paragraph','{"text":"Use a short self-introduction, confirm name pronunciation, and switch to the interpreter when commercial terms become precise."}',0,0,1,'2026-05-03T11:08:00Z','2026-06-21T12:05:00Z');
INSERT INTO counters (key,value) VALUES ('page_seq',9000),('block_seq',9000),('comment_seq',9000),('database_seq',9000),('row_seq',9000);
COMMIT;
