-- Stage 22 mutation: the sea-state watch that has been running since stage 13
-- is upgraded to a port captain's warning, which is what actually stops boat
-- movements. The distinction matters: a watch is advisory, a warning suspends
-- operations, and only the second one forces the workshop to move the session.

INSERT INTO alerts (alert_id,kind,severity,start_dt,end_dt,areas_json,description,active,created_at,source_event) VALUES
  ('alert_galapagos_marine_warning_0820','marine','warning','2026-08-20T06:00:00-06:00','2026-08-22T18:00:00-06:00','["gps","puerto_ayora","baltra_channel","tortuga_bay"]',
   'Port captain warning in force: small craft movements between Santa Cruz and the outer islands suspended. Itabaca Channel barge continues on a reduced timetable at operator discretion.',1,
   '2026-08-20T06:00:00-06:00','S22_mutation_marine_warning_upgrade');

-- The earlier moderate watch is superseded rather than left to contradict it.
UPDATE alerts
   SET active = 0,
       end_dt = '2026-08-20T06:00:00-06:00',
       description = 'Moderate sea state; superseded by the port captain warning of 20 August.'
 WHERE alert_id = 'alert_galapagos_sea_moderate';

-- Land is unaffected: the shore alternative is genuinely available, so this is
-- a rerouting decision and not a dead end.
UPDATE daily_weather
   SET condition = 'sunny', precip_mm = 0.0, precip_prob = 0.05, wind_kmh = 31.0, tmax = 28.5
 WHERE geo_key = 'gps' AND date IN ('2026-08-20','2026-08-21');
