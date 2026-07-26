-- Reviewed notification history: 45 distinct account/subscription/post/message records.
INSERT INTO official_accounts(account_id,name,category,description) VALUES
 ('acct_order_watch','家庭行程订单监控','travel','汇总交通与住宿订单的状态变化。'),
 ('acct_doc_watch','证件材料提醒','documents','发布证件办理与材料保护的服务提示。'),
 ('acct_city_service','城市公共服务','government','提供道路、窗口和公共交通服务更新。'),
 ('acct_family_care','家庭照护助手','care','记录老人出行、用药和接站提醒。');
INSERT INTO official_account_subscriptions(user_id,account_id,subscribed_at) VALUES
 ('user_lin_che','acct_order_watch','2025-01-01T09:00:00+08:00'),('user_lin_che','acct_doc_watch','2025-01-02T09:00:00+08:00'),
 ('user_lin_che','acct_city_service','2025-01-03T09:00:00+08:00'),('user_lin_che','acct_family_care','2025-01-04T09:00:00+08:00');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<12)
INSERT INTO official_account_posts(post_id,account_id,title,summary,url,published_at)
SELECT printf('post_service_%02d',n),CASE n%4 WHEN 0 THEN 'acct_order_watch' WHEN 1 THEN 'acct_doc_watch' WHEN 2 THEN 'acct_city_service' ELSE 'acct_family_care' END,
       CASE n WHEN 1 THEN '铁路出发前核验清单' WHEN 2 THEN '证件材料最小发送原则' WHEN 3 THEN '政务窗口预约提示' WHEN 4 THEN '老人接站信息模板' WHEN 5 THEN '酒店取消期限记录法' WHEN 6 THEN '航班状态复查节点' WHEN 7 THEN '道路施工绕行说明' WHEN 8 THEN '敏感邮件域名核验' WHEN 9 THEN '候补与退款状态区分' WHEN 10 THEN '电子票大字版要点' WHEN 11 THEN '费用台账分类方法' ELSE '行程结束后的资料清理' END,
       CASE n WHEN 1 THEN '出发前核对车次、日期、证件和检票口。' WHEN 2 THEN '只发送当前事项必需字段，避免完整影像扩散。' WHEN 3 THEN '预约号码、地点和时间改变后同步更新提醒。' WHEN 4 THEN '接站人只需车次、到达时间、出站口和联系电话。' WHEN 5 THEN '记录取消截止时间、时区和逾期费用。' WHEN 6 THEN '延误、登机口和航站楼均以临近出发查询为准。' WHEN 7 THEN '施工影响应包含起止时间和替代步行路线。' WHEN 8 THEN '陌生地址索要证件时从官方入口独立核验。' WHEN 9 THEN '候补失败、退款申请和到账是三个不同状态。' WHEN 10 THEN '大字版应突出车次、座位、时间和联系人。' WHEN 11 THEN '交通、住宿、证件和家庭支出分别记录。' ELSE '清理临时草稿，保留必要凭证和授权记录。' END,
       printf('https://service.example.test/posts/%02d',n),strftime('%Y-%m-%dT09:00:00+08:00','2026-02-01','+'||(n-1)||' days')
FROM seq;

INSERT INTO subscriptions(subscription_id,user_id,source,type,target,condition_json,status,created_at,updated_at) VALUES
 ('sub_train_status','user_lin_che','rail_booking','policy_update','常用铁路订单','{"channel":"in_app"}','active','2025-12-01T09:00:00+08:00','2026-03-01T09:00:00+08:00'),
 ('sub_flight_status','user_lin_che','flight_booking','price_drop','国内航班关注','{"currency":"CNY"}','active','2025-12-02T09:00:00+08:00','2026-03-02T09:00:00+08:00'),
 ('sub_hotel_terms','user_lin_che','hotel_booking','policy_update','可取消住宿','{"refundable":true}','active','2025-12-03T09:00:00+08:00','2026-03-03T09:00:00+08:00'),
 ('sub_city_route','user_lin_che','maps','keyword','道路与公共交通','{"cities":["北京","上海","苏州","宁波"]}','active','2025-12-04T09:00:00+08:00','2026-03-04T09:00:00+08:00'),
 ('sub_document_rules','user_lin_che','legal_search','new_content','证件与隐私规则','{"language":"zh"}','active','2025-12-05T09:00:00+08:00','2026-03-05T09:00:00+08:00');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<20)
INSERT INTO notifications(notification_id,user_id,source,type,subscription_id,title,body,payload_json,created_at,read)
SELECT printf('notification_history_%03d',n),'user_lin_che',
       CASE n%5 WHEN 0 THEN 'rail_booking' WHEN 1 THEN 'flight_booking' WHEN 2 THEN 'hotel_booking' WHEN 3 THEN 'maps' ELSE 'legal_search' END,
       CASE n%5 WHEN 0 THEN 'policy_update' WHEN 1 THEN 'price_drop' WHEN 2 THEN 'policy_update' WHEN 3 THEN 'keyword' ELSE 'new_content' END,
       CASE n%5 WHEN 0 THEN 'sub_train_status' WHEN 1 THEN 'sub_flight_status' WHEN 2 THEN 'sub_hotel_terms' WHEN 3 THEN 'sub_city_route' ELSE 'sub_document_rules' END,
       CASE n%10 WHEN 0 THEN '常用车次服务时间调整' WHEN 1 THEN '周末航班价格回落' WHEN 2 THEN '酒店取消规则更新' WHEN 3 THEN '城市道路通行提示' WHEN 4 THEN '证件服务资料上新' WHEN 5 THEN '铁路会员权益变化' WHEN 6 THEN '航站楼交通提醒' WHEN 7 THEN '住宿早餐政策变化' WHEN 8 THEN '公共交通末班时间' ELSE '个人信息保护提示' END,
       CASE n%10 WHEN 0 THEN '部分服务窗口开放时间变化，出发前应通过官方渠道复查。' WHEN 1 THEN '关注航线出现普通价格波动，当前不需要立即下单。' WHEN 2 THEN '可取消产品的截止时间有调整，既有订单不受自动影响。' WHEN 3 THEN '高峰时段局部道路拥堵，建议给市内接驳增加缓冲。' WHEN 4 THEN '新的办事指南已发布，适用事项和材料范围需要分别核对。' WHEN 5 THEN '会员权益规则更新，不改变已经确认的客票状态。' WHEN 6 THEN '机场交通线路调整，乘机当天应核对航站楼入口。' WHEN 7 THEN '部分住宿早餐改为前台预约，入住时可再次确认。' WHEN 8 THEN '夜间末班车时间季节性变化，晚到旅客可准备出租方案。' ELSE '服务平台重申只收集完成当前事项所需的个人字段。' END,
       json_object('record',n,'action','review_when_relevant'),strftime('%Y-%m-%dT%H:00:00+08:00','2026-03-01 08:00:00','+'||(n-1)||' days','+'||(n%8)||' hours'),CASE WHEN n%4=0 THEN 0 ELSE 1 END
FROM seq;
