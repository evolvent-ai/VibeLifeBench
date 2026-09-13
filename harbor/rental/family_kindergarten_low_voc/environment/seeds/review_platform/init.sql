PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM "reservations";
DELETE FROM "saved_merchants";
DELETE FROM "reviews";
DELETE FROM "merchant_qa";
DELETE FROM "deals";
DELETE FROM "merchants";
INSERT INTO "merchants" ("merchant_id","name","category","city","area","address","phone","rating_tenths","review_count","avg_price_minor","price_band","hours","tags","has_private_room","max_party_size") VALUES ('mer_river_garden','Riverside Garden','home_service','Hangzhou','Binjiang','Riverside Garden','',41,168,0,'$$','09:00-21:00','residential community',0,0);
INSERT INTO "merchants" ("merchant_id","name","category","city","area","address","phone","rating_tenths","review_count","avg_price_minor","price_band","hours","tags","has_private_room","max_party_size") VALUES ('mer_maple_lane','Maple Lane','home_service','Hangzhou','Binjiang','Maple Lane','',45,191,0,'$$','09:00-21:00','residential community',0,0);
INSERT INTO "merchants" ("merchant_id","name","category","city","area","address","phone","rating_tenths","review_count","avg_price_minor","price_band","hours","tags","has_private_room","max_party_size") VALUES ('mer_sunbay_loft','Chengwan Apartments','home_service','Hangzhou','Binjiang','Chengwan Apartments','',36,92,0,'$','09:00-21:00','residential community',0,0);
INSERT INTO "reviews" ("review_id","merchant_id","user_id","rating","body","image_captions","created_at") VALUES ('rv_river_noise','mer_river_garden','resident_chen',3,'There is occasional renovation noise during the day because the neighboring unit was newly renovated, and the wardrobe odor needs to be confirmed during the property viewing.','{"tags":["renovation","noise"],"severity":1,"hidden":0}','2026-07-16T10:00:00+08:00');
INSERT INTO "reviews" ("review_id","merchant_id","user_id","rating","body","image_captions","created_at") VALUES ('rv_river_lift','mer_river_garden','resident_wu',4,'One of the two elevators was serviced in June; there are occasional queues during the morning rush, and the fire exit is generally clean.','{"tags":["elevator","fire"],"severity":1,"hidden":0}','2026-07-12T19:20:00+08:00');
INSERT INTO "reviews" ("review_id","merchant_id","user_id","rating","body","image_captions","created_at") VALUES ('rv_maple_child','mer_maple_lane','resident_lu',5,'The fire safety signage in the hallway is up to date, the children''s activity area is well maintained, and the window lock installation records are clear.','{"tags":["child_space","fire"],"severity":0,"hidden":0}','2026-07-15T11:00:00+08:00');
INSERT INTO "reviews" ("review_id","merchant_id","user_id","rating","body","image_captions","created_at") VALUES ('rv_maple_quiet','mer_maple_lane','resident_zhou',4,'Property management enforces quiet hours at midday; bedrooms facing the street can hear traffic noise during the morning rush.','{"tags":["noise","property"],"severity":1,"hidden":0}','2026-07-13T18:30:00+08:00');
INSERT INTO "reviews" ("review_id","merchant_id","user_id","rating","body","image_captions","created_at") VALUES ('rv_sunbay_guardrail','mer_sunbay_loft','resident_fang',2,'The LOFT balcony railing is too low, and there are many complaints about nearby nighttime construction, making it unsuitable for a young child sensitive to noise during naps.','{"tags":["guardrail","construction","noise"],"severity":2,"hidden":0}','2026-07-17T12:00:00+08:00');
INSERT INTO "reviews" ("review_id","merchant_id","user_id","rating","body","image_captions","created_at") VALUES ('rv_sunbay_fire','mer_sunbay_loft','resident_qin',3,'The stairs in the duplex are quite steep, and clutter in the shared corridor was previously cleared by property management. Families with young children should verify this onsite.','{"tags":["stairs","fire"],"severity":2,"hidden":0}','2026-07-10T09:40:00+08:00');
INSERT INTO merchants(merchant_id,name,category,city,area,address,phone,rating_tenths,review_count,avg_price_minor,price_band,hours,tags,has_private_room,max_party_size) VALUES
('mer_changhe_cleaning','Long River Peace-of-Mind Cleaning','home_service','Hangzhou','Binjiang','Long River Road 327','0571-86540819',45,286,26800,'$$','08:00-19:00','home services,post-construction cleaning,window-track cleaning',0,0),
('mer_jianghan_family_cafe','Jianghan Family-Friendly Light Meals','restaurant','Hangzhou','Binjiang','Jianghan Road 1515, 2nd Floor','0571-86690437',42,173,7200,'$$','10:30-20:30','children''s chairs,low-salt meals,reading corner',0,12),
('mer_baima_activity_room','White Horse Lake Community Activity Room','venue','Hangzhou','Binjiang','White Horse Lake Community Complex, 1st Floor','0571-86073156',44,98,3000,'$','09:00-20:00','parent-child activities,indoor,community reservation',1,30);
INSERT INTO reviews(review_id,merchant_id,user_id,rating,body,image_captions,created_at) VALUES
('rv_changhe_cleaning_window','mer_changhe_cleaning','user_family_han',4,'The technician brought a narrow-gap brush; the balcony window tracks and screens were priced separately, and the job was completed in two hours.','{"captions":["Cleaned window track"]}','2026-05-07T18:42:00+08:00'),
('rv_jianghan_cafe_salt','mer_jianghan_family_cafe','user_family_qiu',4,'The children''s meal can be ordered without sauce. After noon on Saturdays, you often have to wait for a high chair.','{"captions":["Children''s meal menu"]}','2026-06-08T13:16:00+08:00'),
('rv_baima_room_floor','mer_baima_activity_room','user_family_xu',5,'The wood floor was clean, the folding tables were stored in the storage room, and there was no step stool for children in the restroom.','{"captions":["Activity room entrance"]}','2026-04-21T10:28:00+08:00');
INSERT INTO deals(deal_id,merchant_id,title,description,price_minor,list_price_minor,serves,valid_until,status) VALUES
('deal_changhe_cleaning_windows','mer_changhe_cleaning','Deep cleaning for three window tracks','Includes removing and washing the screens; does not include high-rise exterior facade work.',19800,26000,1,'2026-06-30','expired'),
('deal_jianghan_weekday_lunch','mer_jianghan_family_cafe','Weekday parent-child meal for two','One staple food, one vegetable dish, and two room-temperature drinks.',8800,10800,2,'2026-07-15','sold_out');
COMMIT;
PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
INSERT INTO merchants(merchant_id,name,category,city,area,address,phone,rating_tenths,review_count,avg_price_minor,price_band,hours,tags,has_private_room,max_party_size) VALUES
('mer_clearair_binjiang','ClearAir Indoor Testing','home_service','Hangzhou','Binjiang District','1120 Jianghong Road','0571-86021875',46,318,68000,'$$','09:00-18:00','indoor air,on-site sampling,electronic reports',0,0),
('mer_childsafe_install','ChildSafe Home Protection','home_service','Hangzhou','Binjiang District','486 Changhe Road','0571-86630142',44,207,36000,'$$','08:30-19:00','window locks,furniture anchoring,rounded-corner treatment',0,0),
('mer_quiet_window','QuietView Window and Door Repair','home_service','Hangzhou','Binjiang District','901 Binsheng Road','0571-86952711',42,164,52000,'$$','09:00-17:30','window-gap sealing,hardware replacement,soundproofing strips',0,0),
('mer_green_move','Green Harmony Family Moving','home_service','Hangzhou','Binjiang District','188 Xixing Road','0571-86541096',45,552,88000,'$$','07:00-21:00','household moving,turnover boxes,furniture disassembly and assembly',0,0),
('mer_deepclean_home','FineLeaf Deep Cleaning','home_service','Hangzhou','Binjiang District','63 Jugong Road','0571-86772035',43,401,46000,'$$','08:00-20:00','post-renovation cleaning,dust removal,kitchen cleaning',0,0),
('mer_babyroom_paint','Sprout Children''s Room Maintenance','home_service','Hangzhou','Binjiang District','707 Binkang Road','0571-86391822',41,126,74000,'$$$','09:30-18:30','water-based touch-ups,wall maintenance,furniture care',0,0),
('mer_elevator_move','Elevator Large-Item Services','home_service','Hangzhou','Binjiang District','1550 Jiangnan Avenue','0571-86843309',39,94,99000,'$$$','07:30-19:30','large-item moving,elevator protection,excluding pianos',0,0),
('mer_home_network','NeighborNet Home Networking','home_service','Hangzhou','Binjiang District','520 Jianghui Road','0571-86077423',47,689,28000,'$','09:00-21:00','network port testing,router placement,low-voltage cabling organization',0,0),
('mer_mold_repair','Rainy Season Wall Repair Cooperative','home_service','Hangzhou','Binjiang District','318 Puyan Road','0571-86261547',40,173,61000,'$$','08:30-18:00','water infiltration checks,wall repairs,dampness treatment',0,0),
('mer_family_storage','Little Elephant Mini Storage Binjiang Branch','home_service','Hangzhou','Binjiang District','1208 South Ring Road','0571-86490218',45,244,120000,'$$$','08:00-20:00','short-term storage,damp-proof mats,at-home pickup',0,0);
INSERT INTO reviews(review_id,merchant_id,user_id,rating,body,image_captions,created_at) VALUES
('rv_clearair_chain','mer_clearair_binjiang','resident_qiu',5,'The sampler showed the sealed-sample number, and the report included the laboratory''s seal.','{"photos":["sealed sample bag","report cover"]}','2026-03-14T12:20:00+08:00'),
('rv_clearair_delay','mer_clearair_binjiang','resident_ma',3,'The report arrived one day later than promised during the rainy season.','{"photos":["shipping label"]}','2026-06-25T18:05:00+08:00'),
('rv_childsafe_screw','mer_childsafe_install','parent_hu',4,'The installer added wall anchors to the tall cabinet and cleaned the floor thoroughly.','{"photos":["fixing brackets"]}','2026-04-09T16:40:00+08:00'),
('rv_childsafe_rental','mer_childsafe_install','tenant_zhai',4,'The rental unit uses removable restrictors, leaving only very small holes after move-out.','{"photos":["window frame hardware"]}','2026-05-18T11:35:00+08:00'),
('rv_quietwindow_gap','mer_quiet_window','owner_sun',4,'After the weatherstripping was replaced, wind noise from the north-facing window gap was noticeably reduced.','{"photos":["old weatherstripping"]}','2026-02-27T19:10:00+08:00'),
('rv_quietwindow_quote','mer_quiet_window','tenant_luo',3,'The property viewing and inspection fee is itemized separately, and the quote is valid on the same day.','{}','2026-06-03T14:22:00+08:00'),
('rv_greenmove_boxes','mer_green_move','family_dai',5,'The reusable moving boxes arrived in advance and were collected the same evening after the move.','{"photos":["sealed boxes"]}','2026-03-30T21:15:00+08:00'),
('rv_greenmove_rain','mer_green_move','family_yan',4,'The mattress was given a double-layer waterproof cover on the rainy day.','{"photos":["mattress packaging"]}','2026-06-19T20:08:00+08:00'),
('rv_deepclean_tracks','mer_deepclean_home','tenant_shi',5,'The dust buildup in the window tracks and on top of the cabinets was cleaned very thoroughly.','{"photos":["window track after cleaning"]}','2026-04-22T17:32:00+08:00'),
('rv_deepclean_odor','mer_deepclean_home','tenant_kang',3,'The cleaning product smell lasted about half a day and dissipated after ventilation.','{}','2026-05-07T09:26:00+08:00'),
('rv_babyroom_color','mer_babyroom_paint','parent_lin',4,'The touch-up paint on the small area closely matched the original wall color, and the edges were barely noticeable.','{"photos":["repaired wall corner"]}','2026-01-24T15:55:00+08:00'),
('rv_babyroom_schedule','mer_babyroom_paint','owner_qian',3,'The carpenter and wall-finishing technician came on separate days.','{}','2026-06-11T19:44:00+08:00'),
('rv_elevator_padding','mer_elevator_move','owner_wu',4,'The elevator car protection panels were installed completely, and property management inspection went smoothly.','{"photos":["elevator protection panels"]}','2026-03-06T18:18:00+08:00'),
('rv_elevator_floorfee','mer_elevator_move','tenant_gao',2,'The hallway corner was narrow, so an additional labor fee was added on site.','{}','2026-05-29T10:07:00+08:00'),
('rv_network_mesh','mer_home_network','remote_worker_he',5,'The two routers were switched to wired backhaul, making the bedroom signal stable.','{"photos":["low-voltage wiring cabinet"]}','2026-02-18T20:30:00+08:00'),
('rv_network_cable','mer_home_network','remote_worker_meng',4,'The network cable labels were clear, and all the old RJ45 plugs were replaced.','{"photos":["cable labels"]}','2026-04-30T13:48:00+08:00'),
('rv_mold_source','mer_mold_repair','resident_feng',4,'They first located a leak caused by air-conditioner condensate, then repaired the wall.','{"photos":["pipe connection"]}','2026-05-12T16:21:00+08:00'),
('rv_mold_recurrence','mer_mold_repair','resident_liu',3,'Before the rainwater issue on the exterior wall was addressed, the interior wall repair peeled again.','{"photos":["peeled area"]}','2026-06-28T09:14:00+08:00'),
('rv_storage_humidity','mer_family_storage','family_pan',5,'The storage unit''s humidity records can be viewed in the mini program.','{"photos":["humidity chart"]}','2026-03-21T12:02:00+08:00'),
('rv_storage_access','mer_family_storage','family_zhou',4,'Picking up items on the weekend involved about a twenty-minute wait, but there were plenty of carts.','{}','2026-06-15T17:36:00+08:00');
INSERT INTO deals(deal_id,merchant_id,title,description,price_minor,list_price_minor,serves,valid_until,status) VALUES
('deal_air_two_rooms','mer_clearair_binjiang','Basic sampling for two bedrooms and one living room','Three sampling points, including delivery of a printed report.',59800,68000,1,'2026-06-30','expired'),
('deal_childproof_visit','mer_childsafe_install','Home child safety inspection','On-site measurement of window frames and tall-cabinet fixing locations.',16800,22000,1,'2026-05-31','expired'),
('deal_window_seal','mer_quiet_window','Weatherstripping maintenance for two windows','Includes weatherstripping and hardware lubrication.',42000,52000,2,'2026-07-15','sold_out'),
('deal_move_boxes','mer_green_move','Seven-day rental of twenty reusable moving boxes','Includes one delivery and one pickup within the urban area.',26000,32000,1,'2026-06-20','expired'),
('deal_kitchen_clean','mer_deepclean_home','Deep kitchen cleaning','Cleaning of the range hood exterior and cabinet surfaces.',32000,42000,1,'2026-07-10','expired'),
('deal_wall_touchup','mer_babyroom_paint','Three-square-meter wall repair','Uses the store''s standard white water-based paint.',56000,68000,1,'2026-05-18','expired'),
('deal_elevator_wrap','mer_elevator_move','Elevator car protection','Includes transportation and removal of the protection panels.',38000,45000,1,'2026-06-25','expired'),
('deal_network_test','mer_home_network','Whole-home network port speed test','Tests six wall plates and labels the wiring.',19900,28000,1,'2026-07-12','expired'),
('deal_damp_check','mer_mold_repair','Wall moisture-content inspection','Tests four wall corners and provides an on-site record.',29800,36000,1,'2026-06-08','expired'),
('deal_storage_month','mer_family_storage','Five-cubic-meter monthly storage unit','Includes basic dampness protection mats; transportation not included.',98000,120000,1,'2026-05-30','expired');
INSERT INTO merchant_qa(qa_id,merchant_id,user_id,question,answer,answered_by,created_at) VALUES
('qa_air_lab','mer_clearair_binjiang','user_han','Which laboratory issues the report?','The partner is Hangzhou Chengming Testing Laboratory.','Merchant customer service','2026-04-02T10:12:00+08:00'),
('qa_childsafe_frame','mer_childsafe_install','user_jiang','What type of restrictor can be installed on a uPVC window?','The store stocks both clamp-on and screw-mounted models.','Installation supervisor','2026-04-16T14:28:00+08:00'),
('qa_move_piano','mer_green_move','user_du','Does the service include upright pianos?','The standard package does not include piano moving.','Dispatcher','2026-05-04T09:46:00+08:00'),
('qa_network_ports','mer_home_network','user_xie','What should I do if an older home has no network wall plates?','The low-voltage conduits can be checked first to see whether cables can be run through them.','Network engineer','2026-03-12T19:33:00+08:00'),
('qa_storage_insurance','mer_family_storage','user_miao','What items are covered by the basic insurance?','The terms exclude cash, identification documents, and fragile collectibles.','Storage customer service','2026-06-07T11:08:00+08:00');
COMMIT;
