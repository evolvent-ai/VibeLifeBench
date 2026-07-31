-- Stage 1 mutation: the organiser publishes the final session grid to the
-- shared programme calendar, and it syncs into Lin Qiao's diary.
--
-- The seed already holds the four session days she typed in herself back in
-- June from the invitation. What did NOT exist until now is the venue desk's
-- own opening hours entry -- the coordinator only confirmed on 6 July that the
-- cut-off was "an evening one" and said the exact time was still being decided
-- (email 6). This mutation is where the desk hours become a real, queryable
-- calendar object.

INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('ev_venue_desk_0817','cal_linqiao_primary','Venue desk open (badge collection)',
   'Published by the Galapagos Data Field Office. The desk is staffed from 10:00 and shuts at 18:00; the badge printer goes back to the mainland overnight and there is no desk on the opening morning.',
   'Puerto Ayora Marine Data Lab, Avenida Charles Darwin 102',
   '2026-08-17T10:00:00-06:00','2026-08-17T18:00:00-06:00',0,'confirmed',
   '2026-07-25T10:00:00-06:00','2026-07-25T10:00:00-06:00',NULL,NULL),
  ('ev_welcome_drinks_0817','cal_linqiao_primary','Welcome drinks (optional)',
   'After the desk closes. Guests welcome.','Puerto Ayora',
   '2026-08-17T19:30:00-06:00','2026-08-17T21:30:00-06:00',0,'tentative',
   '2026-07-25T10:00:00-06:00','2026-07-25T10:00:00-06:00',NULL,NULL),
  ('ev_coordinator_travel_0810','cal_linqiao_primary','Coordinator flies out with the badges',
   'Marisol travels to the island on 10 August. Nothing printed on the mainland can be changed after she leaves.',
   'Mainland Ecuador',
   '2026-08-10T00:00:00-06:00','2026-08-11T00:00:00-06:00',1,'confirmed',
   '2026-07-25T10:00:00-06:00','2026-07-25T10:00:00-06:00',NULL,NULL);

-- The day-two session gains its dependency note now the grid is final.
UPDATE events
   SET description = 'Outdoor session, walked from the beach. Runs only if the port captain has no marine warning in force; otherwise it is replaced by a shore-based alternative.',
       updated_at  = '2026-07-25T10:00:00-06:00'
 WHERE event_id = 'ev_workshop_day2_0819';

INSERT INTO attendees (event_id, email, name, response_status) VALUES
  ('ev_venue_desk_0817','ops@galapagos-data.example','Galapagos Data Field Office','accepted'),
  ('ev_welcome_drinks_0817','linqiao@example.com','Lin Qiao','needsAction');
