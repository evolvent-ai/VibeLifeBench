-- Reviewed Stage 0 banking state: 55 records, all transactions predate 2026-04-03 08:20 +08:00.
INSERT INTO accounts(account_id,user_id,type,name,balance_minor,currency,opened_at,frozen) VALUES
 ('acct_lin_main_cny','user_lin_che','checking','Lin Chedaily account',2200000,'CNY','2021-01-01T00:00:00+08:00',0),
 ('acct_lin_reserve_cny','user_lin_che','savings','family emergency savings',8600000,'CNY','2020-06-18T00:00:00+08:00',0);

INSERT INTO payees(payee_id,user_id,name,account_no,account_no_masked,bank_name,added_at) VALUES
 ('payee_suzhou_funeral_home','user_lin_che','Suzhou Funeral Service Center','6222021000000188','****0188','ICBCSuzhouWuzhongscenario text','2026-03-18T10:00:00+08:00'),
 ('payee_lin_mother','user_lin_che','Zhou Huilan','6222081000000888','****0888','Bank of NingboHaishuscenario text','2023-05-12T09:30:00+08:00'),
 ('payee_property_beijing','user_lin_che','scenario text','6222001000002361','****2361','China Construction BankBeijingscenario text','2022-09-01T12:00:00+08:00'),
 ('payee_mobile','user_lin_che','China MobileBeijingscenario text','955880001036','****1036','ICBCBeijingscenario text','2021-03-08T08:20:00+08:00'),
 ('payee_power','user_lin_che','State Grid Beijing Electric','955980006118','****6118','Bank of ChinaBeijingscenario text','2021-03-08T08:25:00+08:00'),
 ('payee_insurance','user_lin_che','Hua’an Travel Insurance','6222600880003172','****3172','Bank of CommunicationsShanghaiscenario text','2025-08-14T14:10:00+08:00');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<45)
INSERT INTO transactions(tx_id,account_id,posted_at,amount_minor,kind,counterparty,memo,balance_after_minor)
SELECT printf('tx_history_%03d',n),
       CASE WHEN n IN (9,22,37) THEN 'acct_lin_reserve_cny' ELSE 'acct_lin_main_cny' END,
       strftime('%Y-%m-%dT%H:%M:00+08:00','2026-01-14 08:00:00','+'||n||' days','+'||(n%11)||' hours'),
       CASE n%10 WHEN 0 THEN 315000 WHEN 1 THEN -12600 WHEN 2 THEN -39800 WHEN 3 THEN -8800 WHEN 4 THEN -52000 WHEN 5 THEN -16800 WHEN 6 THEN -23600 WHEN 7 THEN -7600 WHEN 8 THEN -28900 ELSE 4200 END,
       CASE n%10 WHEN 0 THEN 'deposit' WHEN 9 THEN 'interest' ELSE 'payment' END,
       CASE n%10 WHEN 0 THEN 'Huachen Design Institute' WHEN 1 THEN 'community pharmacy' WHEN 2 THEN 'Jingkelong supermarket' WHEN 3 THEN 'Beijingscenario text' WHEN 4 THEN 'Beijingscenario text' WHEN 5 THEN 'China Railway online ticketing' WHEN 6 THEN 'family dining' WHEN 7 THEN 'China Mobile' WHEN 8 THEN 'State Grid Beijing Electric' ELSE 'account interest' END,
       CASE n%10 WHEN 0 THEN 'monthly salary deposit' WHEN 1 THEN 'routine family medicine purchase' WHEN 2 THEN 'weekend household supplies' WHEN 3 THEN 'city transit top-up' WHEN 4 THEN 'residential gas prepayment' WHEN 5 THEN 'family-visit round-trip ticket' WHEN 6 THEN 'family meal settlement' WHEN 7 THEN 'monthly communications bill' WHEN 8 THEN 'residential electricity bill' ELSE 'quarterly checking interest' END,
       CASE WHEN n IN (9,22,37) THEN 8600000+n*1200 ELSE 2200000-(45-n)*1700 END
FROM seq;

INSERT INTO recurring_payments(schedule_id,user_id,account_id,payee_id,amount_minor,freq,start_date,end_date,next_run_date,status) VALUES
 ('recurring_mobile_monthly','user_lin_che','acct_lin_main_cny','payee_mobile',11800,'monthly','2025-01-05',NULL,'2026-04-05','active'),
 ('recurring_property_quarter','user_lin_che','acct_lin_main_cny','payee_property_beijing',86000,'monthly','2025-07-12','2026-06-12','2026-04-12','active');
