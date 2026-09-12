BEGIN TRANSACTION;
INSERT INTO metrics VALUES
('MET001', 'liming@company.com', 'weight', 72.5, NULL, 'kg', '2026-03-01T07:30:00+08:00'),
('MET002', 'liming@company.com', 'steps', 7820, NULL, 'count', '2026-03-03T22:00:00+08:00'),
('MET003', 'liming@company.com', 'sleep_minutes', 405, NULL, 'min', '2026-03-04T07:10:00+08:00'),
('MET004', 'liming@company.com', 'heart_rate', 72, NULL, 'bpm', '2026-03-05T08:00:00+08:00'),
('MET005', 'liming@company.com', 'body_fat', 18.6, NULL, 'percent', '2026-02-28T07:30:00+08:00');
INSERT INTO workouts VALUES
('WK001', 'liming@company.com', 'swimming', 45, 300, 1200, '2026-01-20T19:00:00+08:00'),
('WK002', 'liming@company.com', 'brisk_walk', 35, 180, 3200, '2026-02-07T08:00:00+08:00'),
('WK003', 'liming@company.com', 'mobility_yoga', 30, 120, NULL, '2026-03-05T20:00:00+08:00');
INSERT INTO goals VALUES
('GOAL_SEGMENT_ECONOMY_LIMIT', 'liming@company.com', 'max_economy_segment_hours', 10, 'hours', 'once', 'at_most', '2026-01-01', 'active'),
('GOAL_WEEKLY_STEPS', 'liming@company.com', 'steps', 50000, 'count', 'week', 'at_least', '2026-02-01', 'active'),
('GOAL_MOBILITY_WORKOUTS', 'liming@company.com', 'workouts', 3, 'sessions', 'week', 'at_least', '2026-02-01', 'active');
CREATE TABLE IF NOT EXISTS restrictions (
    restriction_id TEXT PRIMARY KEY,
    user_email TEXT NOT NULL,
    category TEXT,
    item TEXT,
    value TEXT,
    unit TEXT,
    notes TEXT,
    created_at TEXT
);
INSERT OR IGNORE INTO restrictions VALUES (
    'RES001', 'liming@company.com', 'flight', 'max_economy_segment_hours', '10', 'hours',
    'Lower back issue: avoid a single economy segment exceeding 10 hours. Prefer business class or segmented/transit flights.',
    '2026-01-01T09:00:00+08:00'
);
INSERT INTO _counters VALUES ('metric', 5), ('workout', 3), ('restriction', 1), ('nutrition', 0), ('goal', 3);
COMMIT;
