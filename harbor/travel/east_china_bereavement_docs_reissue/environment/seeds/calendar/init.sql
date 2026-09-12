-- Reviewed Stage 0 calendar: one calendar, 27 distinct historical events and 27 reminders.
INSERT INTO calendars(calendar_id,user_id,name,color,timezone,is_primary,created_at)
VALUES ('cal_lin_primary','user_lin_che','Lin Chescenario textcalendar','#3366cc','Asia/Shanghai',1,'2024-01-01T00:00:00+08:00');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<27)
INSERT INTO events(event_id,calendar_id,summary,description,location,start_dt,end_dt,all_day,status,created_at,updated_at,recurrence_rule,parent_event_id)
SELECT printf('cal_history_%03d',n),'cal_lin_primary',
       CASE n%9 WHEN 0 THEN 'scenario text' WHEN 1 THEN 'scenario text' WHEN 2 THEN 'scenario text' WHEN 3 THEN 'familyscenario text' WHEN 4 THEN 'scenario text' WHEN 5 THEN 'scenario text' WHEN 6 THEN 'scenario text' WHEN 7 THEN 'scenario text' ELSE 'scenario text' END,
       CASE n%9 WHEN 0 THEN 'scenario text。' WHEN 1 THEN 'scenario textelderscenario text，scenario texttime。' WHEN 2 THEN 'verifyscenario text、scenario text。' WHEN 3 THEN 'scenario textfamilyscenario text。' WHEN 4 THEN 'scenario textdocumentsscenario text，scenario textFile。' WHEN 5 THEN 'scenario textServicescenario text，scenario text。' WHEN 6 THEN 'scenario text，scenario text。' WHEN 7 THEN 'scenario texttime。' ELSE 'verifyscenario text、scenario textfamilyscenario text。' END,
       CASE n%6 WHEN 0 THEN 'Beijingscenario text' WHEN 1 THEN 'Beijingscenario text' WHEN 2 THEN 'scenario text' WHEN 3 THEN 'scenario textServicescenario text' WHEN 4 THEN 'BeijingDongcheng' ELSE 'scenario text' END,
       strftime('%Y-%m-%dT%H:00:00+08:00','2026-02-01 07:00:00','+'||(n-1)||' days','+'||(n%10)||' hours'),
       strftime('%Y-%m-%dT%H:00:00+08:00','2026-02-01 08:00:00','+'||(n-1)||' days','+'||(n%10)||' hours'),
       0,'confirmed','2026-01-20T09:00:00+08:00','2026-01-20T09:00:00+08:00',NULL,NULL
FROM seq;

INSERT INTO reminders(event_id,method,minutes_before)
SELECT event_id,CASE CAST(substr(event_id,-1) AS INTEGER)%2 WHEN 0 THEN 'popup' ELSE 'email' END,
       CASE CAST(substr(event_id,-1) AS INTEGER)%3 WHEN 0 THEN 15 WHEN 1 THEN 30 ELSE 60 END
FROM events;
