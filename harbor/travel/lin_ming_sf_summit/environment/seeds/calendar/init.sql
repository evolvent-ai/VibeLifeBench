BEGIN TRANSACTION;
INSERT INTO calendars VALUES ('CAL001', 'liming@company.com', 'Work', 'blue', 'Asia/Shanghai', 1, '2025-01-06T09:00:00+08:00');
INSERT INTO events VALUES ('EV001', 'CAL001', '2026 Global Tech Summit', 'Industry summit, must attend in person; transport and lodging are not yet arranged.', 'Moscone Center, San Francisco', '2026-03-28T09:00:00-07:00', '2026-03-30T18:00:00-07:00', 0, 'confirmed', '2026-03-10T10:00:00+08:00', '2026-03-14T18:00:00+08:00', NULL, NULL);
INSERT INTO events VALUES
('EVH01', 'CAL001', '2025 Global Tech Forum recap', 'Historical internal debrief for last year''s online forum; no travel or booking action is associated with this record.', 'Conference Room C', '2025-11-21T15:00:00+08:00', '2025-11-21T16:00:00+08:00', 0, 'confirmed', '2025-11-10T09:00:00+08:00', '2025-11-21T16:05:00+08:00', NULL, NULL),
('EVH02', 'CAL001', 'Q1 expense-policy Q&A', 'Finance office hour covering receipt retention and manager approval evidence for ordinary domestic and international travel.', 'Online', '2026-03-12T16:00:00+08:00', '2026-03-12T16:45:00+08:00', 0, 'confirmed', '2026-03-01T10:00:00+08:00', '2026-03-12T17:00:00+08:00', NULL, NULL),
('EVH03', 'CAL001', 'Manager weekly one-on-one', 'Routine pipeline and staffing review; move only with Zhang manager''s agreement.', 'Meeting Room 5', '2026-03-20T10:00:00+08:00', '2026-03-20T10:30:00+08:00', 0, 'confirmed', '2026-03-02T10:00:00+08:00', '2026-03-13T09:10:00+08:00', NULL, NULL),
('EVH04', 'CAL001', 'Family dinner', 'Personal commitment before the overseas work trip.', 'Beijing', '2026-03-25T18:30:00+08:00', '2026-03-25T20:00:00+08:00', 0, 'confirmed', '2026-03-08T20:00:00+08:00', '2026-03-08T20:00:00+08:00', NULL, NULL),
('EVH05', 'CAL001', 'Quarterly product all-hands', 'Ordinary company update; recording will be available if travel preparation conflicts.', 'Auditorium', '2026-03-27T15:00:00+08:00', '2026-03-27T16:30:00+08:00', 0, 'confirmed', '2026-03-05T11:00:00+08:00', '2026-03-13T13:00:00+08:00', NULL, NULL),
('EVH06', 'CAL001', 'Post-travel inbox catch-up', 'Protected time for routine follow-up after returning to Beijing; not a transport segment or supplier appointment.', 'Office', '2026-04-02T09:30:00+08:00', '2026-04-02T11:00:00+08:00', 0, 'tentative', '2026-03-10T17:00:00+08:00', '2026-03-14T08:30:00+08:00', NULL, NULL);
INSERT INTO attendees VALUES (1, 'EV001', 'liming@company.com', 'Ming Lin', 'accepted');
INSERT INTO _counters VALUES ('calendar', 1), ('event', 7), ('attendee', 1), ('reminder', 0);
COMMIT;
