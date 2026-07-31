-- Stage 7 mutation: the mainland late-arrival picture is loaded into maps.
-- Until now the only mainland road object was the Quito old-town route. This
-- adds the Guayaquil airport-to-terminal walk and the two overnight conditions
-- that make a late landing on the mainland a real decision rather than a
-- rhetorical one.

INSERT INTO roads (road_id,name,city,geom_json) VALUES
  ('road_gye_airport_terminal_walk','Guayaquil airport terminal to hotel footbridge','Guayaquil','[[-2.158,-79.884],[-2.1565,-79.8842],[-2.155,-79.884]]'),
  ('road_uio_airport_hotel_strip','Quito airport perimeter hotel strip','Quito','[[-0.129,-78.357],[-0.135,-78.362]]');

INSERT INTO road_events (event_id,road_id,start_dt,end_dt,kind,magnitude,note,active) VALUES
  ('ev_gye_footbridge_open','road_gye_airport_terminal_walk','2026-07-31T00:00:00-05:00','2026-08-31T23:59:00-05:00','heavy_traffic',0.1,
   'Covered footbridge from the terminal, lit and staffed overnight; about six minutes on foot with luggage.',1),
  ('ev_uio_night_road_caution','road_uio_airport_city_late','2026-07-31T19:00:00-05:00','2026-08-31T05:00:00-05:00','heavy_traffic',0.65,
   'Quito airport to the city is roughly 45 km; the road is unlit for long stretches and journey times after dark are unpredictable.',1),
  ('ev_uio_strip_shuttle_gap','road_uio_airport_hotel_strip','2026-07-31T23:00:00-05:00','2026-08-31T05:00:00-05:00','heavy_traffic',0.4,
   'Perimeter hotel shuttles stop running between 23:00 and 05:00; arrivals in that window need a pre-arranged pickup.',1);
