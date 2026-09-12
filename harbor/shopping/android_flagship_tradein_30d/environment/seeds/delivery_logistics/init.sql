-- Stage 0 logistics state for Pan Yu; later valuation-review outcomes remain absent.
BEGIN;
INSERT INTO address_book (address_id,user_id,label,recipient,phone,province,city,district,detail,postal_code,is_default) VALUES
('ADDR-LP2099-GZ-7Q4M','usr_pan_yu','English business note','English business note(Pan Yu LP2099)','4001234567','Guangdong Province','Guangzhou City','Baiyun District','English business note A English business note 217 English business note LP2099 English business note','510410',0),
('ADDR-HZ-HOME-3K8V','usr_pan_yu','English business note','Pan Yu','13900000000','Zhejiang Province','Hangzhou City','Binjiang District','English business note 3588 English business note 2203','310052',1),
('ADDR-HZ-B3-6P2R','usr_pan_yu','English business note','Pan Yu','057188886666','Zhejiang Province','Hangzhou City','Binjiang District','English business note 699 English business note B3 English business note','310052',0);
INSERT INTO shipments (shipment_id,user_id,tracking_no,carrier,service_level,status,sender_json,recipient_json,weight_kg,dimensions_json,declared_value_minor,fee_minor,created_at,eta_date,scheduled_pickup_at,updated_at,cancel_reason) VALUES
('shp_andt_0001','usr_pan_yu','SF3724520001CN','SF Express','express','in_transit','{"recipient":"English business note","city":"Suzhou City","district":"Industrial Park"}','{"recipient":"Pan Yu","city":"Hangzhou City","district":"Binjiang District"}',1.3,'{"length_cm":34,"width_cm":24,"height_cm":6}',430000,0,'2026-06-13T09:00:00+08:00','2026-06-15',NULL,'2026-06-14T03:20:00+08:00',NULL),
('shp_andt_0002','usr_pan_yu','YTOANDT5520002CN','YTO Express','standard','in_transit','{"recipient":"English business note","city":"Dongguan City","district":"Chang an Town"}','{"recipient":"English business note(Pan Yu LP2099)","city":"Guangzhou City","district":"Baiyun District"}',1.1,'{"length_cm":22,"width_cm":16,"height_cm":9}',108000,800,'2026-06-15T08:30:00+08:00','2026-06-17',NULL,'2026-06-15T08:45:00+08:00',NULL),
('ship-JDVA77268831','usr_pan_yu','JDVA77268831','JD Logistics','same_day','delivered','{"recipient":"English business noteHangzhouEnglish business note"}','{"recipient":"Pan Yu","district":"Binjiang District"}',0.7,'{"length_cm":30,"width_cm":20,"height_cm":12}',35900,0,'2026-05-20T08:00:00+08:00','2026-05-20',NULL,'2026-05-20T18:12:00+08:00',NULL),
('ship-ZTO4821457712','usr_pan_yu','ZTO4821457712','ZTO Express','standard','delivered','{"recipient":"English business note"}','{"recipient":"Pan Yu","district":"Binjiang District"}',0.9,'{"length_cm":35,"width_cm":25,"height_cm":8}',52900,600,'2026-05-27T10:00:00+08:00','2026-05-30',NULL,'2026-05-29T14:30:00+08:00',NULL),
('ship-SFRA37240031','usr_pan_yu','SFRA37240031','SF Express','express','returned','{"recipient":"Pan Yu","district":"Binjiang District"}','{"recipient":"English business note","district":"Xihu District"}',0.4,'{"length_cm":20,"width_cm":14,"height_cm":8}',120000,1800,'2026-04-18T11:00:00+08:00','2026-04-19','2026-04-18T10:30:00+08:00','2026-04-20T09:20:00+08:00','English business note'),
('ship-EMS772093957CN','usr_pan_yu','EMS772093957CN','English business noteEMS','standard','cancelled','{"recipient":"Pan Yu","district":"Binjiang District"}','{"recipient":"English business note","city":"English business note"}',1.6,'{"length_cm":40,"width_cm":30,"height_cm":18}',32000,1800,'2026-05-06T09:00:00+08:00','2026-05-09','2026-05-06T14:00:00+08:00','2026-05-06T10:10:00+08:00','shipmentEnglish business note'),
('ship-SFANDT60488317CN','usr_pan_yu','SFANDT60488317CN','SF Express','express','delivered','{"recipient":"Pan Yu","district":"Binjiang District"}','{"recipient":"English business note","district":"Xihu District"}',1.5,'{"length_cm":48,"width_cm":22,"height_cm":9}',76000,1600,'2026-05-23T09:30:00+08:00','2026-05-24','2026-05-23T09:00:00+08:00','2026-05-24T11:18:00+08:00',NULL);
INSERT INTO shipment_events (event_id,shipment_id,at,location,status_code,description) VALUES
('SF3724520001CN-0613T0910-J6QA','shp_andt_0001','2026-06-13T09:10:00+08:00','English business noteIndustrial Park','picked_up','merchantalreadyEnglish business note'),
('SF3724520001CN-0614T0320-R3XM','shp_andt_0001','2026-06-14T03:20:00+08:00','HangzhouEnglish business note','in_transit','English business noteHangzhouEnglish business note'),
('YTOANDT5520002CN-0615T0845-B5LW','shp_andt_0002','2026-06-15T08:45:00+08:00','English business noteChang an Town','picked_up','officialEnglish business notealreadyEnglish business note'),
('JDVA77268831-0520T0900-H4PR','ship-JDVA77268831','2026-05-20T09:00:00+08:00','HangzhouEnglish business note','out_for_delivery','English business note'),
('JDVA77268831-0520T1812-C9VT','ship-JDVA77268831','2026-05-20T18:12:00+08:00','Hangzhou CityBinjiang District','delivered','English business notedelivery'),
('ZTO4821457712-0527T1200-M2GX','ship-ZTO4821457712','2026-05-27T12:00:00+08:00','English business note','picked_up','merchantEnglish business note'),
('ZTO4821457712-0529T1430-Q6NB','ship-ZTO4821457712','2026-05-29T14:30:00+08:00','Hangzhou CityBinjiang District','delivered','English business notedelivery'),
('SFRA37240031-0418T1110-A8SY','ship-SFRA37240031','2026-04-18T11:10:00+08:00','Hangzhou CityBinjiang District','picked_up','alreadyEnglish business note'),
('SFRA37240031-0419T1500-F5UE','ship-SFRA37240031','2026-04-19T15:00:00+08:00','Hangzhou CityXihu District','delivery_failed','English business notealreadyEnglish business note'),
('SFRA37240031-0420T0920-K3HZ','ship-SFRA37240031','2026-04-20T09:20:00+08:00','Hangzhou CityBinjiang District','returned','English business note'),
('EMS772093957CN-0506T0920-P7BJ','ship-EMS772093957CN','2026-05-06T09:20:00+08:00','Hangzhou CityBinjiang District','pickup_scheduled','appointmentEnglish business note'),
('EMS772093957CN-0506T1010-D4CW','ship-EMS772093957CN','2026-05-06T10:10:00+08:00','Hangzhou CityBinjiang District','cancelled','shipmentEnglish business note'),
('SFANDT60488317CN-0523T0912-X5MR','ship-SFANDT60488317CN','2026-05-23T09:12:00+08:00','Hangzhou CityBinjiang District','picked_up','English business notefromEnglish business note'),
('SFANDT60488317CN-0523T1855-G2KL','ship-SFANDT60488317CN','2026-05-23T18:55:00+08:00','HangzhouEnglish business note','in_transit','English business note'),
('SFANDT60488317CN-0524T1118-W8PV','ship-SFANDT60488317CN','2026-05-24T11:18:00+08:00','Hangzhou CityXihu District','delivered','English business notedelivery');
INSERT INTO pickups (pickup_id,shipment_id,scheduled_at,completed_at,status) VALUES
('PU-SFRA37240031-0418-A6K9','ship-SFRA37240031','2026-04-18T10:30:00+08:00','2026-04-18T11:10:00+08:00','completed'),
('PU-EMS772093957-0506-C4T7','ship-EMS772093957CN','2026-05-06T14:00:00+08:00',NULL,'cancelled'),
('PU-SFANDT60488317-0523-N8R2','ship-SFANDT60488317CN','2026-05-23T09:00:00+08:00','2026-05-23T09:12:00+08:00','completed');
INSERT INTO issue_tickets (ticket_id,shipment_id,issue_type,description,status,opened_at,expected_response_date,resolved_at) VALUES
('case-SFRA37240031-MV6D','ship-SFRA37240031','wrong_address','English business note，English business notepleaseEnglish business note','resolved','2026-04-19T15:10:00+08:00','2026-04-20','2026-04-20T09:20:00+08:00'),
('case-ZTO4821457712-SMS4','ship-ZTO4821457712','delivery_failed','English business note，English business notealreadyEnglish business note','resolved','2026-05-29T16:00:00+08:00','2026-05-30','2026-05-29T18:00:00+08:00'),
('case-SFANDT60488317-LST9','ship-SFANDT60488317CN','missing_item','English business notenot yetEnglish business note，shipmentEnglish business notedaysEnglish business note','closed','2026-05-24T12:05:00+08:00','2026-05-25','2026-05-24T15:40:00+08:00');
INSERT INTO status_subscriptions (subscription_id,shipment_id,channel,target,active,created_at) VALUES
('SUB-SF3724520001-6K8P','shp_andt_0002','email','pan.yu.tradein@gmail.com',1,'2026-06-15T09:00:00+08:00'),
('SUB-YTO5520002-4R7M','shp_andt_0001','sms','13900000000',0,'2026-06-13T09:00:00+08:00');
INSERT INTO notifications_outbox (subscription_id,payload_json,queued_at,sent_at) VALUES
('SUB-SF3724520001-6K8P','{"tracking_no":"YTOANDT5520002CN","status":"picked_up"}','2026-06-15T08:46:00+08:00','2026-06-15T08:46:00+08:00');
INSERT INTO _counters (key,value) VALUES ('shipment_seq',7),('event_seq',18),('pickup_seq',3),('ticket_seq',3),('subscription_seq',2),('outbox_seq',2),('address_seq',3);
COMMIT;
