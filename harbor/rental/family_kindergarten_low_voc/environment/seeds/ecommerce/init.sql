PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM "stocks";
DELETE FROM "refunds";
DELETE FROM "cart_items";
DELETE FROM "skus";
DELETE FROM "order_status_history";
DELETE FROM "order_items";
DELETE FROM "applied_coupons";
DELETE FROM "products";
DELETE FROM "orders";
DELETE FROM "coupons";
DELETE FROM "carts";
DELETE FROM "addresses";
INSERT INTO "carts" ("user_id","updated_at") VALUES ('usr_family_038','2026-07-18T09:00:00+08:00');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prd_window_lock_child','Child Safety Window Lock Set','ChildSafe','Baby & Maternity','Aluminum-alloy sliding window restrictors. The standard version fits 12–18 mm window tracks. The package includes two lock bodies and a hex key; measure the window frame before installation.',4.7,2400,9000,7900,'7-day no-reason returns');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prd_corner_guard','Child Safety Bumper Strip Set','ChildSafe','Baby & Maternity','Bumper strips for table and wall corners, to be prepared before move-in.',4.6,1900,8500,5600,'7-day no-reason returns');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prd_air_test_box','Air Quality Test Box Reference Kit','AirHome','Home','For self-testing reference only; it cannot replace a professional testing report.',4.2,980,3100,12900,'Returnable if unopened');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prd_cabinet_latch','Drawer Cabinet Door Safety Lock','SafeNest','Mother and Baby','No-drill safety lock; verify the cabinet door material. ',4.5,860,2400,4900,'7-day no-reason returns');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prd_stair_gate','Child Stair Safety Gate','Kido','Mother and Baby','Only suitable for homes with indoor stairs; measure the width before installation.',4.4,620,1700,19900,'Non-quality issues cannot be returned after installation');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prd_low_voc_sealant','Low-Odor Water-Based Sealant','HomeCare','Home','For small-scale gap maintenance; cannot replace pollution source testing.',4.3,430,980,6900,'Returnable if unopened');
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_prd_window_lock_child','prd_window_lock_child','{"specification": "Standard"}',7900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_prd_corner_guard','prd_corner_guard','{"specification": "Standard"}',5600);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_prd_air_test_box','prd_air_test_box','{"specification": "Standard"}',12900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_cabinet_latch','prd_cabinet_latch','{"Specification":"8-piece pack"}',4900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_stair_gate','prd_stair_gate','{"Width":"75-82cm"}',19900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_low_voc_sealant','prd_low_voc_sealant','{"Capacity":"300ml"}',6900);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_prd_window_lock_child',20);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_prd_corner_guard',21);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_prd_air_test_box',22);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_cabinet_latch',18);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_stair_gate',6);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_low_voc_sealant',12);
COMMIT;
PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
INSERT INTO products(product_id,title,brand,category,description,rating,rating_count,sales_count,base_price_minor,return_policy) VALUES
('prd_blackout_curtain','Blackout Curtains for Children''s Room','LumaHome','Home','Double-layer fabric, finished width 150 centimeters.',4.6,1380,5200,18900,'Custom sizes cannot be returned'),
('prd_white_noise_machine','Portable White Noise Machine','SleepPebble','Mother & Baby','Built-in eight ambient sounds, usable with a rechargeable battery.',4.5,2240,8600,15900,'7-day no-questions-asked returns'),
('prd_cable_box','Power Strip Organizer Box','NeatDesk','Home','Two openings on top; the box body has a V0 flame-retardant rating.',4.4,3160,12100,6900,'7-day no-questions-asked returns'),
('prd_furniture_anchor','Tall Cabinet Anti-Tip Straps','SafeNest','Mother & Baby','Set of two, including expansion screws and metal buckles.',4.7,1870,7300,8800,'Opened items cannot be returned for non-quality issues'),
('prd_door_guard','Door Finger Guard Strip','Kido','Mother & Baby','Foam strip covers the hinge side of the door, 120 centimeters long.',4.3,940,2800,3600,'7-day no-questions-asked returns'),
('prd_dehumidifier_box','Six-Pack Wardrobe Moisture Absorbers','DryLeaf','Home','Calcium chloride granules and the water collection box are sealed in separate layers.',4.5,4520,19800,5200,'Food and consumables cannot be returned'),
('prd_lux_meter','Pocket Illuminance Meter','MeterLab','Hardware Tools','Measures up to 200,000 lux, with a backlit display.',4.6,630,1700,7600,'15-day quality-related returns or exchanges'),
('prd_socket_tester','Socket Polarity Tester','VoltCheck','Hardware Tools','Three lights indicate the live, neutral, and grounding status.',4.8,1100,4300,9900,'Non-quality issues cannot be returned after being powered on'),
('prd_folding_step','Non-Slip Folding Step Stool','HomeStep','Home','Expanded height 22 centimeters, rated load capacity 100 kilograms.',4.4,2780,9500,5900,'7-day no-questions-asked returns'),
('prd_moving_labels','Moving Room Label Stickers','PackMark','Office Supplies','Eight-color zone labels, 160 stickers in total.',4.7,760,3100,2900,'Unopened items can be returned');
INSERT INTO skus(sku_id,product_id,attrs_json,price_minor) VALUES
('sku_blackout_curtain_gray','prd_blackout_curtain','{"Color":"Light Gray","Width":"150cm"}',18900),
('sku_white_noise_machine_mint','prd_white_noise_machine','{"Color":"Mint Green"}',15900),
('sku_cable_box_large','prd_cable_box','{"Size":"Large","Color":"White"}',6900),
('sku_furniture_anchor_pair','prd_furniture_anchor','{"Quantity":"2 straps"}',8800),
('sku_door_guard_120','prd_door_guard','{"Length":"120cm"}',3600),
('sku_dehumidifier_six','prd_dehumidifier_box','{"Quantity":"6 pieces"}',5200),
('sku_lux_meter_standard','prd_lux_meter','{"Range":"200000lx"}',7600),
('sku_socket_tester_cn','prd_socket_tester','{"Plug":"Chinese standard three-prong"}',9900),
('sku_folding_step_blue','prd_folding_step','{"Color":"Dark Blue"}',5900),
('sku_moving_labels_eight','prd_moving_labels','{"Color":"8 colors"}',2900);
INSERT INTO stocks(sku_id,quantity) VALUES
('sku_blackout_curtain_gray',14),
('sku_white_noise_machine_mint',27),
('sku_cable_box_large',53),
('sku_furniture_anchor_pair',9),
('sku_door_guard_120',61),
('sku_dehumidifier_six',88),
('sku_lux_meter_standard',7),
('sku_socket_tester_cn',22),
('sku_folding_step_blue',35),
('sku_moving_labels_eight',104);
INSERT INTO coupons(code,kind,value_bp_or_minor,min_spend_minor,valid_from,valid_until,category_restriction,max_uses,used_count,active) VALUES
('HOMEJAN30','percent_off',700,30000,'2026-01-05T00:00:00+08:00','2026-01-31T23:59:59+08:00','Home',500,412,0),
('KIDSAPRIL','flat_off',1200,10000,'2026-04-01T00:00:00+08:00','2026-04-20T23:59:59+08:00','Mother & Baby',300,300,0),
('TOOLS618','percent_off',850,20000,'2026-06-10T00:00:00+08:00','2026-06-18T23:59:59+08:00','Hardware Tools',800,756,0),
('SHIPMAY','free_shipping',0,5900,'2026-05-01T00:00:00+08:00','2026-05-07T23:59:59+08:00',NULL,1200,1190,0),
('STATIONERYJUN','flat_off',500,3000,'2026-06-20T00:00:00+08:00','2026-06-30T23:59:59+08:00','Office Supplies',250,186,0);
INSERT INTO addresses(address_id,user_id,recipient,phone,province,city,district,detail,postal_code,is_default) VALUES
('addr_family_old_east','usr_family_038','Lin Lan','13800000000','Zhejiang','Hangzhou','Binjiang District','Beside the parcel locker at the east gate of the old residence','310000',0),
('addr_family_office','usr_family_038','Lin Lan','13800000000','Zhejiang','Hangzhou','Shangcheng District','Front desk of the office building in Qianjiang New City CBD','310016',0),
('addr_family_grandma','usr_family_038','Zhou Minhua','13700000018','Zhejiang','Shaoxing','Yuecheng District','Old residence on Fushan Subdistrict','312000',0),
('addr_family_daycare','usr_family_038','Teacher of the Orange Class','13600000027','Zhejiang','Hangzhou','Binjiang District','Former daycare security office','310052',0),
('addr_family_photo_shop','usr_family_038','Binjiang Photo Studio','13900000045','Zhejiang','Hangzhou','Binjiang District','Front desk of the photo studio on Tai''an Road','310051',0);
COMMIT;
