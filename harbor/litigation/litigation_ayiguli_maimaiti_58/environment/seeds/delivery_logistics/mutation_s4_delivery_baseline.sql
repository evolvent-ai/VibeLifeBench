INSERT OR IGNORE INTO shipments
  (shipment_id,user_id,tracking_no,carrier,service_level,status,sender_json,recipient_json,weight_kg,dimensions_json,declared_value_minor,fee_minor,created_at,eta_date,scheduled_pickup_at,updated_at,cancel_reason)
VALUES
  ('shp_b7ca8fd45e','user_aygul_mamt','DL-AXG-0705','evidence record','cold_chain','delivered','{"name":"evidence record","city":"evidence record"}','{"name":"evidence record","contact_role":"evidence record","district":"evidence record"}',13.0,'{}',(5580 * 100),(28 * 100 + 60),'2026-06-05T08:20:00+08:00','2026-06-05',NULL,'2026-06-05T16:20:00+08:00',NULL),
  ('shp_aecf94bd71','user_aygul_mamt','DL-AXG-0712','evidence record','next_day','delivered','{"name":"evidence record","city":"evidence record"}','{"name":"evidence record","contact_role":"evidence record","district":"evidence record"}',14.0,'{}',(9360 * 100),(37 * 100 + 40),'2026-06-12T09:10:00+08:00','2026-06-12',NULL,'2026-06-12T16:20:00+08:00',NULL),
  ('shp_f4d8be2ca9','user_aygul_mamt','DL-AXG-0720','evidence record','economy','delivered','{"name":"evidence record","city":"evidence record"}','{"name":"evidence record","contact_role":"evidence record","district":"evidence record"}',15.0,'{}',(3840 * 100),(31 * 100 + 80),'2026-06-20T08:50:00+08:00','2026-06-20',NULL,'2026-06-20T16:20:00+08:00',NULL),
  ('shp_cabef75d4a','user_aygul_mamt','DL-AXG-0728','evidence record','scheduled','delivered','{"name":"evidence record","city":"evidence record"}','{"name":"evidence record","contact_role":"evidence record","district":"evidence record"}',16.0,'{}',(4200 * 100),(29 * 100 + 20),'2026-06-28T11:20:00+08:00','2026-06-28',NULL,'2026-06-28T16:20:00+08:00',NULL);

INSERT OR IGNORE INTO shipment_events (event_id,shipment_id,at,location,status_code,description) VALUES
  ('evt_milk_created_6fca','shp_b7ca8fd45e','2026-06-05T08:20:00+08:00','evidence record','created','evidence record ML-0705 evidence record，evidence record 4.6℃'),
  ('evt_milk_delivered_baec','shp_b7ca8fd45e','2026-06-05T16:20:00+08:00','evidence record','delivered','evidence record，evidence record；evidence record'),
  ('evt_nut_created_d4af','shp_aecf94bd71','2026-06-12T09:10:00+08:00','evidence record','created','evidence record NT-0712 evidence record，evidence record'),
  ('evt_nut_delivered_ecab','shp_aecf94bd71','2026-06-12T16:20:00+08:00','evidence record','delivered','evidence record，evidence record；evidence record'),
  ('evt_drink_created_afce','shp_f4d8be2ca9','2026-06-20T08:50:00+08:00','evidence record','created','evidence record DR-0720 evidence record，evidence record'),
  ('evt_drink_delivered_cafe','shp_f4d8be2ca9','2026-06-20T16:20:00+08:00','evidence record','delivered','evidence record，evidence record'),
  ('evt_biscuit_created_bdfa','shp_cabef75d4a','2026-06-28T11:20:00+08:00','evidence record','created','evidence record SN-0728 evidence record，evidence record'),
  ('evt_biscuit_delivered_feca','shp_cabef75d4a','2026-06-28T16:20:00+08:00','evidence record','delivered','evidence record，evidence record');
