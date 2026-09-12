PRAGMA foreign_keys = ON;
INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES ('cal_lin_personal', 'usr_lin_che', 'Claire Lin personal job search', '#2E7D32', 'Asia/Shanghai', 1, '2026-07-01T08:00:00+08:00');
INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES ('cal_lin_work', 'usr_lin_che', 'current work calendar', '#1565C0', 'Asia/Shanghai', 0, '2026-07-01T08:00:00+08:00');
INSERT INTO _counters (key, value) VALUES ('event_seq', 0);
INSERT INTO _counters (key, value) VALUES ('attendee_seq', 0);
INSERT INTO _counters (key, value) VALUES ('reminder_seq', 0);
