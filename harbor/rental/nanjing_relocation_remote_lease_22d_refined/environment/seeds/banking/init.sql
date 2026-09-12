PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM "transactions";
DELETE FROM "recurring_payments";
DELETE FROM "pending_payments";
DELETE FROM "payees";
DELETE FROM "accounts";
INSERT INTO "accounts" ("account_id","user_id","type","name","balance_minor","currency","opened_at","frozen") VALUES ('acc_njr_chk','usr_gufeng','checking','Gu Feng rental recordbankrental record',3050000,'CNY','2022-03-01',0);
INSERT INTO "accounts" ("account_id","user_id","type","name","balance_minor","currency","opened_at","frozen") VALUES ('acc_njr_sav','usr_gufeng','savings','Gu Feng rental recordbankrental record+',8200000,'CNY','2022-03-01',0);
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_njr_owner','usr_gufeng','Gu Jianguo','6225********8841','****8841','Industrial and Commercial Bank of China','2026-06-20');
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_njr_d4','usr_gufeng','Zheng Guohua','6217********2290','****2290','inrental recordbank','2026-06-22');
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_h00','usr_gufeng','Nanjingrental record','6228****1000','****1000','rental recordbank','2024-01-15');
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_h01','usr_gufeng','rental recordNanjingrental record','6228****1001','****1001','rental recordbank','2024-01-15');
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_h03','usr_gufeng','Gu Fenglandlord(old)Wuhan','6228****1003','****1003','inrental recordbank','2024-01-15');
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_h04','usr_gufeng','inrental record','6228****1004','****1004','rental recordbank','2024-01-15');
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_h07','usr_gufeng','rental record','6228****1007','****1007','inrental recordbank','2024-01-15');
INSERT INTO "recurring_payments" ("schedule_id","user_id","account_id","payee_id","amount_minor","freq","start_date","end_date","next_run_date","status") VALUES ('rec_water','usr_gufeng','acc_njr_chk','pye_h00',24000,'monthly','2025-01-01',NULL,'2026-07-01','paused');
INSERT INTO "recurring_payments" ("schedule_id","user_id","account_id","payee_id","amount_minor","freq","start_date","end_date","next_run_date","status") VALUES ('rec_power','usr_gufeng','acc_njr_chk','pye_h01',8000,'monthly','2025-01-01',NULL,'2026-07-01','active');
INSERT INTO "recurring_payments" ("schedule_id","user_id","account_id","payee_id","amount_minor","freq","start_date","end_date","next_run_date","status") VALUES ('rec_mobile','usr_gufeng','acc_njr_chk','pye_h04',5900,'monthly','2025-01-01',NULL,'2026-07-01','active');
INSERT INTO "transactions" ("tx_id","account_id","posted_at","amount_minor","kind","counterparty","memo","balance_after_minor") VALUES ('tx_salary_june','acc_njr_chk','2026-06-25T09:12:00Z',1680000,'deposit','Wuhanrental record','rental recordmonthrental record',3568000);
INSERT INTO "transactions" ("tx_id","account_id","posted_at","amount_minor","kind","counterparty","memo","balance_after_minor") VALUES ('tx_old_rent','acc_njr_chk','2026-06-24T11:20:00Z',-260000,'payment','Wuhanoldlandlord','rental recordmonthunitrent',1888000);
INSERT INTO "transactions" ("tx_id","account_id","posted_at","amount_minor","kind","counterparty","memo","balance_after_minor") VALUES ('tx_train_hold','acc_njr_chk','2026-06-23T19:05:00Z',-46300,'payment','rental record12306','WuhantoNanjingrental record',2148000);
INSERT INTO "transactions" ("tx_id","account_id","posted_at","amount_minor","kind","counterparty","memo","balance_after_minor") VALUES ('tx_moving_box','acc_njr_chk','2026-06-21T14:18:00Z',-12800,'payment','rental record','rental recordandrental record',2194300);
INSERT INTO "transactions" ("tx_id","account_id","posted_at","amount_minor","kind","counterparty","memo","balance_after_minor") VALUES ('tx_mobile_june','acc_njr_chk','2026-06-18T08:32:00Z',-5900,'payment','inrental record','rental recordmonthunitrental record',2207100);
INSERT INTO "transactions" ("tx_id","account_id","posted_at","amount_minor","kind","counterparty","memo","balance_after_minor") VALUES ('tx_grocery_week','acc_njr_chk','2026-06-16T20:10:00Z',-18640,'payment','rental record','dayrental record',2213000);
INSERT INTO "transactions" ("tx_id","account_id","posted_at","amount_minor","kind","counterparty","memo","balance_after_minor") VALUES ('tx_savings_interest','acc_njr_sav','2026-06-20T00:10:00Z',12600,'interest','rental recordbank','rental record',8200000);
INSERT INTO "transactions" ("tx_id","account_id","posted_at","amount_minor","kind","counterparty","memo","balance_after_minor") VALUES ('tx_old_deposit_return','acc_njr_chk','2026-06-12T15:40:00Z',180000,'deposit','Wuhanoldlandlord','rental recordcentssecurity depositrental record',2231640);
COMMIT;
-- Keep t=0 free of schedules whose next run or end date is in the future.
DELETE FROM recurring_payments
WHERE (end_date IS NOT NULL AND end_date > '2026-06-28')
   OR (next_run_date IS NOT NULL AND next_run_date > '2026-06-28');
PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;
INSERT INTO accounts(account_id,user_id,type,name,balance_minor,currency,opened_at,frozen) VALUES
('acc_njr_travel','usr_gufeng','checking','Gu Feng rental recordcommunicaterental record',126800,'CNY','2023-09-12',0),
('acc_njr_emergency','usr_gufeng','money_market','Gu Feng shouldurgentrental record',2400000,'CNY','2024-02-18',0),
('acc_njr_education','usr_gufeng','education_fund','Gu Feng rental record',960000,'CNY','2024-08-01',0),
('acc_njr_old_joint','usr_gufeng','savings','Wuhanrental recordnameoldaccount',73500,'CNY','2021-11-06',1);
INSERT INTO payees(payee_id,user_id,name,account_no,account_no_masked,bank_name,added_at) VALUES
('pye_njr_rail','usr_gufeng','rental record12306','6214********3106','****3106','inrental recordbank','2024-03-18'),
('pye_njr_mobile_old','usr_gufeng','inrental recordcompany','6222********4817','****4817','rental recordbank','2023-12-07'),
('pye_njr_broadband_old','usr_gufeng','Wuhanrental recordcommunicaterental record','6216********5290','****5290','inrental recordbank','2023-12-07'),
('pye_njr_course','usr_gufeng','rental record','6228********7724','****7724','rental recordbank','2025-02-16'),
('pye_njr_insurance','usr_gufeng','rental record','6217********1108','****1108','rental recordbank','2024-06-20'),
('pye_njr_storage_wh','usr_gufeng','rental recordyourental record','6226********3645','****3645','rental recordcommunicatebank','2026-05-11'),
('pye_njr_mover_wh','usr_gufeng','Wuhanrental record','6214********9082','****9082','inrental recordbank','2026-05-24'),
('pye_njr_gym','usr_gufeng','rental recordinrental record','6225********2421','****2421','rental recordbank','2024-09-03'),
('pye_njr_cloud','usr_gufeng','rental record','6228********6310','****6310','rental recordbank','2024-01-19'),
('pye_njr_hospital','usr_gufeng','Wuhanrental recordinrental record','6217********7856','****7856','inrental recordbank','2023-08-15'),
('pye_njr_charity','usr_gufeng','Wuhanrental record Station','6222********9054','****9054','rental recordbank','2025-06-02'),
('pye_njr_cardrepay','usr_gufeng','rental recordbankrental recordinrental record','6228********1888','****1888','rental recordbank','2022-03-02');
INSERT INTO transactions(tx_id,account_id,posted_at,amount_minor,kind,counterparty,memo,balance_after_minor) VALUES
('tx_njr_bus_may','acc_njr_travel','2026-05-07T08:16:00Z',-200,'payment','Wuhanrental record','commuterental record',143600),
('tx_njr_metro_may','acc_njr_travel','2026-05-12T18:42:00Z',-480,'payment','WuhanMetro','rental recordMetro',143120),
('tx_njr_rail_refund','acc_njr_travel','2026-05-19T10:28:00Z',32600,'deposit','rental record12306','rental record',175720),
('tx_njr_taxi_station','acc_njr_travel','2026-05-24T06:55:00Z',-3680,'payment','rental recordaboutrental recordplatform','rental record Stationrental record Station',172040),
('tx_njr_bike_month','acc_njr_travel','2026-06-03T07:31:00Z',-1800,'payment','rental record','rental recordmonthrental record',170240),
('tx_njr_travel_transfer','acc_njr_travel','2026-06-15T12:08:00Z',-43440,'transfer_out','rental recordbankrental record','rental recordcommunicaterental record',126800),
('tx_njr_emergency_interest','acc_njr_emergency','2026-05-31T23:59:00Z',8600,'interest','rental recordbank','rental recordmonthrental recordaccountrental record',2391400),
('tx_njr_emergency_topup','acc_njr_emergency','2026-06-05T09:20:00Z',300000,'transfer_in','Gu Fengrental record','rental recordshouldurgentrental record',2691400),
('tx_njr_medical_payment','acc_njr_emergency','2026-06-09T14:36:00Z',-17600,'payment','Wuhanrental recordinrental record','rental record',2673800),
('tx_njr_insurance_renewal','acc_njr_emergency','2026-06-14T08:05:00Z',-128000,'payment','rental record','yearrental recordoutsiderental record',2545800),
('tx_njr_storage_deposit','acc_njr_emergency','2026-06-18T11:44:00Z',-145800,'payment','rental recordyourental record','rental recordmonthrental record',2400000),
('tx_njr_course_refund','acc_njr_education','2026-05-03T16:50:00Z',68000,'deposit','rental record','cancelledrental recordunderrental record',892000),
('tx_njr_course_online','acc_njr_education','2026-05-16T20:12:00Z',-9900,'payment','rental record','onlinerental record',882100),
('tx_njr_book_purchase','acc_njr_education','2026-05-28T13:07:00Z',-12600,'payment','rental record','centsrental record',869500),
('tx_njr_cert_exam','acc_njr_education','2026-06-08T07:48:00Z',-42000,'payment','verifiedrental recordinrental record','rental recordnamerental record',827500),
('tx_njr_education_topup','acc_njr_education','2026-06-21T09:10:00Z',132500,'transfer_in','Gu Fengrental recordaccount','rental record',960000),
('tx_njr_joint_utility','acc_njr_old_joint','2026-05-10T09:00:00Z',-8600,'payment','rental recordWuhanrental record','oldrental recordmonthrental record',106400),
('tx_njr_joint_internet','acc_njr_old_joint','2026-05-18T08:30:00Z',-9900,'payment','Wuhanrental recordcommunicaterental record','rental recordmonthrental record',96500),
('tx_njr_joint_donation','acc_njr_old_joint','2026-06-02T10:15:00Z',-10000,'transfer_out','Wuhanrental record Station','monthrental record',86500),
('tx_njr_joint_fee','acc_njr_old_joint','2026-06-26T00:12:00Z',-13000,'fee','rental recordbank','rental recordnameaccountrental recordandrental record',73500);
INSERT INTO recurring_payments(schedule_id,user_id,account_id,payee_id,amount_minor,freq,start_date,end_date,next_run_date,status) VALUES
('rec_njr_old_broadband','usr_gufeng','acc_njr_old_joint','pye_njr_broadband_old',9900,'monthly','2024-01-01','2026-06-30','2026-06-18','ended'),
('rec_njr_gym_paused','usr_gufeng','acc_njr_chk','pye_njr_gym',12900,'monthly','2025-03-01',NULL,'2026-07-03','paused'),
('rec_njr_cloud_active','usr_gufeng','acc_njr_chk','pye_njr_cloud',1800,'monthly','2024-02-01',NULL,'2026-07-15','active'),
('rec_njr_charity','usr_gufeng','acc_njr_chk','pye_njr_charity',10000,'monthly','2025-06-02',NULL,'2026-07-02','active');
COMMIT;
DELETE FROM recurring_payments
WHERE (end_date IS NOT NULL AND end_date > '2026-06-28')
   OR (next_run_date IS NOT NULL AND next_run_date > '2026-06-28');
