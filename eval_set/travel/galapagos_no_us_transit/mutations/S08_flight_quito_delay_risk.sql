-- Mutation SQL
UPDATE flight_status SET status='delayed', delay_min=95, last_updated='2026-08-01T11:00:00Z' WHERE flight_no IN ('KL755','AV1688');
