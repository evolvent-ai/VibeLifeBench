-- Stage 18 mutation: check-in opens for the outbound sectors. Gates and
-- terminals are assigned for the first time, so get_flight_status now returns
-- something an agent can actually check a connection against. Before this the
-- rows carried NULL gate and terminal.

UPDATE flight_status
   SET status = 'scheduled', gate = 'D62', terminal = 'T2', delay_min = 0,
       last_updated = '2026-08-12T02:00:00Z'
 WHERE flight_no = 'CX368' AND date = '2026-08-14';

UPDATE flight_status
   SET status = 'scheduled', gate = '23', terminal = 'T1', delay_min = 0,
       last_updated = '2026-08-12T02:00:00Z'
 WHERE flight_no = 'CX315' AND date = '2026-08-15';

UPDATE flight_status
   SET status = 'scheduled', gate = 'H8', terminal = 'T4S', delay_min = 0,
       last_updated = '2026-08-12T02:00:00Z'
 WHERE flight_no = 'IB6453' AND date = '2026-08-15';

UPDATE flight_status
   SET status = 'scheduled', gate = '4', terminal = 'DOM', delay_min = 0,
       last_updated = '2026-08-12T02:00:00Z'
 WHERE flight_no = 'AV1632' AND date = '2026-08-16';

-- The Quito-routed alternatives are still carrying their delay history, so a
-- late switch is visibly worse than the route already held.
UPDATE flight_status
   SET last_updated = '2026-08-12T02:00:00Z'
 WHERE flight_no IN ('KL755','AV1688');
