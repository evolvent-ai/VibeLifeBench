UPDATE transit_events SET active=1,start_dt='2026-08-06T08:30:00+08:00',end_dt='2026-08-09T23:59:00+08:00',note='云栖苑东门步行段在看房周末临时绕行' WHERE event_id='evt_c_road_alert';
UPDATE road_events SET active=1,start_dt='2026-08-06T08:30:00+08:00',end_dt='2026-08-09T23:59:00+08:00',note='东门绕行增加步行距离，搬家车辆限时进入' WHERE event_id='rd_evt_c_patrol';
