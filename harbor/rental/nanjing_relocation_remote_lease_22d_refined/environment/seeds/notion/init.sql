PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM "database_rows";
DELETE FROM "workspaces";
DELETE FROM "users";
DELETE FROM "pages";
DELETE FROM "databases";
DELETE FROM "counters";
DELETE FROM "comments";
DELETE FROM "blocks";
INSERT INTO "blocks" ("block_id","parent_block_id","parent_page_id","type","content_json","has_children","archived","position","created_time","last_edited_time") VALUES ('blk_0001',NULL,'page_index','paragraph','{"rich_text": [{"type": "text", "text": {"content": "Gu Fengrental recordmonthly rent、commute、property ownerandpayee name、service feeandlistingstatusrental recordatrental recordsheetledgerin；rental recordto 6 month 28 dayrental recordnonerental recordNanjinglistingrecord。", "link": null}, "plain_text": "rental recordto 6 month 28 dayledgerrental recordnonerental recordNanjinglistingrecord。"}], "color": "default"}',0,0,0,'2026-06-28T08:00:00Z','2026-06-28T08:00:00Z');
INSERT INTO "databases" ("database_id","parent_type","parent_id","title","schema_json","archived","created_time","last_edited_time") VALUES ('db_njr_verify','workspace','ws_gufeng','Nanjingrental verificationledger','{"listing_id": {"id": "title", "name": "listing_id", "type": "title", "title": {}}, "community": {"id": "c1", "name": "community", "type": "rich_text", "rich_text": {}}, "monthly rent": {"id": "c2", "name": "monthly rent", "type": "number", "number": {"format": "number"}}, "measuredcommuteminutes": {"id": "c3", "name": "measuredcommuteminutes", "type": "number", "number": {"format": "number"}}, "property owner": {"id": "c4", "name": "property owner", "type": "rich_text", "rich_text": {}}, "payee name": {"id": "c5", "name": "payee name", "type": "rich_text", "rich_text": {}}, "rental recordcents": {"id": "c6", "name": "rental recordcents", "type": "number", "number": {"format": "number"}}, "verified": {"id": "c7", "name": "verified", "type": "checkbox", "checkbox": {}}, "agency fee": {"id": "c8", "name": "agency fee", "type": "rich_text", "rich_text": {}}, "rental recordchoose": {"id": "c9", "name": "rental recordchoose", "type": "select", "select": {"options": [{"name": "rental record", "color": "green"}, {"name": "inflated", "color": "red"}, {"name": "too low", "color": "yellow"}]}}, "status": {"id": "c10", "name": "status", "type": "select", "select": {"options": [{"name": "active", "color": "green"}, {"name": "delisted", "color": "gray"}]}}, "conclusion": {"id": "c11", "name": "conclusion", "type": "select", "select": {"options": [{"name": "pass", "color": "green"}, {"name": "rental record", "color": "red"}, {"name": "rental recordchoose", "color": "gray"}]}}}',0,'2026-06-28T08:00:00Z','2026-06-28T08:00:00Z');
INSERT INTO "pages" ("page_id","parent_type","parent_id","title","archived","created_time","last_edited_time","properties_json","icon","cover") VALUES ('page_index','workspace','ws_gufeng','Nanjingremoterentalverification rental record',0,'2026-06-28T08:00:00Z','2026-06-28T08:00:00Z','{"title": {"id": "title", "type": "title", "title": [{"type": "text", "text": {"content": "Nanjingremoterentalverification rental record", "link": null}, "plain_text": "Nanjingremoterentalverification rental record"}]}}',NULL,NULL);
INSERT INTO "users" ("user_id","name","avatar_url","email","type") VALUES ('usr_gufeng','Gu Feng',NULL,'gufeng@vmail.example.cn','person');
INSERT INTO "workspaces" ("workspace_id","name","owner_user_id") VALUES ('ws_gufeng','Gu Feng rental recordunitworkrental record','usr_gufeng');
INSERT INTO "database_rows" ("row_id","database_id","properties_json","created_time","last_edited_time","archived") VALUES ('row_njr_lodging_quote_8PmQ','db_njr_verify','{"listing_id": {"id": "title", "type": "title", "title": [{"type": "text", "text": {"content": "rental recordhourliverental recordweekplan", "link": null}, "plain_text": "rental recordhourliverental recordweekplan"}]}, "monthly rent": {"id": "c2", "type": "number", "number": 840000}, "conclusion": {"id": "c11", "type": "select", "select": {"name": "rental record", "color": "red"}}}','2026-06-12T09:20:00Z','2026-06-13T08:10:00Z',1);
COMMIT;
UPDATE blocks SET created_time = '2026-06-27T23:00:00Z', last_edited_time = '2026-06-27T23:00:00Z'
WHERE created_time > '2026-06-28T01:00:00Z' OR last_edited_time > '2026-06-28T01:00:00Z';
UPDATE pages SET created_time = '2026-06-27T23:00:00Z', last_edited_time = '2026-06-27T23:00:00Z'
WHERE created_time > '2026-06-28T01:00:00Z' OR last_edited_time > '2026-06-28T01:00:00Z';
UPDATE databases SET created_time = '2026-06-27T23:00:00Z', last_edited_time = '2026-06-27T23:00:00Z'
WHERE created_time > '2026-06-28T01:00:00Z' OR last_edited_time > '2026-06-28T01:00:00Z';
UPDATE comments SET created_time = '2026-06-27T23:00:00Z'
WHERE created_time > '2026-06-28T01:00:00Z';
PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;
INSERT INTO pages(page_id,parent_type,parent_id,title,archived,created_time,last_edited_time,properties_json,icon,cover) VALUES
('page_njr_job_docs','workspace','ws_gufeng','Nanjingonboardingmaterials',0,'2026-04-08T04:00:00Z','2026-06-21T03:00:00Z','{"company":"Nanjingrental recorditemrental record","reportingday":"2026-07-20"}','💼',NULL),
('page_njr_oldlease','workspace','ws_gufeng','Wuhanoldrental recordrentrecord',0,'2026-04-12T10:20:00Z','2026-06-24T11:30:00Z','{"monthly rent":2600,"contracttorental record":"2026-06-30"}','🏚️',NULL),
('page_njr_move_inventory','workspace','ws_gufeng','rental record',0,'2026-05-02T08:15:00Z','2026-06-20T13:40:00Z','{"rental record":20,"rental record":12}','📦',NULL),
('page_njr_storage','workspace','ws_gufeng','rental recordhourrental record',0,'2026-05-11T03:40:00Z','2026-06-18T04:00:00Z','{"rental record":"5rental record","monthly rent":1200}','🗄️',NULL),
('page_njr_train','workspace','ws_gufeng','WuhanNanjingrental recordcommunicaterecord',0,'2026-05-15T06:30:00Z','2026-06-23T19:10:00Z','{"rental recordsend Station":"rental record Station","rental recordof Station":"Nanjingrental record Station"}','🚄',NULL),
('page_njr_move_costs_7QmP','workspace','ws_gufeng','rental recordbeforerental record',0,'2026-05-19T10:35:00Z','2026-06-26T10:00:00Z','{"rental record":"CNY","rental recordledger":8}','🧾',NULL),
('page_njr_commute_notes','workspace','ws_gufeng','rental recordcommuterental record',0,'2026-05-23T09:10:00Z','2026-06-26T14:10:00Z','{"rental record":"Software Avenue","rental recordcommunicate":"Metroandsteprental record"}','🚇',NULL),
('page_njr_utilities','workspace','ws_gufeng','oldrental record',0,'2026-05-28T12:00:00Z','2026-06-27T02:00:00Z','{"rental record":"Wuhan","rental record":"2026-06-30"}','💡',NULL),
('page_njr_health','workspace','ws_gufeng','rental recordandrental record',0,'2026-06-09T07:10:00Z','2026-06-14T00:20:00Z','{"rental record":"Wuhan","rental record":"rental recordcomplete"}','🩺',NULL),
('page_njr_accounts','workspace','ws_gufeng','rental recordaccount',0,'2026-06-05T09:30:00Z','2026-06-25T10:00:00Z','{"rental record":"rental recordbank","rental record":24000}','🏦',NULL),
('page_njr_work_training','workspace','ws_gufeng','onboardingbeforerental record',0,'2026-05-01T02:00:00Z','2026-06-22T13:00:00Z','{"rental recordcompleterental record":6,"rental record":8}','🧑‍💻',NULL),
('page_njr_parcel_addresses','workspace','ws_gufeng','rental recordaddress',0,'2026-05-08T16:45:00Z','2026-06-20T08:30:00Z','{"Wuhanaddress":3,"Nanjingaddress":1}','📮',NULL),
('page_njr_area_notes_4KxV','workspace','ws_gufeng','rental recordmaterialsrental record',0,'2026-05-30T11:25:00Z','2026-06-27T08:05:00Z','{"rental record":5,"source":"rental recordandcommunityrental record"}','🗺️',NULL),
('page_njr_contacts','workspace','ws_gufeng','rental recordcontactperson',0,'2026-06-01T14:20:00Z','2026-06-24T06:50:00Z','{"Wuhan":4,"Nanjing":2}','☎️',NULL),
('page_njr_lodging_quote','workspace','ws_gufeng','rental recordliverental record',1,'2026-06-12T09:15:00Z','2026-06-13T08:15:00Z','{"rental recordweekrental record":8400,"status":"notrental record"}','🏨',NULL);
INSERT INTO blocks(block_id,parent_block_id,parent_page_id,type,content_json,has_children,archived,position,created_time,last_edited_time) VALUES
('blk_njr_job_location',NULL,'page_njr_job_docs','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recordofficelocationatrental recordSoftware Avenue。"}}]}',0,0,1,'2026-04-08T04:02:00Z','2026-04-08T04:02:00Z'),
('blk_njr_job_hotel',NULL,'page_njr_job_docs','paragraph','{"rich_text":[{"type":"text","text":{"content":"companyrental recordcontainsrental recordweekrental recordhourliverental record。"}}]}',0,0,2,'2026-04-09T06:50:00Z','2026-04-09T06:50:00Z'),
('blk_njr_oldlease_end',NULL,'page_njr_oldlease','paragraph','{"rich_text":[{"type":"text","text":{"content":"Wuhanoldrental recordcontractrental recordmonthrental recorddaytorental record。"}}]}',0,0,1,'2026-04-12T10:22:00Z','2026-06-24T11:30:00Z'),
('blk_njr_oldlease_marks',NULL,'page_njr_oldlease','bulleted_list_item','{"rich_text":[{"type":"text","text":{"content":"rental recordrentrental recordrecordrental record。"}}]}',0,0,2,'2026-06-12T06:30:00Z','2026-06-12T06:30:00Z'),
('blk_njr_inventory_books',NULL,'page_njr_move_inventory','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recordinnumberrental record。"}}]}',0,0,1,'2026-05-02T08:18:00Z','2026-06-16T04:30:00Z'),
('blk_njr_inventory_desk',NULL,'page_njr_move_inventory','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recordGu Fengall，rental recordcanrental record。"}}]}',0,0,2,'2026-05-13T13:50:00Z','2026-05-13T13:50:00Z'),
('blk_njr_storage_access',NULL,'page_njr_storage','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recordaccess controlrental recordtorental recorddayrental record。"}}]}',0,0,1,'2026-06-18T03:50:00Z','2026-06-18T04:00:00Z'),
('blk_njr_storage_exclusions',NULL,'page_njr_storage','quote','{"rich_text":[{"type":"text","text":{"content":"rental recordcontractnotrental recordandidentity documentrental recorditem。"}}]}',0,0,2,'2026-05-11T03:45:00Z','2026-05-11T03:45:00Z'),
('blk_njr_train_refund',NULL,'page_njr_train','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recordmonthrental recordCNY。"}}]}',0,0,1,'2026-05-19T10:35:00Z','2026-05-19T10:35:00Z'),
('blk_njr_train_luggage',NULL,'page_njr_train','bulleted_list_item','{"rich_text":[{"type":"text","text":{"content":"rental recordreserverental recordandidentity documentrental record。"}}]}',0,0,2,'2026-06-23T19:10:00Z','2026-06-23T19:10:00Z'),
('blk_njr_budget_boxes',NULL,'page_njr_move_costs_7QmP','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recordandrental recordCNY。"}}]}',0,0,1,'2026-06-16T04:32:00Z','2026-06-16T04:32:00Z'),
('blk_njr_budget_storage',NULL,'page_njr_move_costs_7QmP','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recordyourental recordCNY。"}}]}',0,0,2,'2026-06-18T11:50:00Z','2026-06-18T11:50:00Z'),
('blk_njr_commute_transfer',NULL,'page_njr_commute_notes','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recordcommunicaterental record S8 rental recordtransferrental record。"}}]}',0,0,1,'2026-05-23T09:12:00Z','2026-05-23T09:12:00Z'),
('blk_njr_commute_rain',NULL,'page_njr_commute_notes','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recorddaysSoftware Avenuerental record。"}}]}',0,0,2,'2026-06-26T14:10:00Z','2026-06-26T14:10:00Z'),
('blk_njr_utility_modem',NULL,'page_njr_utilities','paragraph','{"rich_text":[{"type":"text","text":{"content":"Wuhanrental recordcommunicaterental recordasset。"}}]}',0,0,1,'2026-05-18T02:00:00Z','2026-05-18T02:00:00Z'),
('blk_njr_utility_meter',NULL,'page_njr_utilities','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recordmontholdrental recordgoyearrental record。"}}]}',0,0,2,'2026-06-27T02:00:00Z','2026-06-27T02:00:00Z'),
('blk_njr_health_receipt',NULL,'page_njr_health','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recordmonthrental recordCNY。"}}]}',0,0,1,'2026-06-09T07:12:00Z','2026-06-09T07:12:00Z'),
('blk_njr_account_emergency',NULL,'page_njr_accounts','paragraph','{"rich_text":[{"type":"text","text":{"content":"shouldurgentaccountrental recordmonthrental recordten-thousandrental recordCNY。"}}]}',0,0,1,'2026-06-20T12:15:00Z','2026-06-20T12:15:00Z'),
('blk_njr_training_modules',NULL,'page_njr_work_training','to_do','{"rich_text":[{"type":"text","text":{"content":"securityandrental recordalreadycomplete。"}}],"checked":true}',0,0,1,'2026-05-22T12:20:00Z','2026-05-22T12:20:00Z'),
('blk_njr_hotel_reason',NULL,'page_njr_lodging_quote','paragraph','{"rich_text":[{"type":"text","text":{"content":"rental recordweekrental recordcompanyrental record。"}}]}',0,1,1,'2026-06-13T08:12:00Z','2026-06-13T08:15:00Z');
INSERT INTO comments(comment_id,parent_page_id,discussion_id,content_json,created_by,created_time) VALUES
('cmt_njr_job_badge','page_njr_job_docs','disc_job','{"text":"rental recordphotouserental recordidentity documentfollow。"}','usr_gufeng','2026-06-21T03:00:00Z'),
('cmt_njr_oldlease_receipt','page_njr_oldlease','disc_oldlease','{"text":"rental recordmonthly rentrental recordalreadyunderrental record。"}','usr_gufeng','2026-06-24T11:30:00Z'),
('cmt_njr_inventory_monitor','page_njr_move_inventory','disc_inventory','{"text":"showsrental recordreserverental record。"}','usr_gufeng','2026-06-17T12:05:00Z'),
('cmt_njr_storage_key','page_njr_storage','disc_storage','{"text":"rental recordatidentity documentrental recordoutsiderental record。"}','usr_gufeng','2026-06-18T04:00:00Z'),
('cmt_njr_train_seat','page_njr_train','disc_train','{"text":"rental recordpreferencesrental record。"}','usr_gufeng','2026-06-23T19:10:00Z'),
('cmt_njr_budget_refund','page_njr_move_costs_7QmP','disc_budget','{"text":"rental recordtorental recordcommunicaterental recordaccount。"}','usr_gufeng','2026-05-19T10:36:00Z'),
('cmt_njr_commute_weather','page_njr_commute_notes','disc_commute','{"text":"rental recordmonthrental recorddayNanjinghaverental record。"}','usr_gufeng','2026-06-26T14:10:00Z'),
('cmt_njr_utility_close','page_njr_utilities','disc_utility','{"text":"rental recordaboutrental recorddayisrental recordmonthrental recordday。"}','usr_gufeng','2026-06-27T02:00:00Z'),
('cmt_njr_training_exam','page_njr_work_training','disc_training','{"text":"rental recordalreadyrental record。"}','usr_gufeng','2026-06-22T13:00:00Z'),
('cmt_njr_hotel_close_5KqM','page_njr_lodging_quote','disc_hotel','{"text":"rental recordliverental record。"}','usr_gufeng','2026-06-13T08:15:00Z');
INSERT INTO databases(database_id,parent_type,parent_id,title,schema_json,archived,created_time,last_edited_time) VALUES ('db_njr_move_items','workspace','ws_gufeng','rental recordstatus','{"rental record":{"type":"title"},"rental record":{"type":"number"},"rental record":{"type":"select"},"location":{"type":"rich_text"}}',0,'2026-05-02T08:10:00Z','2026-06-20T13:40:00Z');
INSERT INTO database_rows(row_id,database_id,properties_json,created_time,last_edited_time,archived) VALUES
('row_njr_books','db_njr_move_items','{"rental record":"rental record","rental record":3,"rental record":"rental record","location":"oldrental recordunit"}','2026-05-02T08:20:00Z','2026-06-16T04:30:00Z',0),
('row_njr_clothes','db_njr_move_items','{"rental record":"rental record","rental record":5,"rental record":"rental record","location":"oldrental recordbedroom"}','2026-05-02T08:22:00Z','2026-06-18T04:00:00Z',0),
('row_njr_kitchen','db_njr_move_items','{"rental record":"kitchenrental record","rental record":2,"rental record":"rental record","location":"rental recordyourental record"}','2026-05-02T08:24:00Z','2026-06-18T04:00:00Z',0),
('row_njr_desk','db_njr_move_items','{"rental record":"canrental record","rental record":1,"rental record":"rental record","location":"oldrental recordunit"}','2026-05-13T13:52:00Z','2026-06-20T13:40:00Z',0),
('row_njr_chair','db_njr_move_items','{"rental record":"officerental record","rental record":1,"rental record":"rental record","location":"oldrental recordliving room"}','2026-05-13T13:54:00Z','2026-06-12T18:10:00Z',1),
('row_njr_bedding','db_njr_move_items','{"rental record":"rental record","rental record":2,"rental record":"rental record","location":"rental recordyourental record"}','2026-05-18T09:10:00Z','2026-06-18T04:00:00Z',0),
('row_njr_documents','db_njr_move_items','{"rental record":"identity documentandcontract","rental record":1,"rental record":"rental record","location":"identity documentrental record"}','2026-06-04T18:25:00Z','2026-06-23T19:10:00Z',0);
COMMIT;

BEGIN TRANSACTION;
UPDATE blocks SET position=10 WHERE block_id='blk_njr_job_location';
UPDATE blocks SET position=30 WHERE block_id='blk_njr_job_hotel';
UPDATE blocks SET position=4 WHERE block_id='blk_njr_oldlease_end';
UPDATE blocks SET position=19 WHERE block_id='blk_njr_oldlease_marks';
UPDATE blocks SET position=7 WHERE block_id='blk_njr_inventory_books';
UPDATE blocks SET position=28 WHERE block_id='blk_njr_inventory_desk';
UPDATE blocks SET position=3 WHERE block_id='blk_njr_storage_access';
UPDATE blocks SET position=17 WHERE block_id='blk_njr_storage_exclusions';
UPDATE blocks SET position=11 WHERE block_id='blk_njr_train_refund';
UPDATE blocks SET position=26 WHERE block_id='blk_njr_train_luggage';
UPDATE blocks SET position=5 WHERE block_id='blk_njr_budget_boxes';
UPDATE blocks SET position=23 WHERE block_id='blk_njr_budget_storage';
UPDATE blocks SET position=8 WHERE block_id='blk_njr_commute_transfer';
UPDATE blocks SET position=21 WHERE block_id='blk_njr_commute_rain';
UPDATE blocks SET position=2 WHERE block_id='blk_njr_utility_modem';
UPDATE blocks SET position=14 WHERE block_id='blk_njr_utility_meter';
UPDATE blocks SET position=6 WHERE block_id='blk_njr_health_receipt';
UPDATE blocks SET position=12 WHERE block_id='blk_njr_account_emergency';
UPDATE blocks SET position=9 WHERE block_id='blk_njr_training_modules';
UPDATE blocks SET position=16 WHERE block_id='blk_njr_hotel_reason';
COMMIT;
UPDATE blocks SET created_time = '2026-06-27T23:00:00Z', last_edited_time = '2026-06-27T23:00:00Z'
WHERE created_time > '2026-06-28T01:00:00Z' OR last_edited_time > '2026-06-28T01:00:00Z';
UPDATE pages SET created_time = '2026-06-27T23:00:00Z', last_edited_time = '2026-06-27T23:00:00Z'
WHERE created_time > '2026-06-28T01:00:00Z' OR last_edited_time > '2026-06-28T01:00:00Z';
UPDATE databases SET created_time = '2026-06-27T23:00:00Z', last_edited_time = '2026-06-27T23:00:00Z'
WHERE created_time > '2026-06-28T01:00:00Z' OR last_edited_time > '2026-06-28T01:00:00Z';
UPDATE comments SET created_time = '2026-06-27T23:00:00Z'
WHERE created_time > '2026-06-28T01:00:00Z';
