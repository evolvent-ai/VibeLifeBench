-- Reviewed Stage 0 banking state: 55 records, all transactions predate 2026-04-03 08:20 +08:00.
INSERT INTO accounts(account_id,user_id,type,name,balance_minor,currency,opened_at,frozen) VALUES
 ('acct_lin_main_cny','user_lin_che','checking','林澈日常账户',2200000,'CNY','2021-01-01T00:00:00+08:00',0),
 ('acct_lin_reserve_cny','user_lin_che','savings','家庭应急储蓄',8600000,'CNY','2020-06-18T00:00:00+08:00',0);

INSERT INTO payees(payee_id,user_id,name,account_no,account_no_masked,bank_name,added_at) VALUES
 ('payee_suzhou_funeral_home','user_lin_che','苏州市殡仪服务中心','6222021000000188','****0188','工商银行苏州吴中支行','2026-03-18T10:00:00+08:00'),
 ('payee_lin_mother','user_lin_che','周慧兰','6222081000000888','****0888','宁波银行海曙支行','2023-05-12T09:30:00+08:00'),
 ('payee_property_beijing','user_lin_che','北辰家园物业','6222001000002361','****2361','建设银行北京安贞支行','2022-09-01T12:00:00+08:00'),
 ('payee_mobile','user_lin_che','中国移动北京分公司','955880001036','****1036','工商银行北京分行','2021-03-08T08:20:00+08:00'),
 ('payee_power','user_lin_che','国网北京电力','955980006118','****6118','中国银行北京分行','2021-03-08T08:25:00+08:00'),
 ('payee_insurance','user_lin_che','华安旅行保险','6222600880003172','****3172','交通银行上海分行','2025-08-14T14:10:00+08:00');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<45)
INSERT INTO transactions(tx_id,account_id,posted_at,amount_minor,kind,counterparty,memo,balance_after_minor)
SELECT printf('tx_history_%03d',n),
       CASE WHEN n IN (9,22,37) THEN 'acct_lin_reserve_cny' ELSE 'acct_lin_main_cny' END,
       strftime('%Y-%m-%dT%H:%M:00+08:00','2026-01-14 08:00:00','+'||n||' days','+'||(n%11)||' hours'),
       CASE n%10 WHEN 0 THEN 315000 WHEN 1 THEN -12600 WHEN 2 THEN -39800 WHEN 3 THEN -8800 WHEN 4 THEN -52000 WHEN 5 THEN -16800 WHEN 6 THEN -23600 WHEN 7 THEN -7600 WHEN 8 THEN -28900 ELSE 4200 END,
       CASE n%10 WHEN 0 THEN 'deposit' WHEN 9 THEN 'interest' ELSE 'payment' END,
       CASE n%10 WHEN 0 THEN '华辰设计院' WHEN 1 THEN '社区药房' WHEN 2 THEN '京客隆超市' WHEN 3 THEN '北京一卡通' WHEN 4 THEN '北京燃气' WHEN 5 THEN '中国铁路网络售票' WHEN 6 THEN '家庭餐饮' WHEN 7 THEN '中国移动' WHEN 8 THEN '国网北京电力' ELSE '账户结息' END,
       CASE n%10 WHEN 0 THEN '月度工资入账' WHEN 1 THEN '家庭常用药采购' WHEN 2 THEN '周末生活用品' WHEN 3 THEN '市内交通充值' WHEN 4 THEN '居民燃气预存' WHEN 5 THEN '探亲往返车票' WHEN 6 THEN '家庭聚餐结算' WHEN 7 THEN '月度通信费用' WHEN 8 THEN '居民用电缴费' ELSE '季度活期利息' END,
       CASE WHEN n IN (9,22,37) THEN 8600000+n*1200 ELSE 2200000-(45-n)*1700 END
FROM seq;

INSERT INTO recurring_payments(schedule_id,user_id,account_id,payee_id,amount_minor,freq,start_date,end_date,next_run_date,status) VALUES
 ('recurring_mobile_monthly','user_lin_che','acct_lin_main_cny','payee_mobile',11800,'monthly','2025-01-05',NULL,'2026-04-05','active'),
 ('recurring_property_quarter','user_lin_che','acct_lin_main_cny','payee_property_beijing',86000,'monthly','2025-07-12','2026-06-12','2026-04-12','active');
