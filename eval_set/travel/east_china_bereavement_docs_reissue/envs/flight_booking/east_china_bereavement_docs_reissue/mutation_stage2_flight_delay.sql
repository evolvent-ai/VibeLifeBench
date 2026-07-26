UPDATE flight_status SET status='delayed', actual_depart='2026-04-03T15:30:00+08:00', actual_arrive='2026-04-03T17:40:00+08:00', delay_min=75, last_updated='2026-04-03T13:10:00+08:00' WHERE flight_no='MU5102' AND date='2026-04-03';
INSERT INTO notifications(created_at, channel, payload_json) VALUES ('2026-04-03T13:10:00+08:00','system','{"flight_no":"MU5102","status":"delayed","delay_min":75}');
