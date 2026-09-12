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
INSERT INTO "pages" ("page_id","parent_type","parent_id","title","archived","created_time","last_edited_time","properties_json","icon","cover") VALUES ('pg_tracker','workspace','ws_family_038','Parent-child rental tracker',0,'2026-07-18T09:00:00+08:00','2026-07-18T09:00:00+08:00','{}',NULL,NULL);
INSERT INTO "pages" ("page_id","parent_type","parent_id","title","archived","created_time","last_edited_time","properties_json","icon","cover") VALUES ('pg_risk','workspace','ws_family_038','risk log',0,'2026-07-18T09:00:00+08:00','2026-07-18T09:00:00+08:00','{}',NULL,NULL);
INSERT INTO "pages" ("page_id","parent_type","parent_id","title","archived","created_time","last_edited_time","properties_json","icon","cover") VALUES ('pg_budget','workspace','ws_family_038','budget ledger',0,'2026-07-18T09:00:00+08:00','2026-07-18T09:00:00+08:00','{}',NULL,NULL);
INSERT INTO "pages" ("page_id","parent_type","parent_id","title","archived","created_time","last_edited_time","properties_json","icon","cover") VALUES ('pg_auth','workspace','ws_family_038','authorization log',0,'2026-07-18T09:00:00+08:00','2026-07-18T09:00:00+08:00','{}',NULL,NULL);
INSERT INTO "users" ("user_id","name","avatar_url","email","type") VALUES ('usr_family_038','Lin Lan',NULL,'lin.lan@example.invalid','person');
INSERT INTO "users" ("user_id","name","avatar_url","email","type") VALUES ('bot_family_038','rental coordination assistant',NULL,'assistant@example.invalid','bot');
INSERT INTO "workspaces" ("workspace_id","name","owner_user_id") VALUES ('ws_family_038','Lin Lan family rental workspace','usr_family_038');
COMMIT;
PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
INSERT INTO pages(page_id,parent_type,parent_id,title,archived,created_time,last_edited_time,properties_json,icon,cover) VALUES
('pg_family_meals','workspace','ws_family_038','One-Week Family Meal Plan',0,'2026-01-04T20:10:00+08:00','2026-06-28T19:20:00+08:00','{"Theme":"Family diet","Status":"Keep using"}','🍲',NULL),
('pg_child_books','workspace','ws_family_038','Little Orange Picture Book Loans',0,'2026-01-12T18:45:00+08:00','2026-07-03T07:20:00+08:00','{"Category":"Reading","Quantity":18}','📚',NULL),
('pg_fam_health_7Qm2','workspace','ws_family_038','Family Health Records',0,'2026-01-26T09:30:00+08:00','2026-06-20T08:30:00+08:00','{"Custodian":"Lin Lan","Year":2026}','🩺',NULL),
('pg_home_devices','workspace','ws_family_038','Home Appliance Warranty List',0,'2026-02-08T11:00:00+08:00','2026-05-29T15:20:00+08:00','{"Location":"Old home","Under warranty":3}','🔧',NULL),
('pg_family_visits','workspace','ws_family_038','Record of Visits from Relatives and Friends',0,'2026-02-19T21:15:00+08:00','2026-05-23T18:05:00+08:00','{"Most recent visitor":"Grandma","Nights stayed":4}','🏠',NULL),
('pg_work_routines','workspace','ws_family_038','Work-from-Home Habits',0,'2026-03-02T08:50:00+08:00','2026-06-18T17:40:00+08:00','{"Frequently used room":"Study","Network":"Gigabit"}','💻',NULL),
('pg_weekend_outings','workspace','ws_family_038','Weekend Outings with the Child',0,'2026-03-15T16:25:00+08:00','2026-06-21T18:20:00+08:00','{"Preferences":"Parks and libraries","Season":"Spring and summer"}','🌳',NULL),
('pg_clothing_sizes','workspace','ws_family_038','Children''s Clothing Sizes',0,'2026-04-03T13:10:00+08:00','2026-07-15T12:30:00+08:00','{"Shoe size":27,"Top":"110"}','👟',NULL),
('pg_old_home_repairs','workspace','ws_family_038','Old Home Repair Records',0,'2026-04-24T19:40:00+08:00','2026-05-29T15:10:00+08:00','{"Rooms":"Kitchen and balcony","Settled":true}','🧰',NULL),
('pg_fam_trip_4Kx9','workspace','ws_family_038','Qingming Holiday Plan',1,'2026-03-20T10:05:00+08:00','2026-04-06T20:50:00+08:00','{"Status":"Completed","Destination":"Shaoxing"}','🗓️',NULL);
INSERT INTO blocks(block_id,parent_block_id,parent_page_id,type,content_json,has_children,archived,position,created_time,last_edited_time) VALUES
('blk_meals_breakfast',NULL,'pg_family_meals','paragraph','{"rich_text":[{"type":"text","text":{"content":"Weekday breakfasts rotate among oatmeal, eggs, and small wontons."}}]}',0,0,1,'2026-01-04T20:12:00+08:00','2026-06-28T19:20:00+08:00'),
('blk_meals_allergy',NULL,'pg_family_meals','bulleted_list_item','{"rich_text":[{"type":"text","text":{"content":"Little Orange does not eat whole peanuts; there is no recorded allergy to soy products."}}]}',0,0,2,'2026-01-04T20:14:00+08:00','2026-05-07T18:35:00+08:00'),
('blk_books_due',NULL,'pg_child_books','paragraph','{"rich_text":[{"type":"text","text":{"content":"Return three dinosaur-themed picture books before July 10."}}]}',0,0,1,'2026-06-22T08:00:00+08:00','2026-07-03T07:20:00+08:00'),
('blk_books_favorite',NULL,'pg_child_books','quote','{"rich_text":[{"type":"text","text":{"content":"Recently rereading “The Little Bear''s Rain Boots” repeatedly."}}]}',0,0,2,'2026-04-10T19:05:00+08:00','2026-06-12T20:30:00+08:00'),
('blk_health_vaccine',NULL,'pg_fam_health_7Qm2','paragraph','{"rich_text":[{"type":"text","text":{"content":"The influenza vaccine batch has been recorded in the vaccination booklet."}}]}',0,0,1,'2026-01-09T11:30:00+08:00','2026-01-09T11:30:00+08:00'),
('blk_health_dental',NULL,'pg_fam_health_7Qm2','to_do','{"rich_text":[{"type":"text","text":{"content":"Schedule the next dental follow-up in October."}}],"checked":false}',0,0,2,'2026-04-11T11:30:00+08:00','2026-04-11T11:30:00+08:00'),
('blk_device_washer',NULL,'pg_home_devices','paragraph','{"rich_text":[{"type":"text","text":{"content":"The washing machine''s drain pump was replaced in May, with a 90-day warranty."}}]}',0,0,1,'2026-05-29T15:05:00+08:00','2026-05-29T15:20:00+08:00'),
('blk_device_router',NULL,'pg_home_devices','paragraph','{"rich_text":[{"type":"text","text":{"content":"The fiber modem''s power supply was replaced in March, restoring gigabit service to the study''s network port."}}]}',0,0,2,'2026-03-03T16:10:00+08:00','2026-03-03T16:10:00+08:00'),
('blk_visit_grandma',NULL,'pg_family_visits','heading_2','{"rich_text":[{"type":"text","text":{"content":"Grandma Visits Hangzhou in May"}}]}',0,0,1,'2026-05-18T08:20:00+08:00','2026-05-23T18:05:00+08:00'),
('blk_visit_bedding',NULL,'pg_family_visits','paragraph','{"rich_text":[{"type":"text","text":{"content":"The guest room uses a folding bed and a thin blue quilt."}}]}',0,0,2,'2026-05-18T08:22:00+08:00','2026-05-18T08:22:00+08:00'),
('blk_work_video',NULL,'pg_work_routines','paragraph','{"rich_text":[{"type":"text","text":{"content":"Video meetings primarily use the study''s wired network."}}]}',0,0,1,'2026-03-02T08:52:00+08:00','2026-06-18T17:40:00+08:00'),
('blk_work_break',NULL,'pg_work_routines','bulleted_list_item','{"rich_text":[{"type":"text","text":{"content":"At midday, usually step away from the screen for half an hour."}}]}',0,0,2,'2026-03-02T08:54:00+08:00','2026-04-09T12:40:00+08:00'),
('blk_outing_library',NULL,'pg_weekend_outings','paragraph','{"rich_text":[{"type":"text","text":{"content":"The picture-book section of the Binjiang Library is suitable for rainy-day activities."}}]}',0,0,1,'2026-03-15T16:28:00+08:00','2026-05-09T12:05:00+08:00'),
('blk_outing_park',NULL,'pg_weekend_outings','paragraph','{"rich_text":[{"type":"text","text":{"content":"It is about a twelve-minute walk from the North Gate of Baima Lake to the lawn."}}]}',0,0,2,'2026-03-15T16:30:00+08:00','2026-06-21T18:20:00+08:00'),
('blk_clothes_shoes',NULL,'pg_clothing_sizes','paragraph','{"rich_text":[{"type":"text","text":{"content":"Indoor shoes are size 27; the instep is somewhat high."}}]}',0,0,1,'2026-04-03T13:12:00+08:00','2026-07-15T12:30:00+08:00'),
('blk_clothes_raincoat',NULL,'pg_clothing_sizes','paragraph','{"rich_text":[{"type":"text","text":{"content":"The yellow raincoat sleeves are slightly long, but it can still be worn in autumn."}}]}',0,0,2,'2026-04-03T13:14:00+08:00','2026-06-19T08:10:00+08:00'),
('blk_repairs_balcony',NULL,'pg_old_home_repairs','paragraph','{"rich_text":[{"type":"text","text":{"content":"Drainage on the balcony was restored after the floor drain was cleaned in April."}}]}',0,0,1,'2026-04-24T19:42:00+08:00','2026-04-24T19:42:00+08:00'),
('blk_repairs_washer',NULL,'pg_old_home_repairs','paragraph','{"rich_text":[{"type":"text","text":{"content":"The washing machine service order cost 460 yuan in May."}}]}',0,0,2,'2026-05-29T15:08:00+08:00','2026-05-29T15:10:00+08:00'),
('blk_holiday_train',NULL,'pg_fam_trip_4Kx9','paragraph','{"rich_text":[{"type":"text","text":{"content":"The round trip used a high-speed train from Hangzhou East Station to Shaoxing North Station."}}]}',0,1,1,'2026-03-20T10:08:00+08:00','2026-04-06T20:50:00+08:00'),
('blk_holiday_weather',NULL,'pg_fam_trip_4Kx9','paragraph','{"rich_text":[{"type":"text","text":{"content":"There was light rain on April 5, so we switched to an indoor exhibition hall in the afternoon."}}]}',0,1,2,'2026-04-05T18:35:00+08:00','2026-04-06T20:50:00+08:00');
INSERT INTO comments(comment_id,parent_page_id,discussion_id,content_json,created_by,created_time) VALUES
('cmt_meals_soup','pg_family_meals','disc_meals','{"text":"Sunday''s pork rib soup was changed to tomato beef brisket."}','usr_family_038','2026-05-03T18:10:00+08:00'),
('cmt_books_return','pg_child_books','disc_books','{"text":"“Cloud Bread” has been returned."}','usr_family_038','2026-05-11T20:22:00+08:00'),
('cmt_health_copy','pg_fam_health_7Qm2','disc_health','{"text":"A scan of the vaccination booklet has been stored in the family cloud drive."}','usr_family_038','2026-01-10T09:05:00+08:00'),
('cmt_device_filter','pg_home_devices','disc_devices','{"text":"The water purifier filter was replaced in June."}','usr_family_038','2026-06-09T19:40:00+08:00'),
('cmt_visit_train','pg_family_visits','disc_visits','{"text":"Grandma''s return train was changed to 5:00 p.m."}','usr_family_038','2026-05-25T08:15:00+08:00'),
('cmt_work_headset','pg_work_routines','disc_work','{"text":"The backup headset is in the second compartment of the desk."}','usr_family_038','2026-04-18T21:05:00+08:00'),
('cmt_outing_pool','pg_weekend_outings','disc_outing','{"text":"Do not renew the swimming class for now after the trial session."}','usr_family_038','2026-05-17T09:35:00+08:00'),
('cmt_clothes_hat','pg_clothing_sizes','disc_clothes','{"text":"The sun hat''s head circumference is 52 centimeters."}','usr_family_038','2026-06-02T20:12:00+08:00'),
('cmt_repairs_invoice','pg_old_home_repairs','disc_repairs','{"text":"The repair invoice and photos of the old parts have been archived."}','usr_family_038','2026-05-29T20:18:00+08:00'),
('cmt_holiday_closed','pg_fam_trip_4Kx9','disc_holiday','{"text":"The itinerary is complete, and the page has been moved to the archive."}','usr_family_038','2026-04-06T20:50:00+08:00');
INSERT INTO databases(database_id,parent_type,parent_id,title,schema_json,archived,created_time,last_edited_time) VALUES ('db_family_receipts','workspace','ws_family_038','Family Receipt Index','{"Name":{"type":"title"},"Amount":{"type":"number"},"Category":{"type":"select"}}',0,'2026-01-02T09:00:00+08:00','2026-06-30T18:00:00+08:00');
INSERT INTO database_rows(row_id,database_id,properties_json,created_time,last_edited_time,archived) VALUES
('row_receipt_dental','db_family_receipts','{"Name":"Child fluoride treatment","Amount":32000,"Category":"Medical"}','2026-04-11T11:45:00+08:00','2026-04-11T11:45:00+08:00',0),
('row_receipt_washer','db_family_receipts','{"Name":"Washing machine repair","Amount":46000,"Category":"Appliances"}','2026-05-29T15:12:00+08:00','2026-05-29T15:12:00+08:00',0),
('row_receipt_bike','db_family_receipts','{"Name":"Bicycle maintenance","Amount":18500,"Category":"Transportation"}','2026-06-27T17:30:00+08:00','2026-06-27T17:30:00+08:00',0),
('row_receipt_photo','db_family_receipts','{"Name":"Family ID photos","Amount":16800,"Category":"Imaging"}','2026-06-13T11:08:00+08:00','2026-06-13T11:08:00+08:00',0);
COMMIT;
