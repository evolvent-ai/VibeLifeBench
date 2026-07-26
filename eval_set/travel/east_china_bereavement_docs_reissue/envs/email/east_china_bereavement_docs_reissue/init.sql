-- Reviewed Stage 0 mailbox: only historical messages; story emails enter via event mutations.
INSERT INTO account_config(id,email,name,created_at) VALUES (1,'lin.che@example.test','林澈','2024-01-01T00:00:00+08:00');
INSERT INTO folders(id,name,delimiter,flags_json,message_count,unread_count) VALUES
 (1,'INBOX','/','[]',60,8),(2,'Sent','/','[]',0,0),(3,'Archive','/','[]',0,0),(4,'Trip Archive','/','[]',0,0);

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<60)
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,in_reply_to,references_header,headers_json,uid,size,created_at)
SELECT 1,printf('msg_archive_%03d',n),
       CASE n%12 WHEN 0 THEN '物业季度检修安排' WHEN 1 THEN '部门会议纪要' WHEN 2 THEN '家庭体检预约确认' WHEN 3 THEN '铁路会员积分提醒' WHEN 4 THEN '社区活动报名回执' WHEN 5 THEN '图书馆借阅到期' WHEN 6 THEN '水电账单通知' WHEN 7 THEN '保险保单年度摘要' WHEN 8 THEN '同学聚会时间征询' WHEN 9 THEN '快递柜取件提示' WHEN 10 THEN '课程资料更新' ELSE '银行月度对账单' END,
       printf('sender%02d@records.example.test',n),
       '["lin.che@example.test"]','[]','[]',
       strftime('%Y-%m-%dT%H:%M:00+08:00','2026-01-20 08:00:00','+'||(n-1)||' days','+'||(n%9)||' hours'),
       CASE n%12 WHEN 0 THEN '物业将分楼栋检查消防和供水设施，请留意公告中的入户时段。' WHEN 1 THEN '会议纪要已归档，包含负责人、完成日期和需要复核的交付项。' WHEN 2 THEN '常规体检预约已确认，现场需要携带本人有效证件和既往报告。' WHEN 3 THEN '本月铁路会员积分即将更新，可在官方账户查看明细和有效期。' WHEN 4 THEN '社区活动报名成功，签到地点与志愿分工会在开始前再次通知。' WHEN 5 THEN '借阅图书临近到期，可线上续借或在开放时间归还到服务台。' WHEN 6 THEN '本期水电账单已经生成，请核对户号、周期与已扣金额。' WHEN 7 THEN '年度保单摘要可供下载，保障责任和紧急联系电话均未变更。' WHEN 8 THEN '老同学正在收集周末聚会时间，暂未要求立即回复或付款。' WHEN 9 THEN '包裹已放入小区快递柜，取件码仅用于本次领取。' WHEN 10 THEN '线上课程新增阅读资料和练习题，下一节课前完成即可。' ELSE '月度账户对账单已生成，请通过银行应用核对收支与余额。' END
       || CASE n%5 WHEN 0 THEN ' 本邮件无需转发个人证件。' WHEN 1 THEN ' 如有疑问请从官方入口核验。' WHEN 2 THEN ' 当前没有不可逆操作。' WHEN 3 THEN ' 相关记录可在原系统中查看。' ELSE ' 请按自己的时间安排处理。' END,
       NULL,CASE WHEN n%7=0 THEN 0 ELSE 1 END,CASE WHEN n%17=0 THEN 1 ELSE 0 END,0,NULL,NULL,'{"source":"historical_mail"}',1000+n,220+n,
       strftime('%Y-%m-%dT%H:%M:00+08:00','2026-01-20 08:00:00','+'||(n-1)||' days','+'||(n%9)||' hours')
FROM seq;
