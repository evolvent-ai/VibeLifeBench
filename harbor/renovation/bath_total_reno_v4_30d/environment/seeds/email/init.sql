-- Generated email seed for bath_total_reno_v4_30d
BEGIN;
INSERT INTO account_config (id, email, name, created_at) VALUES (1, 'geng.lu.reno4@gmail.com', 'Geng Lu', '2021-09-01T00:00:00Z');
INSERT INTO folders (id,name) VALUES (1,'INBOX'),(2,'Sent'),(3,'Drafts'),(4,'Trash'),(5,'Spam');
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES (1, 1, '<order-260615-7f2a@mall.cn>', 'renovation project detail：bathroom waterproofing+renovation project detail', 'renovation project detail <order@mall.cn>', '["geng.lu.reno4@gmail.com"]', '2026-06-15T11:25:00Z', 'renovation project detail ord_qbath_0001 renovation project detail。renovation project detail。', 1, 0, '{}', 220, '2026-06-15T11:25:00Z');
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES (2, 1, '<order-260615-9c4d@mall.cn>', 'renovation project detail：bathroom waterproofing+renovation project detail', 'renovation project detail <order@mall.cn>', '["geng.lu.reno4@gmail.com"]', '2026-06-15T02:10:00Z', 'renovation project detail ord_qbath_0002 renovation project detail，renovation project detail。', 1, 0, '{}', 220, '2026-06-15T02:10:00Z');
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES (3, 1, '<dispatch-260615-pd8m@citylogistics.example>', '【renovation project detail】renovation project detail，renovation project detail', 'renovation project detail <service@forward.com>', '["geng.lu.reno4@gmail.com"]', '2026-06-15T12:00:00Z', 'renovation project detail GL2099 renovation project detail：renovation project detail。renovation project detail：renovation project detail/renovation project detail，renovation project detail。', 0, 1, '{}', 220, '2026-06-15T12:00:00Z');
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES (4, 1, '<property-receipt-260614-4k7q@property.example>', 'renovation project detail', 'renovation project detail <finance@property.example>', '["geng.lu.reno4@gmail.com"]', '2026-06-14T16:20:00+08:00', 'renovation project detail 300 renovation project detail。renovation project detail、renovation project detail。', 1, 0, '{"receipt":"PM-RCPT-260614"}', 246, '2026-06-14T16:20:00+08:00');
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE messages.folder_id=folders.id), unread_count=(SELECT COUNT(*) FROM messages WHERE messages.folder_id=folders.id AND messages.is_read=0);
INSERT INTO _counters (key,value) VALUES ('msg_seq',4);

-- HANDBOOK_REMEDIATION_V113
INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at) VALUES
 (2001,1,'<contract-v3-260610-a8f2@sealpro.example>','contract v3 renovation project detail','renovation project detail <zhou.lan@sealpro.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-10T09:12:00+08:00','renovation project detail、masonry work、renovation project detail，renovation project detail。',NULL,1,1,0,NULL,NULL,'{"thread":"contract"}',2001,420,'2026-06-10T09:12:00+08:00'),
 (2002,1,'<permit-docs-260610-k3m9@property.example>','renovation project detail：renovation project detail','renovation project detail <engineering@property.example>','["geng.lu.reno4@gmail.com"]','["zhou.lan@sealpro.example"]','[]','2026-06-10T15:40:00+08:00','renovation project detail，renovation project detail。',NULL,1,1,0,NULL,NULL,'{"case":"PM-QB-0610"}',2002,380,'2026-06-10T15:40:00+08:00'),
 (2003,1,'<verify-4251g-260611-r7q4@brand.example>','renovation project detail','SealPro renovation project detail <verify@sealpro.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-11T10:18:00+08:00','renovation project detail VRF-QBATH-4251G renovation project detail v3，renovation project detail。',NULL,0,1,0,NULL,NULL,'{"vcode":"VRF-QBATH-4251G"}',2003,360,'2026-06-11T10:18:00+08:00'),
 (2004,1,'<precheck-260612-hh6d@inspect.example>','renovation project detail：renovation project detail','renovation project detail <service@huaheng-inspect.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-12T16:05:00+08:00','renovation project detail、renovation project detail。',NULL,1,0,0,NULL,NULL,'{"visit":"HH-QB-PRE"}',2004,310,'2026-06-12T16:05:00+08:00'),
 (2005,1,'<batch-260613-05sh@supplier.example>','renovation project detail','renovation project detail <batch@supplier.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-13T11:24:00+08:00','renovation project detail 2026-05-SH，renovation project detail，renovation project detail。',NULL,0,0,0,NULL,NULL,'{"batch":"2026-05-SH"}',2005,300,'2026-06-13T11:24:00+08:00'),
 (2006,1,'<schedule-260613-c9v2@sealpro.example>','renovation project detail','renovation project detail <chen@sealpro.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-13T17:10:00+08:00','renovation project detail；renovation project detail。',NULL,1,0,0,NULL,NULL,'{"schedule":"QB-SCH-01"}',2006,330,'2026-06-13T17:10:00+08:00'),
 (2007,1,'<card-confirm-260614-4251@card.example>','renovation project detail','renovation project detail <notice@card.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-14T09:00:00+08:00','renovation project detail，renovation project detail。',NULL,1,1,0,NULL,NULL,'{"card":"card_qbath_01"}',2007,280,'2026-06-14T09:00:00+08:00'),
 (2008,1,'<concealed-photo-260614-wm8p@sealpro.example>','renovation project detail','renovation project detail <wu.min@sealpro.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-14T13:35:00+08:00','renovation project detail、renovation project detail、renovation project detail。',NULL,0,1,0,NULL,NULL,'{"checklist":"concealed-v2"}',2008,360,'2026-06-14T13:35:00+08:00'),
 (2009,1,'<delivery-window-260614-z2n5@logistics.example>','renovation project detail','renovation project detail <dispatch@logistics.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-14T14:20:00+08:00','renovation project detail，renovation project detail。',NULL,1,0,0,NULL,NULL,'{"tracking":"QB260614"}',2009,290,'2026-06-14T14:20:00+08:00'),
 (2010,1,'<watertest-rule-260614-pm48@property.example>','renovation project detail','renovation project detail <engineering@property.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-14T15:05:00+08:00','renovation project detail 48 renovation project detail、renovation project detail。',NULL,0,1,0,NULL,NULL,'{"rule":"PM-WT-48"}',2010,310,'2026-06-14T15:05:00+08:00'),
 (2011,1,'<changeorder-door-260614-q6k1@sealpro.example>','renovation project detail：renovation project detail','renovation project detail <zhou.lan@sealpro.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-14T16:10:00+08:00','renovation project detail 980 CNY，renovation project detail。',NULL,0,0,0,NULL,NULL,'{"change":"CO-QB-01"}',2011,250,'2026-06-14T16:10:00+08:00'),
 (2012,1,'<reinspection-hold-260614-hh02@inspect.example>','renovation project detail 6 month 30 day','renovation project detail <service@huaheng-inspect.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-14T17:00:00+08:00','renovation project detail，renovation project detail 24 renovation project detail。',NULL,1,0,0,NULL,NULL,'{"hold":"HH-QB-02"}',2012,250,'2026-06-14T17:00:00+08:00'),
 (2013,1,'<retention-5pct-260614-f3w8@sealpro.example>','renovation project detail','renovation project detail <finance@sealpro.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-14T17:30:00+08:00','renovation project detail 5% renovation project detail。',NULL,0,1,0,NULL,NULL,'{"term":"retention-5pct"}',2013,270,'2026-06-14T17:30:00+08:00'),
 (2014,1,'<neighbor-watertest-260614-b7m2@community.example>','renovation project detail','renovation project detail <service@property.example>','["geng.lu.reno4@gmail.com"]','[]','[]','2026-06-14T18:00:00+08:00','renovation project detail，renovation project detail。',NULL,1,0,0,NULL,NULL,'{"neighbor":"downstairs"}',2014,260,'2026-06-14T18:00:00+08:00');
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id), unread_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id AND is_read=0);

COMMIT;

-- Final English contract email fact consumed by the English oracle and rubric.
BEGIN;
UPDATE messages SET subject='Contract verification result', from_addr='SealPro official verification <verify@sealpro.example>', body_text='Verification code VRF-QBATH-4251G maps to Shanghai regional standard contract v3; door-frame repair and debris removal are outside the base scope.' WHERE id=2003;
COMMIT;

-- Stage-0 temporal fence: order and dispatch messages are released later.
BEGIN;
DELETE FROM messages WHERE id IN (1,2,3);
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE messages.folder_id=folders.id), unread_count=(SELECT COUNT(*) FROM messages WHERE messages.folder_id=folders.id AND messages.is_read=0);
COMMIT;

-- REMEDIATION_20260730_RENOVATION_EMAIL_CONTEXT
BEGIN;
UPDATE messages
SET body_text='order ord_qbath_0002 renovation project detail，renovation project detail；renovation project detail。'
WHERE id=2;
UPDATE messages
SET subject='【renovation project detail】renovation project detail，renovation project detail',
    body_text='renovation project detail。renovation project detail、renovation project detail；renovation project detail。',
    from_addr='renovation project detail <dispatch@citylogistics.example>'
WHERE id=3;
COMMIT;
