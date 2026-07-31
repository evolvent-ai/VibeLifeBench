-- Stage 21 mutation: the ground situation on arrival day. Real, current road
-- conditions the agent has to read to work out whether 18:00 is still reachable
-- from where they actually are.

INSERT INTO road_events (event_id,road_id,start_dt,end_dt,kind,magnitude,note,active) VALUES
  ('ev_itabaca_barge_queue','road_baltra_to_puerto_ayora_standard','2026-08-17T12:00:00-06:00','2026-08-17T19:00:00-06:00','heavy_traffic',0.8,
   'Barge running one vessel while the second is off for maintenance; queue at the Baltra side is about 40 minutes and lengthening.',1),
  ('ev_santa_cruz_road_works','road_baltra_to_puerto_ayora_standard','2026-08-17T13:00:00-06:00','2026-08-19T18:00:00-06:00','heavy_traffic',0.5,
   'Single-lane working with traffic control at the highlands junction; add 15 to 20 minutes southbound.',1);

-- The certified pickup situation tightens further on the day.
UPDATE road_events
   SET note = 'Certified pickup last departure from the airport is 16:40 today; operators are not waiting for delayed arrivals. Shared taxis continue from the bus terminal side.',
       magnitude = 0.85,
       end_dt = '2026-08-17T18:00:00-06:00'
 WHERE event_id = 'ev_baltra_pickup_late_change';
