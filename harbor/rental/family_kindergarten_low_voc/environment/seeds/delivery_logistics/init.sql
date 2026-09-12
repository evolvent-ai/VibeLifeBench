PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM "notifications_outbox";
DELETE FROM "status_subscriptions";
DELETE FROM "shipment_events";
DELETE FROM "pickups";
DELETE FROM "issue_tickets";
DELETE FROM "shipments";
DELETE FROM "address_book";
INSERT INTO "address_book" ("address_id","user_id","label","recipient","phone","province","city","district","detail","postal_code","is_default") VALUES ('addr_old','usr_family_038','old residence','Lin Lan','13800000000','Zhejiang','Hangzhou','Binjiang District','old residential community','310000',1);
INSERT INTO "address_book" ("address_id","user_id","label","recipient","phone","province","city","district","detail","postal_code","is_default") VALUES ('addr_new_candidate','usr_family_038','candidate new residence','Lin Lan','13800000000','Zhejiang','Hangzhou','Binjiang District','pending new residence','310000',0);
COMMIT;
PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
INSERT INTO address_book(address_id,user_id,label,recipient,phone,province,city,district,detail,postal_code,is_default) VALUES
('addr_family_library','usr_family_038','Library book return point','Binjiang District Library','057186521018','Zhejiang','Hangzhou','Binjiang District','Self-service book return slot, 200 Tai''an Road','310051',0),
('addr_family_clinic','usr_family_038','Pediatric healthcare clinic','Binjiang Maternal and Child Health Pediatric Clinic','057186620120','Zhejiang','Hangzhou','Binjiang District','East side of the second floor, 1511 Jianghong Road','310052',0),
('addr_family_workdesk','usr_family_038','Company front desk','Lin Lan','13800000000','Zhejiang','Hangzhou','Shangcheng District','Front desk of the Qianjiang New City office building','310016',0),
('addr_family_grandma_home','usr_family_038','Grandmother''s home','Zhou Minhua','13700000018','Zhejiang','Shaoxing','Yuecheng District','Old residence on Fushan Subdistrict','312000',0),
('addr_family_daycare_gate','usr_family_038','Former daycare gatehouse','Orange Class teacher','13600000027','Zhejiang','Hangzhou','Binjiang District','Gatehouse of the former daycare on Chunxiao Road','310052',0),
('addr_family_bike_shop','usr_family_038','Bicycle shop','Changhe Cycling Workshop','057186410209','Zhejiang','Hangzhou','Binjiang District','519 Changhe Road','310053',0),
('addr_family_photo_studio','usr_family_038','Photo studio','Binjiang Photo Studio','057186743155','Zhejiang','Hangzhou','Binjiang District','118 Tai''an Road','310051',0),
('addr_family_old_west','usr_family_038','West gate of old residence','Lin Lan','13800000000','Zhejiang','Hangzhou','Binjiang District','Security office at the west gate of the old residential compound','310000',0);
INSERT INTO shipments(shipment_id,user_id,tracking_no,carrier,service_level,status,sender_json,recipient_json,weight_kg,dimensions_json,declared_value_minor,fee_minor,created_at,eta_date,scheduled_pickup_at,updated_at,cancel_reason) VALUES
('ship_family_vaccine_book','usr_family_038','SF-FAM-JAN09','SF Express','standard','delivered','{"city":"Hangzhou","district":"Binjiang District","detail":"Pediatric healthcare clinic"}','{"city":"Hangzhou","district":"Binjiang District","detail":"old residence"}',0.4,'{"cm":[28,20,4]}',10000,1200,'2026-01-09T11:50:00+08:00','2026-01-10',NULL,'2026-01-10T15:12:00+08:00',NULL),
('ship_family_library_books','usr_family_038','YD-FAM-JAN22','Yunda','economy','delivered','{"city":"Hangzhou","district":"Binjiang District","detail":"Library"}','{"city":"Hangzhou","district":"Binjiang District","detail":"old residence"}',3.2,'{"cm":[36,28,20]}',28000,800,'2026-01-22T09:14:00+08:00','2026-01-24',NULL,'2026-01-24T18:25:00+08:00',NULL),
('ship_family_raincoat','usr_family_038','ZT-FAM-FEB19','ZTO Express','standard','returned','{"city":"Suzhou","district":"Wuzhong District"}','{"city":"Hangzhou","district":"Binjiang District","detail":"old residence"}',0.7,'{"cm":[30,24,8]}',12900,0,'2026-02-19T12:03:00+08:00','2026-02-22',NULL,'2026-02-27T10:40:00+08:00','Size runs small'),
('ship_family_router_adapter','usr_family_038','JD-FAM-MAR02','JD Logistics','next_day','delivered','{"city":"Hangzhou","district":"Yuhang District"}','{"city":"Hangzhou","district":"Binjiang District","detail":"old residence"}',0.5,'{"cm":[22,16,10]}',7900,0,'2026-03-02T08:35:00+08:00','2026-03-03',NULL,'2026-03-03T10:18:00+08:00',NULL),
('ship_family_dental_prints','usr_family_038','EMS-FAM-APR12','China Post','standard','delivered','{"city":"Hangzhou","district":"Binjiang District","detail":"Dental clinic"}','{"city":"Hangzhou","district":"Binjiang District","detail":"old residence"}',0.2,'{"cm":[32,23,2]}',5000,900,'2026-04-12T08:22:00+08:00','2026-04-14',NULL,'2026-04-14T16:35:00+08:00',NULL),
('ship_family_swim_gear','usr_family_038','YT-FAM-MAY12','YTO Express','standard','delivered','{"city":"Ningbo","district":"Yinzhou District"}','{"city":"Hangzhou","district":"Binjiang District","detail":"old residence"}',1.1,'{"cm":[34,25,18]}',24600,600,'2026-05-12T14:10:00+08:00','2026-05-15',NULL,'2026-05-15T13:56:00+08:00',NULL),
('ship_family_grandma_parcel','usr_family_038','SF-FAM-MAY19','SF Express','standard','delivered','{"city":"Shaoxing","district":"Yuecheng District"}','{"city":"Hangzhou","district":"Binjiang District","detail":"old residence"}',4.8,'{"cm":[45,35,28]}',36000,1800,'2026-05-19T10:45:00+08:00','2026-05-20',NULL,'2026-05-20T17:18:00+08:00',NULL),
('ship_family_washer_part','usr_family_038','DB-FAM-MAY28','Deppon','standard','delivered','{"city":"Jiaxing","district":"Nanhu District"}','{"city":"Hangzhou","district":"Binjiang District","detail":"old residence"}',2.3,'{"cm":[38,30,25]}',46000,1500,'2026-05-28T08:50:00+08:00','2026-05-29',NULL,'2026-05-29T11:42:00+08:00',NULL),
('ship_family_photo_prints','usr_family_038','SF-FAM-JUN14','SF Express','same_day','delivered','{"city":"Hangzhou","district":"Binjiang District","detail":"Photo studio"}','{"city":"Hangzhou","district":"Binjiang District","detail":"old residence"}',0.3,'{"cm":[26,20,3]}',16800,1300,'2026-06-14T09:08:00+08:00','2026-06-14',NULL,'2026-06-14T16:20:00+08:00',NULL),
('ship_family_bike_bolt','usr_family_038','STO-FAM-JUN25','STO Express','standard','delivered','{"city":"Shanghai","district":"Jiading District"}','{"city":"Hangzhou","district":"Binjiang District","detail":"Bicycle shop"}',0.6,'{"cm":[20,14,8]}',8500,700,'2026-06-25T13:32:00+08:00','2026-06-27',NULL,'2026-06-27T10:15:00+08:00',NULL),
('ship_family_school_shoes','usr_family_038','JD-FAM-JUL14','JD Logistics','next_day','delivered','{"city":"Hangzhou","district":"Yuhang District"}','{"city":"Hangzhou","district":"Binjiang District","detail":"old residence"}',0.6,'{"cm":[31,20,12]}',8900,0,'2026-07-14T11:16:00+08:00','2026-07-15',NULL,'2026-07-15T12:16:00+08:00',NULL),
('ship_family_book_return','usr_family_038','EMS-FAM-JUL09','China Post','standard','delivered','{"city":"Hangzhou","district":"Binjiang District","detail":"old residence"}','{"city":"Hangzhou","district":"Binjiang District","detail":"Library"}',2.7,'{"cm":[35,26,18]}',24000,1000,'2026-07-09T08:05:00+08:00','2026-07-10',NULL,'2026-07-10T14:28:00+08:00',NULL);
INSERT INTO shipment_events(event_id,shipment_id,at,location,status_code,description) VALUES
('evt_vaccine_pickup','ship_family_vaccine_book','2026-01-09T12:18:00+08:00','Binjiang Maternal and Child Health','picked_up','The document pouch was handed to the courier by the clinic front desk.'),
('evt_vaccine_delivered','ship_family_vaccine_book','2026-01-10T15:12:00+08:00','East gate of old residence','delivered','Lin Lan collected the document pouch from the gatehouse.'),
('evt_books_departed','ship_family_library_books','2026-01-22T17:40:00+08:00','Binjiang distribution center','in_transit','The picture-book box was weighed and loaded onto the truck.'),
('evt_books_home','ship_family_library_books','2026-01-24T18:25:00+08:00','Express locker at old residence','delivered','The parcel was placed in compartment C12.'),
('evt_raincoat_received','ship_family_raincoat','2026-02-22T11:06:00+08:00','West gate of old residence','delivered','The yellow raincoat was tried on after being signed for.'),
('evt_raincoat_returned','ship_family_raincoat','2026-02-27T10:40:00+08:00','Suzhou returns warehouse','returned','The merchant warehouse processed the returned item into inventory.'),
('evt_router_station','ship_family_router_adapter','2026-03-02T19:25:00+08:00','Hangzhou Yuhang station','in_transit','The optical modem power accessory entered local delivery.'),
('evt_router_home','ship_family_router_adapter','2026-03-03T10:18:00+08:00','East gate of old residence','delivered','The gatehouse accepted the parcel before the engineer arrived.'),
('evt_dental_posted','ship_family_dental_prints','2026-04-12T09:35:00+08:00','Jianghong Road post office','picked_up','The clinic receipt and dental photos were sealed in a rigid paper envelope.'),
('evt_dental_home','ship_family_dental_prints','2026-04-14T16:35:00+08:00','Mailbox at old residence','delivered','The rigid paper envelope was placed in the large mailbox.'),
('evt_swim_departed','ship_family_swim_gear','2026-05-13T06:50:00+08:00','Ningbo transfer yard','in_transit','The swim goggles and cap passed security inspection.'),
('evt_swim_home','ship_family_swim_gear','2026-05-15T13:56:00+08:00','Express locker at old residence','delivered','The parcel was placed in compartment A03.'),
('evt_grandma_pickup','ship_family_grandma_parcel','2026-05-19T11:30:00+08:00','Fushan, Shaoxing','picked_up','The box of seasonal clothing was handed over by Grandmother.'),
('evt_grandma_home','ship_family_grandma_parcel','2026-05-20T17:18:00+08:00','West gate of old residence','delivered','The carton was intact and accepted by the gatehouse.'),
('evt_washer_transit','ship_family_washer_part','2026-05-28T18:20:00+08:00','Jiaxing Nanhu service point','in_transit','The drain pump part was sent to Hangzhou.'),
('evt_washer_shop','ship_family_washer_part','2026-05-29T11:42:00+08:00','Old residence repair point','delivered','The repair technician verified the part number and signed for it.'),
('evt_photo_pickup','ship_family_photo_prints','2026-06-14T09:30:00+08:00','Tai''an Road photo studio','picked_up','The document-photo paper bag was sealed.'),
('evt_photo_home','ship_family_photo_prints','2026-06-14T16:20:00+08:00','East gate of old residence','delivered','Lin Lan signed for the paper bag in person.'),
('evt_bolt_transit','ship_family_bike_bolt','2026-06-26T02:40:00+08:00','Shanghai Jiading facility','in_transit','The child seat fasteners were loaded into a small-parcel cage cart.'),
('evt_bolt_shop','ship_family_bike_bolt','2026-06-27T10:15:00+08:00','Changhe Cycling Workshop','delivered','The technician inspected and accepted the two mounting bolts.'),
('evt_shoes_station','ship_family_school_shoes','2026-07-15T06:55:00+08:00','Hangzhou Binjiang station','out_for_delivery','The indoor shoes were dispatched on the morning route.'),
('evt_shoes_locker','ship_family_school_shoes','2026-07-15T12:16:00+08:00','Express locker at old residence','delivered','The shoebox was placed in compartment B06.'),
('evt_return_books_pickup','ship_family_book_return','2026-07-09T09:02:00+08:00','East gate of old residence','picked_up','Three picture books were placed in a waterproof bag and handed over.'),
('evt_return_books_library','ship_family_book_return','2026-07-10T14:28:00+08:00','Binjiang District Library','delivered','A staff member at the self-service book return point signed for it.');
INSERT INTO status_subscriptions(subscription_id,shipment_id,channel,target,active,created_at) VALUES
('sub_ship_vaccine_email','ship_family_vaccine_book','email','lin.lan@example.invalid',0,'2026-01-09T11:55:00+08:00'),
('sub_ship_router_sms','ship_family_router_adapter','sms','13800000000',0,'2026-03-02T08:40:00+08:00'),
('sub_ship_grandma_email','ship_family_grandma_parcel','email','lin.lan@example.invalid',0,'2026-05-19T10:50:00+08:00'),
('sub_ship_washer_sms','ship_family_washer_part','sms','13800000000',0,'2026-05-28T08:55:00+08:00'),
('sub_ship_shoes_webhook','ship_family_school_shoes','webhook','family-parcel-feed',0,'2026-07-14T11:20:00+08:00'),
('sub_ship_books_email','ship_family_book_return','email','lin.lan@example.invalid',0,'2026-07-09T08:10:00+08:00');
INSERT INTO issue_tickets(ticket_id,shipment_id,issue_type,description,status,opened_at,expected_response_date,resolved_at) VALUES
('ticket_raincoat_size','ship_family_raincoat','wrong_address','The return shipping label was initially printed with the old merchant warehouse address.','closed','2026-02-23T09:10:00+08:00','2026-02-24','2026-02-23T15:42:00+08:00'),
('ticket_books_corner','ship_family_library_books','damaged','The lower-right corner of the cardboard box was damp, but the picture books were undamaged.','resolved','2026-01-24T18:40:00+08:00','2026-01-26','2026-01-25T10:15:00+08:00'),
('ticket_swim_missing_cap','ship_family_swim_gear','missing_item','One child''s swim cap was missing from the package.','closed','2026-05-15T14:20:00+08:00','2026-05-17','2026-05-16T11:35:00+08:00'),
('ticket_photo_delay','ship_family_photo_prints','delivery_failed','The handoff to the doorman was paused during the first delivery attempt.','resolved','2026-06-14T12:05:00+08:00','2026-06-15','2026-06-14T16:25:00+08:00'),
('ticket_shoes_locker','ship_family_school_shoes','wrong_address','The system SMS indicated the west gate, but the actual locker was at the east gate.','closed','2026-07-15T12:22:00+08:00','2026-07-16','2026-07-15T13:10:00+08:00');
COMMIT;
