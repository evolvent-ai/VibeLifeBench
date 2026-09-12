UPDATE shipments
SET status='exception', updated_at='2026-07-20T06:40:00+08:00'
WHERE shipment_id='shp_f4d8be2ca9' AND tracking_no='DL-AXG-0720';
INSERT OR IGNORE INTO shipment_events (event_id,shipment_id,at,location,status_code,description)
VALUES ('evt_drink_exception_7bca','shp_f4d8be2ca9','2026-07-20T06:40:00+08:00','evidence record','exception','evidence record：evidence record，evidence record；evidence record、evidence record。');
