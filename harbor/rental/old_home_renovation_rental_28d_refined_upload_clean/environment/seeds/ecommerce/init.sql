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
INSERT INTO "addresses" ("address_id","user_id","recipient","phone","province","city","district","detail","postal_code","is_default") VALUES ('addr_hj603','usr_zhanglan','Zhang Lan','13900001111','Shanghai','Shanghai','Minhang','Unit 603, Hongqiao Jiayuan','201100',1);
INSERT INTO "carts" ("user_id","updated_at") VALUES ('usr_zhanglan','2026-07-01T08:00:00+08:00');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_haier_fridge_210l','translated source text 210L','translated source text','appliances','Core rental appliance: one standard refrigerator is required; this is not a luxury upgrade.',4.7,836,2146,219900,'7translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_littleswan_washer_8kg','translated source text 8kg','translated source text','appliances','Core rental appliance: one standard washer is required; this is not a luxury upgrade.',4.5,572,1379,189900,'7translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_mijia_air_purifier','mtranslated source text','mtranslated source text','appliances','Optional air purifier after the formal air-quality gate; not part of the required core pair.',4.8,1245,3862,89900,'7translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_luxe_fridge_620l','Luxe translated source text 620L','Luxe','appliances','translated source text，translated source textandtranslated source text。',4.2,47,63,1689900,'7translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_shewei_smart_toilet','translated source text X9','translated source text','kitchen and bathroom','translated source text、translated source textandtranslated source text。',4.4,92,118,980000,'translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_nord_oak_flooring','Nord translated source text','Nord','translated source text','translated source text，translated source text。',4.1,31,24,2380000,'translated source text');
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_haier_fridge_210l_white','prod_haier_fridge_210l','{"translated source text":"translated source text"}',219900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_littleswan_washer_8kg_white','prod_littleswan_washer_8kg','{"translated source text":"translated source text"}',189900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_mijia_air_purifier_white','prod_mijia_air_purifier','{"translated source text":"translated source text"}',89900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_luxe_fridge_620l_silver','prod_luxe_fridge_620l','{"translated source text":"translated source text"}',1689900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_shewei_toilet_x9_white','prod_shewei_smart_toilet','{"translated source text":"translated source text"}',980000);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_nord_oak_flooring_natural','prod_nord_oak_flooring','{"translated source text":"translated source text"}',2380000);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_haier_fridge_210l_white',12);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_littleswan_washer_8kg_white',10);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_mijia_air_purifier_white',8);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_luxe_fridge_620l_silver',3);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_shewei_toilet_x9_white',6);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_nord_oak_flooring_natural',5);
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_opple_led_ceiling_24w','translated source text 24W translated source text','translated source text','translated source text','translated source textm，translated source text。',4.7,864,2310,15900,'translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_davco_k11_waterproof','translated source text K11 kitchen and bathroomtranslated source text 18kg','translated source text','translated source text','translated source text，translated source textm，translated source text。',4.8,527,1180,23800,'translated source textnottranslated source text7translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_panasonic_exhaust_165','translated source text 165mm','translated source text','kitchen and bathroom','translated source textm，translated source textm。',4.5,311,740,42900,'translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_honeywell_smoke_pair','translated source text translated source text','translated source text','translated source text','translated source text，translated source text，translated source text。',4.6,193,506,12800,'nottranslated source text15translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_jinpoint_lock_cylinder_c','translated source text Ctranslated source text 75mm','translated source text','translated source text','translated source textm，translated source textmtranslated source textmtranslated source text。',4.7,448,967,26900,'translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_molike_curtain_180','translated source text 1.8m translated source text','translated source text','translated source text','translated source textm、translated source textm，translated source text，translated source text。',4.3,286,612,32900,'translated source textnottranslated source text，translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_gree_dehumidifier_12l','translated source text  daytranslated source text12L','translated source text','appliances','translated source text，translated source text，translated source text。',4.4,372,825,79900,'translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_midea_microwave_20l','translated source text 20L','translated source text','appliances','translated source text，translated source textm，translated source textm。',4.6,1035,3420,39900,'translated source textandtranslated source text7translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_hota_drying_rack_x','translated source text translated source text','translated source text','translated source text','translated source textm，translated source text，translated source textm。',4.2,154,398,18900,'translated source text7translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_jomoo_faucet_33080','translated source text 33080','translated source text','kitchen and bathroom','translated source text，translated source text，translated source text。',4.8,679,1406,21900,'translated source texttreatment');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_dohia_mattress_pad_150','translated source text 150×200cm','translated source text','translated source text','translated source text，translated source text，translated source textmtranslated source text。',4.5,221,477,9900,'translated source text');
INSERT INTO "products" ("product_id","title","brand","category","description","rating","rating_count","sales_count","base_price_minor","return_policy") VALUES ('prod_karcher_wd1_vacuum','translated source text WD1 translated source text','translated source text','translated source text','translated source text，translated source textrenovationtranslated source text，translated source textm。',4.6,147,329,56900,'translated source text');
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_opple_led_ceiling_24w_white','prod_opple_led_ceiling_24w','{"translated source text":"translated source text","translated source text":"translated source text"}',15900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_davco_k11_waterproof_grey','prod_davco_k11_waterproof','{"translated source text":"18kg","translated source text":"translated source text"}',23800);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_panasonic_exhaust_165_white','prod_panasonic_exhaust_165','{"translated source text":"translated source text","translated source text":"100mm"}',42900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_honeywell_smoke_pair_battery','prod_honeywell_smoke_pair','{"quantity":"2translated source text","translated source text":"translated source text"}',12800);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_jinpoint_lock_cylinder_75_brass','prod_jinpoint_lock_cylinder_c','{"translated source text":"75mm","translated source text":"translated source text"}',26900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_molike_curtain_180_grey','prod_molike_curtain_180','{"translated source text":"translated source text","translated source text":"180×240cm"}',32900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_gree_dehumidifier_12l_white','prod_gree_dehumidifier_12l','{"translated source text":"translated source text","translated source text":"2.5L"}',79900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_midea_microwave_20l_black','prod_midea_microwave_20l','{"translated source text":"translated source text","translated source text":"translated source text"}',39900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_hota_drying_rack_x_silver','prod_hota_drying_rack_x','{"translated source text":"translated source text","translated source text":"translated source text"}',18900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_jomoo_faucet_33080_chrome','prod_jomoo_faucet_33080','{"translated source text":"translated source text","translated source text":"translated source text"}',21900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_dohia_mattress_pad_150_white','prod_dohia_mattress_pad_150','{"translated source text":"150×200cm","translated source text":"translated source text"}',9900);
INSERT INTO "skus" ("sku_id","product_id","attrs_json","price_minor") VALUES ('sku_karcher_wd1_vacuum_yellow','prod_karcher_wd1_vacuum','{"translated source text":"12L","translated source text":"translated source text"}',56900);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_opple_led_ceiling_24w_white',26);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_davco_k11_waterproof_grey',17);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_panasonic_exhaust_165_white',4);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_honeywell_smoke_pair_battery',31);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_jinpoint_lock_cylinder_75_brass',9);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_molike_curtain_180_grey',13);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_gree_dehumidifier_12l_white',2);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_midea_microwave_20l_black',22);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_hota_drying_rack_x_silver',7);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_jomoo_faucet_33080_chrome',18);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_dohia_mattress_pad_150_white',35);
INSERT INTO "stocks" ("sku_id","quantity") VALUES ('sku_karcher_wd1_vacuum_yellow',5);
INSERT INTO "coupons" ("code","kind","value_bp_or_minor","min_spend_minor","valid_from","valid_until","category_restriction","max_uses","used_count","active") VALUES ('LIGHTING-MAR26','flat_off',3000,19900,'2026-03-01T00:00:00+08:00','2026-03-31T23:59:59+08:00','translated source text',800,764,0);
INSERT INTO "coupons" ("code","kind","value_bp_or_minor","min_spend_minor","valid_from","valid_until","category_restriction","max_uses","used_count","active") VALUES ('BATHROOM-APRIL','percent_off',850,50000,'2026-04-05T00:00:00+08:00','2026-04-20T23:59:59+08:00','kitchen and bathroom',420,420,0);
INSERT INTO "coupons" ("code","kind","value_bp_or_minor","min_spend_minor","valid_from","valid_until","category_restriction","max_uses","used_count","active") VALUES ('HOME-FREIGHT-MAY','free_shipping',0,12900,'2026-05-08T00:00:00+08:00','2026-05-18T23:59:59+08:00','translated source text',1200,1187,0);
INSERT INTO "coupons" ("code","kind","value_bp_or_minor","min_spend_minor","valid_from","valid_until","category_restriction","max_uses","used_count","active") VALUES ('CLEAN-JUNE-40','flat_off',4000,39900,'2026-06-01T00:00:00+08:00','2026-06-15T23:59:59+08:00','translated source text',360,219,0);
INSERT INTO "coupons" ("code","kind","value_bp_or_minor","min_spend_minor","valid_from","valid_until","category_restriction","max_uses","used_count","active") VALUES ('TEXTILE-SUMMER','percent_off',900,19900,'2026-06-12T00:00:00+08:00','2026-06-30T23:59:59+08:00','translated source text',650,401,0);
INSERT INTO "addresses" ("address_id","user_id","recipient","phone","province","city","district","detail","postal_code","is_default") VALUES ('addr_zhanglan_xuhui_old','usr_zhanglan','Zhang Lan','13900001111','Shanghai','Shanghai','translated source text','translated source text18translated source text302translated source text','200233',0);
INSERT INTO "addresses" ("address_id","user_id","recipient","phone","province","city","district","detail","postal_code","is_default") VALUES ('addr_zhanglan_parent_putuo','usr_zhanglan','Zhang Lan','13900001111','Shanghai','Shanghai','translated source text','translated source text465translated source text7translated source text501translated source text','200062',0);
INSERT INTO "addresses" ("address_id","user_id","recipient","phone","province","city","district","detail","postal_code","is_default") VALUES ('addr_zhanglan_work_lobby','usr_zhanglan','Zhang Lan','13900001111','Shanghai','Shanghai','Changning','translated source text1438translated source textAtranslated source text','200051',0);
INSERT INTO "orders" ("order_id","user_id","address_id","payment_method","subtotal_minor","discount_minor","shipping_minor","total_minor","status","placed_at","note","tracking_no") VALUES ('ord_ceiling_lamp_202602','usr_zhanglan','addr_zhanglan_xuhui_old','alipay',31800,3000,0,28800,'completed','2026-02-19T20:16:00+08:00','translated source text，translated source text。','YT26022094831');
INSERT INTO "orders" ("order_id","user_id","address_id","payment_method","subtotal_minor","discount_minor","shipping_minor","total_minor","status","placed_at","note","tracking_no") VALUES ('ord_dehumidifier_return_202604','usr_zhanglan','addr_zhanglan_parent_putuo','wechat_pay',79900,0,0,79900,'refunded','2026-04-11T09:42:00+08:00','translated source text。','JDVA0260411837');
INSERT INTO "orders" ("order_id","user_id","address_id","payment_method","subtotal_minor","discount_minor","shipping_minor","total_minor","status","placed_at","note","tracking_no") VALUES ('ord_curtain_lock_cancel_202605','usr_zhanglan','addr_zhanglan_xuhui_old','bank_card',59800,0,800,60600,'cancelled','2026-05-23T18:05:00+08:00','translated source textfoundtranslated source textandtranslated source text。',NULL);
INSERT INTO "order_items" ("item_id","order_id","product_id","sku_id","qty","unit_price_minor","line_total_minor") VALUES ('item_ceiling_lamp_pair','ord_ceiling_lamp_202602','prod_opple_led_ceiling_24w','sku_opple_led_ceiling_24w_white',2,15900,31800);
INSERT INTO "order_items" ("item_id","order_id","product_id","sku_id","qty","unit_price_minor","line_total_minor") VALUES ('item_dehumidifier_single','ord_dehumidifier_return_202604','prod_gree_dehumidifier_12l','sku_gree_dehumidifier_12l_white',1,79900,79900);
INSERT INTO "order_items" ("item_id","order_id","product_id","sku_id","qty","unit_price_minor","line_total_minor") VALUES ('item_curtain_wrong_width','ord_curtain_lock_cancel_202605','prod_molike_curtain_180','sku_molike_curtain_180_grey',1,32900,32900);
INSERT INTO "order_items" ("item_id","order_id","product_id","sku_id","qty","unit_price_minor","line_total_minor") VALUES ('item_lock_wrong_length','ord_curtain_lock_cancel_202605','prod_jinpoint_lock_cylinder_c','sku_jinpoint_lock_cylinder_75_brass',1,26900,26900);
INSERT INTO "order_status_history" ("order_id","status","set_at") VALUES ('ord_ceiling_lamp_202602','completed','2026-02-23T16:48:00+08:00');
INSERT INTO "order_status_history" ("order_id","status","set_at") VALUES ('ord_dehumidifier_return_202604','refunded','2026-04-18T14:22:00+08:00');
INSERT INTO "order_status_history" ("order_id","status","set_at") VALUES ('ord_curtain_lock_cancel_202605','cancelled','2026-05-23T18:37:00+08:00');
INSERT INTO "refunds" ("refund_id","order_id","item_id","qty","reason","status","opened_at","resolved_at","refund_amount_minor") VALUES ('ref_dehumidifier_noise','ord_dehumidifier_return_202604','item_dehumidifier_single',1,'translated source text，translated source textandtranslated source text。','refunded','2026-04-13T08:54:00+08:00','2026-04-18T14:22:00+08:00',79900);
COMMIT;
PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;
INSERT INTO products(product_id,title,brand,category,description,rating,rating_count,sales_count,base_price_minor,return_policy) VALUES
('prod_3m_door_stop_pair','3M translated source text translated source text','3M','translated source text','translated source text，translated source textm。',4.5,318,746,3900,'translated source text7translated source text'),
('prod_submarine_leak_alarm','translated source text','translated source text','translated source text','translated source text，translated source text，translated source text。',4.7,241,529,6900,'translated source text15translated source text'),
('prod_opple_led_bulb_9w_pack','translated source text 9W LED translated source text translated source text','translated source text','translated source text','E27 translated source text，translated source text，translated source text。',4.8,1260,4380,5900,'translated source text'),
('prod_dtc_cabinet_hinge_pair','translated source text translated source text','DTC','translated source text','translated source text，translated source textm，translated source text。',4.4,186,395,12900,'translated source textnottranslated source text'),
('prod_joybos_shower_rod','translated source text 110-190cm','translated source text','kitchen and bathroom','translated source text，translated source text，translated source text。',4.2,437,932,7900,'translated source text7translated source text'),
('prod_supor_induction_2100w','translated source text 2100W translated source text','translated source text','appliances','translated source text，translated source textm，translated source text。',4.6,785,2140,23900,'translated source text'),
('prod_kaadas_chain_lock','translated source text','translated source text','translated source text','translated source textm，translated source text。',4.3,109,228,8900,'translated source text');
INSERT INTO skus(sku_id,product_id,attrs_json,price_minor) VALUES
('sku_3m_door_stop_pair_grey','prod_3m_door_stop_pair','{"translated source text":"translated source text","quantity":"2translated source text"}',3900),
('sku_submarine_leak_alarm_white','prod_submarine_leak_alarm','{"translated source text":"translated source text","translated source text":"2translated source text7translated source text"}',6900),
('sku_opple_led_bulb_9w_4000k','prod_opple_led_bulb_9w_pack','{"translated source text":"9W","translated source text":"4000K","quantity":"4translated source text"}',5900),
('sku_dtc_cabinet_hinge_full_overlay','prod_dtc_cabinet_hinge_pair','{"translated source text":"translated source text","quantity":"2translated source text"}',12900),
('sku_joybos_shower_rod_white','prod_joybos_shower_rod','{"translated source text":"110-190cm","translated source text":"translated source text"}',7900),
('sku_supor_induction_2100w_black','prod_supor_induction_2100w','{"translated source text":"translated source text","translated source text":"translated source text"}',23900),
('sku_kaadas_chain_lock_silver','prod_kaadas_chain_lock','{"translated source text":"translated source text","translated source text":"translated source text"}',8900);
INSERT INTO stocks(sku_id,quantity) VALUES
('sku_3m_door_stop_pair_grey',42),
('sku_submarine_leak_alarm_white',16),
('sku_opple_led_bulb_9w_4000k',58),
('sku_dtc_cabinet_hinge_full_overlay',11),
('sku_joybos_shower_rod_white',24),
('sku_supor_induction_2100w_black',7),
('sku_kaadas_chain_lock_silver',19);
INSERT INTO coupons(code,kind,value_bp_or_minor,min_spend_minor,valid_from,valid_until,category_restriction,max_uses,used_count,active) VALUES
('HARDWARE-SPRING','flat_off',2000,9900,'2026-03-10T00:00:00+08:00','2026-03-24T23:59:59+08:00','translated source text',500,487,0),
('LIGHT-SAFETY-MAY','percent_off',920,19900,'2026-05-01T00:00:00+08:00','2026-05-12T23:59:59+08:00','translated source text',280,196,0);
INSERT INTO addresses(address_id,user_id,recipient,phone,province,city,district,detail,postal_code,is_default) VALUES ('addr_zhanglan_hardware_pickup','usr_zhanglan','Zhang Lan','13900001111','Shanghai','Shanghai','Minhang','translated source text286translated source text','201105',0);
INSERT INTO orders(order_id,user_id,address_id,payment_method,subtotal_minor,discount_minor,shipping_minor,total_minor,status,placed_at,note,tracking_no) VALUES ('ord_hinge_return_202605','usr_zhanglan','addr_zhanglan_hardware_pickup','wechat_pay',12900,0,600,13500,'refunded','2026-05-12T10:38:00+08:00','translated source text，translated source text。','ZTO260512DTC45');
INSERT INTO order_items(item_id,order_id,product_id,sku_id,qty,unit_price_minor,line_total_minor) VALUES ('item_hinge_full_overlay_return','ord_hinge_return_202605','prod_dtc_cabinet_hinge_pair','sku_dtc_cabinet_hinge_full_overlay',1,12900,12900);
INSERT INTO order_status_history(order_id,status,set_at) VALUES ('ord_hinge_return_202605','refunded','2026-05-19T16:26:00+08:00');
INSERT INTO refunds(refund_id,order_id,item_id,qty,reason,status,opened_at,resolved_at,refund_amount_minor) VALUES ('ref_hinge_wrong_overlay','ord_hinge_return_202605','item_hinge_full_overlay_return',1,'translated source textneedstranslated source text，translated source text。','refunded','2026-05-14T09:17:00+08:00','2026-05-19T16:26:00+08:00',12900);
COMMIT;
