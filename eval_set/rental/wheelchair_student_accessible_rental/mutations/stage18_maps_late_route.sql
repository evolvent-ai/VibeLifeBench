UPDATE transit_events SET active=1,start_dt='2026-08-01T08:30:00+08:00',end_dt='2026-08-09T23:59:00+08:00',note='云栖苑东门无障碍通道在陪看周末前临时调整' WHERE event_id='evt_c_road_alert';
UPDATE road_events SET active=1,start_dt='2026-08-01T08:30:00+08:00',end_dt='2026-08-09T23:59:00+08:00',note='东门绕行增加坡道距离，施工围挡压缩通行宽度' WHERE event_id='rd_evt_c_patrol';
