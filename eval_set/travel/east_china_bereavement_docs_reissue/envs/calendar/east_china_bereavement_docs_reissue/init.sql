-- Reviewed Stage 0 calendar: one calendar, 27 distinct historical events and 27 reminders.
INSERT INTO calendars(calendar_id,user_id,name,color,timezone,is_primary,created_at)
VALUES ('cal_lin_primary','user_lin_che','林澈主日历','#3366cc','Asia/Shanghai',1,'2024-01-01T00:00:00+08:00');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<27)
INSERT INTO events(event_id,calendar_id,summary,description,location,start_dt,end_dt,all_day,status,created_at,updated_at,recurrence_rule,parent_event_id)
SELECT printf('cal_history_%03d',n),'cal_lin_primary',
       CASE n%9 WHEN 0 THEN '部门周会' WHEN 1 THEN '母亲复诊陪同' WHEN 2 THEN '项目评审' WHEN 3 THEN '家庭采购' WHEN 4 THEN '客户资料交接' WHEN 5 THEN '社区志愿值班' WHEN 6 THEN '远程课程' WHEN 7 THEN '车辆保养' ELSE '季度财务整理' END,
       CASE n%9 WHEN 0 THEN '整理本周进展并记录需要同事接手的事项。' WHEN 1 THEN '陪同长辈完成常规复诊，预留挂号和取药时间。' WHEN 2 THEN '核对方案版本、风险清单和下一轮修改责任人。' WHEN 3 THEN '采购家庭日用品并顺路办理生活缴费。' WHEN 4 THEN '完成纸质材料清点，确认仅交付必要文件。' WHEN 5 THEN '参与社区服务台轮值，结束后归还门禁卡。' WHEN 6 THEN '参加线上课程，提前测试耳机和网络连接。' WHEN 7 THEN '按预约进行车辆常规检查并记录取车时间。' ELSE '核对银行卡、发票和家庭预算分类。' END,
       CASE n%6 WHEN 0 THEN '北京朝阳' WHEN 1 THEN '北京海淀' WHEN 2 THEN '线上会议' WHEN 3 THEN '社区服务站' WHEN 4 THEN '北京东城' ELSE '家中' END,
       strftime('%Y-%m-%dT%H:00:00+08:00','2026-02-01 07:00:00','+'||(n-1)||' days','+'||(n%10)||' hours'),
       strftime('%Y-%m-%dT%H:00:00+08:00','2026-02-01 08:00:00','+'||(n-1)||' days','+'||(n%10)||' hours'),
       0,'confirmed','2026-01-20T09:00:00+08:00','2026-01-20T09:00:00+08:00',NULL,NULL
FROM seq;

INSERT INTO reminders(event_id,method,minutes_before)
SELECT event_id,CASE CAST(substr(event_id,-1) AS INTEGER)%2 WHEN 0 THEN 'popup' ELSE 'email' END,
       CASE CAST(substr(event_id,-1) AS INTEGER)%3 WHEN 0 THEN 15 WHEN 1 THEN 30 ELSE 60 END
FROM events;
