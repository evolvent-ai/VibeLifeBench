-- Stage 20 mutation: mid-journey. The Shanghai departure delay from stage 19
-- has worked through: the first sector left late but the Madrid connection was
-- held, so the itinerary is intact with a compressed margin at Guayaquil.

UPDATE flight_status
   SET status = 'departed', actual_depart = '2026-08-14T18:50:00+08:00',
       delay_min = 70, last_updated = '2026-08-16T13:20:00Z'
 WHERE flight_no = 'CX368' AND date = '2026-08-14';

UPDATE flight_status
   SET status = 'arrived', actual_depart = '2026-08-15T01:35:00+08:00',
       actual_arrive = '2026-08-15T08:40:00+02:00', delay_min = 35,
       last_updated = '2026-08-16T13:20:00Z'
 WHERE flight_no = 'CX315' AND date = '2026-08-15';

UPDATE flight_status
   SET status = 'arrived', actual_depart = '2026-08-15T12:05:00+02:00',
       actual_arrive = '2026-08-15T17:10:00-05:00', delay_min = 15,
       last_updated = '2026-08-16T13:20:00Z'
 WHERE flight_no = 'IB6453' AND date = '2026-08-15';

-- The island sector is running, but the airport is working through a backlog
-- and the arrivals hall is slower than published.
UPDATE flight_status
   SET status = 'delayed', delay_min = 40, gate = '4', terminal = 'DOM',
       last_updated = '2026-08-16T13:20:00Z'
 WHERE flight_no = 'AV1632' AND date = '2026-08-16';
