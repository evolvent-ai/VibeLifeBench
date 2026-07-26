INSERT OR IGNORE INTO road_events(event_id,road_id,start_dt,end_dt,kind,magnitude,note,active) VALUES ('route_pottery_heping_0710','road_heping_event','2026-07-10T13:30:00+08:00','2026-07-21T18:00:00+08:00','heavy_traffic',0.65,'大理道西段临时施工，周四下午车辆通行较慢；睦南道地铁出口至一层大堂步行路线不受影响。',1);
UPDATE places SET formatted='天津市和平区睦南道88号；路线更新：大理道西段临时施工，建议地铁后步行至一层大堂集合。' WHERE place_id='place_pottery_lumen_heping';
