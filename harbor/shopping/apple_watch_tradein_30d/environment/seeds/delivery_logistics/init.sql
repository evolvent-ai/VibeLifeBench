-- Stage 0 logistics state for  translated text ; later review and settlement outcomes are not present.
BEGIN;
INSERT INTO address_book (address_id,user_id,label,recipient,phone,province,city,district,detail,postal_code,is_default) VALUES
('abk_awch_1','usr_mo_fan',' translated text ',' translated text ( translated text  SY2099)','4001234567','Guangdong','Guangzhou','Baiyun',' translated text  A  translated text  217  translated text  SY2099  translated text ','510410',0),
('abk_awch_2','usr_mo_fan','Home',' translated text ','13900000000','Shanghai','Shanghai','Pudong',' translated text  88  translated text  1203','201203',1),
('abk_awch_3','usr_mo_fan','Office reception',' translated text ','02188886666','Shanghai','Shanghai','Xuhui',' translated text  88  translated text  6  translated text ','200030',0);
INSERT INTO shipments (shipment_id,user_id,tracking_no,carrier,service_level,status,sender_json,recipient_json,weight_kg,dimensions_json,declared_value_minor,fee_minor,created_at,eta_date,scheduled_pickup_at,updated_at,cancel_reason) VALUES
('shp_awch_0001','usr_mo_fan','SF8259520001CN',' translated text ','express','delivered','{"recipient":"Apple  translated text ","city":"Suzhou","district":"Industrial Park"}','{"recipient":" translated text ","city":"Shanghai","district":"Pudong"}',1.0,'{"length_cm":30,"width_cm":22,"height_cm":6}',380000,0,'2026-06-13T09:00:00+08:00','2026-06-15',NULL,'2026-06-15T16:40:00+08:00',NULL),
('shp_awch_0002','usr_mo_fan','YTOAWCH5520002CN',' translated text ','standard','in_transit','{"recipient":" translated text ","city":"Shanghai","district":"Pudong"}','{"recipient":"Apple  translated text ","city":"Suzhou","district":"Industrial Park"}',0.8,'{"length_cm":20,"width_cm":15,"height_cm":8}',380000,800,'2026-06-15T08:30:00+08:00','2026-06-17','2026-06-15T08:30:00+08:00','2026-06-15T20:10:00+08:00',NULL),
('ship-JDVA55268831','usr_mo_fan','JDVA55268831',' translated text ','same_day','delivered','{"recipient":" translated text "}','{"recipient":" translated text ","district":"Pudong"}',0.6,'{"length_cm":28,"width_cm":20,"height_cm":12}',29900,0,'2026-05-20T08:00:00+08:00','2026-05-20',NULL,'2026-05-20T18:12:00+08:00',NULL),
('ship-ZTO6821457712','usr_mo_fan','ZTO6821457712',' translated text ','standard','delivered','{"recipient":" translated text "}','{"recipient":" translated text ","district":"Pudong"}',0.9,'{"length_cm":35,"width_cm":25,"height_cm":8}',48900,600,'2026-05-27T10:00:00+08:00','2026-05-30',NULL,'2026-05-29T14:30:00+08:00',NULL),
('ship-SFRA82590031','usr_mo_fan','SFRA82590031',' translated text ','express','returned','{"recipient":" translated text ","district":"Pudong"}','{"recipient":" translated text table translated text ","district":" translated text "}',0.3,'{"length_cm":18,"width_cm":12,"height_cm":8}',90000,1800,'2026-04-18T11:00:00+08:00','2026-04-19','2026-04-18T10:30:00+08:00','2026-04-20T09:20:00+08:00',' translated text item translated text '),
('ship-EMS552093957CN','usr_mo_fan','EMS552093957CN',' translated text EMS','standard','cancelled','{"recipient":" translated text ","district":"Pudong"}','{"recipient":" translated text ","city":" translated text "}',1.4,'{"length_cm":38,"width_cm":28,"height_cm":16}',28000,1600,'2026-05-06T09:00:00+08:00','2026-05-09','2026-05-06T14:00:00+08:00','2026-05-06T10:10:00+08:00','shipment translated text '),
('ship-ZTOAWCH39174620CN','usr_mo_fan','ZTOAWCH39174620CN',' translated text ','standard','delivered','{"recipient":" translated text ","district":" translated text "}','{"recipient":" translated text ","district":"Pudong"}',0.5,'{"length_cm":24,"width_cm":18,"height_cm":8}',42800,600,'2026-05-14T10:20:00+08:00','2026-05-17',NULL,'2026-05-16T16:32:00+08:00',NULL),
('ship-SFAWCH71820455CN','usr_mo_fan','SFAWCH71820455CN',' translated text ','express','returned','{"recipient":" translated text ","district":"Pudong"}','{"recipient":" translated text item translated text ","district":" translated text "}',0.7,'{"length_cm":26,"width_cm":19,"height_cm":10}',65900,1500,'2026-06-01T08:50:00+08:00','2026-06-02','2026-06-01T08:30:00+08:00','2026-06-02T18:25:00+08:00',' translated text ');
INSERT INTO shipment_events (event_id,shipment_id,at,location,status_code,description) VALUES
('SF8259520001CN-0613T0910-K7QA','shp_awch_0001','2026-06-13T09:10:00+08:00',' translated text Industrial Park','picked_up',' translated text Home translated text '),
('SF8259520001CN-0614T0320-S4XM','shp_awch_0001','2026-06-14T03:20:00+08:00',' translated text ','in_transit',' translated text '),
('SF8259520001CN-0615T1640-W9KD','shp_awch_0001','2026-06-15T16:40:00+08:00','ShanghaiPudong','delivered',' translated text delivery receipt'),
('YTOAWCH5520002CN-0615T0845-C5LW','shp_awch_0002','2026-06-15T08:45:00+08:00','ShanghaiPudong','picked_up',' translated text old device translated text '),
('YTOAWCH5520002CN-0615T2010-P7FC','shp_awch_0002','2026-06-15T20:10:00+08:00',' translated text ','in_transit',' translated text official recycling translated text '),
('JDVA55268831-0520T0900-J4PR','ship-JDVA55268831','2026-05-20T09:00:00+08:00',' translated text ','out_for_delivery',' translated text '),
('JDVA55268831-0520T1812-D9VT','ship-JDVA55268831','2026-05-20T18:12:00+08:00','ShanghaiPudong','delivered',' translated text delivery receipt'),
('ZTO6821457712-0527T1200-N2GX','ship-ZTO6821457712','2026-05-27T12:00:00+08:00','SuzhouIndustrial Park','picked_up',' translated text Home translated text '),
('ZTO6821457712-0529T1430-R6NB','ship-ZTO6821457712','2026-05-29T14:30:00+08:00','ShanghaiPudong','delivered',' translated text delivery receipt'),
('SFRA82590031-0418T1110-B8SY','ship-SFRA82590031','2026-04-18T11:10:00+08:00','ShanghaiPudong','picked_up',' translated text item'),
('SFRA82590031-0419T1500-G5UE','ship-SFRA82590031','2026-04-19T15:00:00+08:00','Shanghai translated text ','delivery_failed',' translated text '),
('SFRA82590031-0420T0920-L3HZ','ship-SFRA82590031','2026-04-20T09:20:00+08:00','ShanghaiPudong','returned',' translated text item translated text '),
('EMS552093957CN-0506T0920-Q7BJ','ship-EMS552093957CN','2026-05-06T09:20:00+08:00','ShanghaiPudong','pickup_scheduled',' translated text item'),
('EMS552093957CN-0506T1010-E4CW','ship-EMS552093957CN','2026-05-06T10:10:00+08:00','ShanghaiPudong','cancelled','shipment translated text '),
('YTOAWCH5520002CN-0615T2100-V9ZK','shp_awch_0002','2026-06-15T21:00:00+08:00',' translated text ','eta_updated',' translated text  6  translated text  17  translated text official recycling translated text '),
('ZTOAWCH39174620CN-0514T1205-Y5MR','ship-ZTOAWCH39174620CN','2026-05-14T12:05:00+08:00',' translated text ','picked_up',' translated text '),
('ZTOAWCH39174620CN-0516T1632-H2KL','ship-ZTOAWCH39174620CN','2026-05-16T16:32:00+08:00','ShanghaiPudong','delivered',' translated text delivery receipt'),
('SFAWCH71820455CN-0601T0842-X8PV','ship-SFAWCH71820455CN','2026-06-01T08:42:00+08:00','ShanghaiPudong','picked_up',' translated text '),
('SFAWCH71820455CN-0602T1825-M6DT','ship-SFAWCH71820455CN','2026-06-02T18:25:00+08:00','ShanghaiPudong','returned',' translated text shipment translated text delivery receipt');
INSERT INTO pickups (pickup_id,shipment_id,scheduled_at,completed_at,status) VALUES
('pk_awch_1','ship-SFRA82590031','2026-04-18T10:30:00+08:00','2026-04-18T11:10:00+08:00','completed'),
('pk_awch_2','ship-EMS552093957CN','2026-05-06T14:00:00+08:00',NULL,'cancelled'),
('pk_awch_3','ship-SFAWCH71820455CN','2026-06-01T08:30:00+08:00','2026-06-01T08:42:00+08:00','completed');
INSERT INTO issue_tickets (ticket_id,shipment_id,issue_type,description,status,opened_at,expected_response_date,resolved_at) VALUES
('case-SFRA82590031-MV8D','ship-SFRA82590031','wrong_address',' translated text ，request translated text ','resolved','2026-04-19T15:10:00+08:00','2026-04-20','2026-04-20T09:20:00+08:00'),
('case-ZTO6821457712-SMS6','ship-ZTO6821457712','delivery_failed',' translated text ， translated text ','resolved','2026-05-29T16:00:00+08:00','2026-05-30','2026-05-29T18:00:00+08:00'),
('case-SFAWCH71820455-DMG3','ship-SFAWCH71820455CN','damaged',' translated text ， translated text ','closed','2026-06-02T09:15:00+08:00','2026-06-03','2026-06-02T18:25:00+08:00');
INSERT INTO status_subscriptions (subscription_id,shipment_id,channel,target,active,created_at) VALUES
('sublog_awch_1','shp_awch_0002','email','mo.fan.tradein@gmail.com',1,'2026-06-15T09:00:00+08:00'),
('sublog_awch_2','shp_awch_0001','sms','13900000000',0,'2026-06-13T09:00:00+08:00');
INSERT INTO notifications_outbox (subscription_id,payload_json,queued_at,sent_at) VALUES
('sublog_awch_1','{"tracking_no":"YTOAWCH5520002CN","status":"in_transit"}','2026-06-15T20:11:00+08:00','2026-06-15T20:12:00+08:00'),
('sublog_awch_2','{"tracking_no":"SF8259520001CN","status":"delivered"}','2026-06-15T16:41:00+08:00','2026-06-15T16:42:00+08:00');
INSERT INTO _counters (key,value) VALUES ('shipment_seq',8),('event_seq',19),('pickup_seq',3),('ticket_seq',3),('subscription_seq',2),('outbox_seq',2),('address_seq',3);
COMMIT;
