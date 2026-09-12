PRAGMA foreign_keys=ON;

-- Stage 0 notification translated text ：2026-06-15 09:00  translated text table translated text 、 translated text 、statement translated text publicrules translated text ，excluding translated text review translated text 。
INSERT INTO subscriptions VALUES
('sub_awch_log','usr_mo_fan','delivery_logistics','keyword','YTOAWCH5520002CN','{"keywords":[" translated text "," translated text ","delivery receipt"," translated text "],"order_id":"ord_awch_0002"}','active','2026-06-01T09:15:00+08:00','2026-06-14T08:05:00+08:00'),
('sub_awch_card','usr_mo_fan','credit_card','keyword','card_awch_01','{"keywords":["foreign currency","duplicate charge","dispute"]}','active','2026-05-16T09:00:00+08:00','2026-06-10T10:00:00+08:00'),
('sub_awch_trade','usr_mo_fan','ecommerce','policy_update','prod_awch_main','{"topics":["battery health","appearancecondition"," translated text "]}','active','2026-05-25T14:00:00+08:00','2026-06-13T16:20:00+08:00'),
('sub_awch_price','usr_mo_fan','ecommerce','price_drop','prod_awch_005','{"drop_percent":8,"include_tradein":false}','active','2026-05-29T20:30:00+08:00','2026-06-14T19:10:00+08:00'),
('sub_awch_listing','usr_mo_fan','listing_platform','keyword','Apple Watch Ultra','{"keywords":[" translated text ","battery health"," translated text item"]}','paused','2026-06-03T21:00:00+08:00','2026-06-12T20:45:00+08:00'),
('sub_awch_weather','usr_mo_fan','weather','policy_update',' translated text ','{"kinds":["rain","storm","heat"]}','active','2026-06-02T07:15:00+08:00','2026-06-02T07:15:00+08:00');

INSERT INTO notifications VALUES
('N-ECO-260611-7K3M','usr_mo_fan','ecommerce','order_update',NULL,' translated text table translated text ','ord_awch_0001  translated text ， translated text  SF8259520001CN。','{"order_id":"ord_awch_0001","status":"shipped"}','2026-06-11T09:08:00+08:00',1),
('N-LOG-260614-5Q7V','usr_mo_fan','delivery_logistics','shipment_update','sub_awch_log',' translated text ','YTOAWCH5520002CN  translated text ，delivery receipt translated text 。','{"tracking_no":"YTOAWCH5520002CN","status":"picked_up"}','2026-06-14T08:03:00+08:00',0),
('N-POL-260613-6D2R','usr_mo_fan','ecommerce','policy_update','sub_awch_trade',' translated text ',' translated text verifyserial number、battery health、 translated text condition， translated text retain translated text record。','{"product_id":"prod_awch_main","order_id":"ord_awch_0002"}','2026-06-13T16:25:00+08:00',0),
('N-CARD-260610-7H9C','usr_mo_fan','credit_card','statement_ready','sub_awch_card',' translated text statement translated text generated',' translated text separate translated text ，foreign currency translated text 。','{"card_id":"card_awch_01","statement_month":"2026-06"}','2026-06-10T10:02:00+08:00',1),
('N-PRICE-260612-6M3X','usr_mo_fan','ecommerce','price_watch','sub_awch_price',' translated text table translated text ','Apple Watch Ultra 2  translated text active translated text ， translated text table translated text table translated text 。','{"product_id":"prod_awch_005","event":"display_price_changed"}','2026-06-12T20:35:00+08:00',1),
('N-LIST-260611-7P8K','usr_mo_fan','listing_platform','market_update','sub_awch_listing',' translated text model translated text ','Apple Watch Ultra  translated text ， translated text 、appearance translated text itemcomplete translated text 。','{"query":"Apple Watch Ultra","new_samples":5}','2026-06-11T19:18:00+08:00',1),
('N-WX-260614-8T2N','usr_mo_fan','weather','daily_brief','sub_awch_weather',' translated text ',' translated text ， translated text note translated text item。','{"geo":" translated text ","condition":"showers"}','2026-06-14T07:02:00+08:00',1),
('N-CPN-260614-4C5J','usr_mo_fan','ecommerce','coupon_expiry',NULL,'wearable accessorycoupon translated text ','AWCH_BAND_30  translated text item translated text ， translated text status translated text 。','{"coupon":"AWCH_BAND_30"}','2026-06-14T09:08:00+08:00',1),
('N-ADDR-260612-5V7L','usr_mo_fan','delivery_logistics','address_check','sub_awch_log','shipment translated text confirm',' translated text shipment translated text verify， translated text item translated text 。','{"address_id":"addr_awch_1"}','2026-06-12T17:35:00+08:00',1),
('N-OA-260608-6R4F','usr_mo_fan','official_account','new_content',NULL,'smartwatch translated text record translated text ','official translated text serial number、 translated text 、 translated text 、 translated text status translated text 。','{"post_id":"post_awch_02"}','2026-06-08T10:05:00+08:00',1),
('N-CART-260614-6K9D','usr_mo_fan','ecommerce','cart_reminder',NULL,'cart translated text item translated text ',' translated text watch band translated text cart， translated text 、 translated text active translated text place an order translated text confirm。','{"cart_items":["cart_awch_01","cart_awch_02"]}','2026-06-14T22:05:00+08:00',0),
('N-SVC-260606-7N2Q','usr_mo_fan','notification_hub','service_notice',NULL,' translated text recovery','notification translated text ； translated text order、amount translated text status translated text verify。','{"maintenance":"completed"}','2026-06-06T06:15:00+08:00',1),
('N-UTILITY-260604-9H4M','usr_mo_fan','utility','bill_paid',NULL,'Home translated text statement translated text ',' translated text  18.6  translated text ，statement 57.30  translated text account translated text 。','{"month":"2026-05","usage_cubic_m":18.6,"amount_minor":5730}','2026-06-04T08:34:00+08:00',1),
('N-GROCERY-260610-8B5T','usr_mo_fan','grocery','refund_complete',NULL,' translated text refund translated text ',' translated text order translated text ，refund 22.80  translated text refunded translated text payaccount。','{"item":" translated text ","amount_minor":2280,"status":"refunded"}','2026-06-10T20:42:00+08:00',1),
('N-MUSEUM-260602-6X7P','usr_mo_fan','museum','membership_record',NULL,' translated text ',' translated text Home translated text ， translated text ， translated text 。','{"month":"2026-05","visits":3,"venues":[" translated text "," translated text "]}','2026-06-02T12:16:00+08:00',1),
('N-PHOTO-260603-4L3C','usr_mo_fan','photo_archive','backup_complete',NULL,' translated text photosarchive translated text ',' translated text  27  translated text photos， translated text group。','{"album":" translated text ","photos":27,"burst_groups":5}','2026-06-03T22:48:00+08:00',1),
('N-VET-260607-5Q8V','usr_mo_fan','veterinary','medical_record',NULL,' translated text ',' translated text batch translated text ， translated text record translated text  4.6  translated text 。','{"pet":" translated text ","vaccine":" translated text ","weight_kg":4.6,"visit_date":"2026-06-07"}','2026-06-07T16:27:00+08:00',1),
('N-NET-260608-7J4R','usr_mo_fan','broadband','speed_test',NULL,'Home translated text ',' translated text  923Mbps、 translated text  96Mbps， translated text  18ms。','{"wired_down_mbps":923,"wired_up_mbps":96,"wifi_latency_ms":18}','2026-06-08T09:52:00+08:00',1),
('N-COFFEE-260609-3M8K','usr_mo_fan','coffee_subscription','delivery_complete',NULL,' translated text ',' translated text ， translated text 。','{"bags":3,"varieties":[" translated text "," translated text "],"roasted_on":"2026-06-06"}','2026-06-09T14:33:00+08:00',1),
('N-FILTER-260610-8P2D','usr_mo_fan','home_appliance','filter_usage',NULL,'air translated text ',' translated text  1,146  translated text ，current translated text  37%。','{"room":" translated text ","runtime_hours":1146,"filter_life_percent":37}','2026-06-10T07:19:00+08:00',1),
('N-BIKE-260611-4T9F','usr_mo_fan','bike_parking','session_closed',NULL,' translated text ',' translated text  31  translated text ， translated text 。','{"origin":" translated text ","destination":" translated text ","duration_minutes":31,"parking":"geofence"}','2026-06-11T19:04:00+08:00',1),
('N-MAG-260613-9V5H','usr_mo_fan','digital_magazine','archive_synced',NULL,' translated text content translated text ','《 translated text 》 translated text  24  translated text 。','{"publication":" translated text ","issues":["2026-03","2026-04","2026-05"],"saved_articles":24}','2026-06-13T08:43:00+08:00',1);

INSERT INTO price_alerts VALUES
('alr_awch_1','usr_mo_fan','prod_awch_005',599900,'CNY','active','2026-05-29T20:32:00+08:00'),
('alr_awch_2','usr_mo_fan','prod_awch_006',329900,'CNY','active','2026-05-30T19:20:00+08:00'),
('alr_awch_3','usr_mo_fan','prod_awch_017',69900,'CNY','triggered','2026-05-04T08:20:00+08:00');

INSERT INTO official_accounts VALUES
('oa_awch_brand','Apple  translated text ','shopping_service',' translated text 、 translated text 、 translated text description'),
('oa_awch_recycle',' translated text ','consumer_service',' translated text table translated text 、appraisalprocess translated text '),
('oa_awch_card',' translated text ','finance','statement、foreign currency translated text dispute translated text '),
('oa_awch_consumer',' translated text ','consumer_rights',' translated text receipt translated text '),
('oa_awch_weather',' translated text ','weather',' translated text 、alert translated text ');
INSERT INTO official_account_subscriptions VALUES
('usr_mo_fan','oa_awch_brand','2026-05-16T09:00:00+08:00'),
('usr_mo_fan','oa_awch_recycle','2026-05-25T14:00:00+08:00'),
('usr_mo_fan','oa_awch_card','2026-04-16T09:00:00+08:00'),
('usr_mo_fan','oa_awch_weather','2026-06-02T07:15:00+08:00');
INSERT INTO official_account_posts VALUES
('post_awch_01','oa_awch_brand','serial number、model translated text status translated text verify',' translated text serial number translated text table，table translated text 、 translated text receipt translated text verify。','https://brand.example/awch/device-id','2026-06-04T11:05:00+08:00'),
('post_awch_02','oa_awch_recycle',' translated text smartwatch translated text record','recommendation translated text 、 translated text 、table translated text 、 translated text 、charging、 translated text 、 translated text 。','https://recycle.example/awch/evidence','2026-06-08T10:00:00+08:00'),
('post_awch_03','oa_awch_recycle','battery health translated text appearancecondition translated text appraisal',' translated text appraisal translated text user translated text ，final translated text 、table translated text 、 translated text record。','https://recycle.example/awch/quote','2026-06-02T15:20:00+08:00'),
('post_awch_04','oa_awch_card','foreign currency translated text formal translated text status translated text ',' translated text amount、 translated text ； translated text verify translated text recordmerchant、amount、 translated text 。','https://card.example/awch/fx','2026-06-05T09:15:00+08:00'),
('post_awch_05','oa_awch_consumer',' translated text trade-in appraisaldispute translated text ',' translated text 、 translated text 、 translated text delivery receipt、 translated text record，avoid translated text retain translated text 。','https://consumer.example/awch/tradein','2026-06-03T14:05:00+08:00'),
('post_awch_06','oa_awch_weather',' translated text recommendation',' translated text retain translated text photos， translated text verify translated text rules。','https://weather.example/awch/shipping','2026-06-11T07:05:00+08:00'),
('post_awch_07','oa_awch_brand',' translated text table translated text table translated text separateconfirm',' translated text 、 translated text coupon translated text table translated text separate translated text item， translated text retaineach translated text amount。','https://brand.example/awch/tradein-rules','2026-05-30T16:35:00+08:00'),
('post_awch_08','oa_awch_card','dispute translated text statement','disputesubmitted translated text accepted translated text ， translated text statement translated text rules translated text amount due translated text 。','https://card.example/awch/dispute','2026-06-12T09:30:00+08:00');
INSERT INTO _counters VALUES ('notification',22),('subscription',6),('post',8);
