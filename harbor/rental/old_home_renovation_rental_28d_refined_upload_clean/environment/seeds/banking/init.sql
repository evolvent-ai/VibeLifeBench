PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM "transactions";
DELETE FROM "recurring_payments";
DELETE FROM "pending_payments";
DELETE FROM "payees";
DELETE FROM "accounts";
INSERT INTO "accounts" ("account_id","user_id","type","name","balance_minor","currency","opened_at","frozen") VALUES ('acct_zl_renovation','usr_zhanglan','checking','renovationrentaltranslated source text',12800000,'CNY','2025-03-01T09:00:00+08:00',0);
INSERT INTO "accounts" ("account_id","user_id","type","name","balance_minor","currency","opened_at","frozen") VALUES ('acct_zl_reserve','usr_zhanglan','savings','reservetranslated source text',3000000,'CNY','2024-01-01T09:00:00+08:00',0);
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_7M2Q8V','usr_zhanglan','Shanghaitranslated source text','6225758419362047','****2047','translated source textShanghaitranslated source text','2026-07-01T09:00:00+08:00');
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_4R8N1C','usr_zhanglan','translated source textair-quality testingtranslated source text','6217003864529186','****9186','translated source textShanghaitranslated source text','2026-07-01T09:00:00+08:00');
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_6T1C9K','usr_zhanglan','Hongqiao Jiayuanproperty managementtranslated source text','6222024581736609','****6609','translated source textShanghaitranslated source text','2026-07-01T09:00:00+08:00');
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_9P3D5L','usr_zhanglan','translated source textpersonal account','6228481057293341','****3341','translated source textShanghaitranslated source text','2026-07-01T09:00:00+08:00');
INSERT INTO "payees" ("payee_id","user_id","name","account_no","account_no_masked","bank_name","added_at") VALUES ('pye_2K7V4S','usr_zhanglan','agenttranslated source text','6226229041857728','****7728','translated source textShanghaitranslated source text','2026-07-01T09:00:00+08:00');
INSERT INTO "transactions" ("tx_id","account_id","posted_at","amount_minor","kind","counterparty","memo","balance_after_minor") VALUES ('tx_initial_budget','acct_zl_renovation','2026-07-01T08:00:00+08:00',12800000,'deposit','Zhang Lan','renovationrentaltranslated source text',12800000);
COMMIT;
PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;
INSERT INTO accounts(account_id,user_id,type,name,balance_minor,currency,opened_at,frozen) VALUES
('acct_zl_household','usr_zhanglan','checking','translated source text daytranslated source text',4860000,'CNY','2019-04-12T09:00:00+08:00',0),
('acc_CMB_20200820_7KqM','usr_zhanglan','savings','translated source text',2150000,'CNY','2020-08-20T09:00:00+08:00',0),
('acct_zl_tax_reserve','usr_zhanglan','money_market','translated source text',1760000,'CNY','2023-01-06T09:00:00+08:00',0),
('acct_zl_home_fund','usr_zhanglan','savings','translated source text',920000,'CNY','2022-06-15T09:00:00+08:00',0);
INSERT INTO payees(payee_id,user_id,name,account_no,account_no_masked,bank_name,added_at) VALUES
('payee_sh_water','usr_zhanglan','Shanghaitranslated source text','6228********4012','****4012','translated source textShanghaitranslated source text','2021-01-18T10:00:00+08:00'),
('payee_sh_power','usr_zhanglan','translated source textShanghaitranslated source text','6217********5216','****5216','translated source textShanghaitranslated source text','2021-01-18T10:05:00+08:00'),
('payee_hj_property_old','usr_zhanglan','Hongqiao Jiayuanproperty managementtranslated source text','6222********1187','****1187','translated source textShanghaitranslated source text','2021-02-02T09:20:00+08:00'),
('payee_home_insurer','usr_zhanglan','translated source text','6214********7623','****7623','translated source textShanghaitranslated source text','2022-08-11T14:10:00+08:00'),
('payee_locksmith','usr_zhanglan','Minhangtranslated source text','6226********3058','****3058','translated source textShanghaitranslated source text','2024-03-17T11:30:00+08:00'),
('payee_appliance_repair','usr_zhanglan','translated source textappliancestranslated source text','6225********6842','****6842','translated source textShanghaitranslated source text','2024-10-06T16:45:00+08:00'),
('payee_QBpipe_7K4m','usr_zhanglan','Qibaotranslated source text','6216********9320','****9320','translated source textShanghaitranslated source text','2025-05-12T08:25:00+08:00'),
('payee_tax_bureau','usr_zhanglan','Shanghaitranslated source text','6228********2109','****2109','translated source textShanghaitranslated source text','2023-01-06T09:15:00+08:00'),
('payee_MHstore_9QxV','usr_zhanglan','Minhangtranslated source text','6217********4471','****4471','translated source textShanghaitranslated source text','2025-11-20T12:05:00+08:00'),
('payee_internet','usr_zhanglan','Shanghaitranslated source text','6222********8254','****8254','translated source textShanghaitranslated source text','2021-01-18T10:10:00+08:00'),
('payee_HJclean_5MpR','usr_zhanglan','translated source text','6214********5706','****5706','translated source textShanghaitranslated source text','2025-02-08T15:30:00+08:00'),
('payee_fire_service','usr_zhanglan','Minhangtranslated source text','6226********1468','****1468','translated source textShanghaitranslated source text','2025-08-19T09:40:00+08:00');
INSERT INTO transactions(tx_id,account_id,posted_at,amount_minor,kind,counterparty,memo,balance_after_minor) VALUES
('tx_zl_water_jan','acct_zl_household','2026-01-08T07:20:00+08:00',-8600,'payment','Shanghaitranslated source text','Hongqiao Jiayuantranslated source text',5124600),
('tx_zl_power_jan','acct_zl_household','2026-01-12T08:10:00+08:00',-12600,'payment','translated source textShanghaitranslated source text','translated source text monthtranslated source text',5112000),
('tx_zl_internet_feb','acct_zl_household','2026-02-03T09:15:00+08:00',-19900,'payment','Shanghaitranslated source text','translated source text monthtranslated source text',5092100),
('tx_zl_lock_service','acct_zl_household','2026-02-16T16:40:00+08:00',-36000,'payment','Minhangtranslated source text','translated source text',5056100),
('tx_zl_insurance_mar','acct_zl_household','2026-03-05T10:25:00+08:00',-68000,'payment','translated source text','translated source text',4988100),
('tx_zl_cleaning_apr','acct_zl_household','2026-04-09T14:08:00+08:00',-42000,'payment','translated source text','translated source text',4946100),
('tx_zl_appliance_may','acct_zl_household','2026-05-18T12:32:00+08:00',-58000,'payment','translated source textappliancestranslated source text','translated source text',4888100),
('tx_zl_mobile_june','acct_zl_household','2026-06-06T07:45:00+08:00',-9800,'payment','translated source text','translated source text monthtranslated source text',4878300),
('tx_zl_grocery_june','acct_zl_household','2026-06-19T20:18:00+08:00',-18300,'payment','Qibaotranslated source text','translated source text daytranslated source text',4860000),
('tx_zl_rent_2025dec','acc_CMB_20200820_7KqM','2025-12-05T10:00:00+08:00',760000,'deposit','Hongqiao Jiayuantranslated source texttenant','translated source text monthtranslated source text',2680000),
('tx_zl_rent_2026jan','acc_CMB_20200820_7KqM','2026-01-05T10:00:00+08:00',760000,'deposit','Hongqiao Jiayuantranslated source texttenant','translated source text monthtranslated source text',3440000),
('tx_zl_property_q1','acc_CMB_20200820_7KqM','2026-01-10T09:30:00+08:00',-186000,'payment','Hongqiao Jiayuanproperty management','translated source textproperty managementtranslated source text',3254000),
('tx_zl_rent_2026feb','acc_CMB_20200820_7KqM','2026-02-05T10:00:00+08:00',760000,'deposit','Hongqiao Jiayuantranslated source texttenant','translated source text monthtranslated source text',4014000),
('tx_zl_plumber_feb','acc_CMB_20200820_7KqM','2026-02-22T13:15:00+08:00',-48000,'payment','Qibaotranslated source text','translated source text',3966000),
('tx_zl_rent_2026mar','acc_CMB_20200820_7KqM','2026-03-05T10:00:00+08:00',760000,'deposit','Hongqiao Jiayuantranslated source texttenant','translated source text monthtranslated source text',4726000),
('tx_zl_deposit_return','acc_CMB_20200820_7KqM','2026-04-02T15:20:00+08:00',-1520000,'transfer_out','Hongqiao Jiayuantranslated source texttenant','translated source textleasetranslated source text',3206000),
('tx_zl_old_damage_deduct','acc_CMB_20200820_7KqM','2026-04-04T11:42:00+08:00',-76000,'payment','translated source textappliancestranslated source text','translated source text',3130000),
('txn_20260501_C8mQ4V','acc_CMB_20200820_7KqM','2026-05-01T09:05:00+08:00',-980000,'transfer_out','Zhang Lantranslated source text','translated source text',2150000),
('tx_zl_tax_interest','acct_zl_tax_reserve','2026-01-31T23:58:00+08:00',5200,'interest','translated source text','translated source text monthtranslated source text',1655200),
('tx_zl_tax_topup','acct_zl_tax_reserve','2026-02-06T08:30:00+08:00',180000,'transfer_in','Zhang Lantranslated source text','translated source text',1835200),
('tx_zl_tax_payment','acct_zl_tax_reserve','2026-03-18T10:12:00+08:00',-108000,'payment','Shanghaitranslated source text','translated source text',1727200),
('tx_zl_tax_interest_may','acct_zl_tax_reserve','2026-05-31T23:58:00+08:00',32800,'interest','translated source text','translated source text',1760000),
('tx_zl_fund_fire','acct_zl_home_fund','2026-02-18T15:35:00+08:00',-26800,'payment','Minhangtranslated source text','translated source text',1006800),
('tx_zl_fund_storage','acct_zl_home_fund','2026-04-12T09:45:00+08:00',-72000,'payment','Minhangtranslated source text','translated source text',934800),
('tx_zl_fund_interest','acct_zl_home_fund','2026-05-31T23:55:00+08:00',7200,'interest','translated source text','translated source text monthtranslated source text',942000),
('tx_zl_fund_tool','acct_zl_home_fund','2026-06-24T13:32:00+08:00',-22000,'payment','JD Logisticstranslated source text','translated source text',920000);
INSERT INTO recurring_payments(schedule_id,user_id,account_id,payee_id,amount_minor,freq,start_date,end_date,next_run_date,status) VALUES
('rp_SHWater_7VnQ','usr_zhanglan','acct_zl_household','payee_sh_water',8600,'monthly','2025-01-08','2026-06-30','2026-06-08','ended'),
('rp_SHPower_4KqM','usr_zhanglan','acct_zl_household','payee_sh_power',12600,'monthly','2025-01-12','2026-06-30','2026-06-12','ended'),
('rec_zl_internet_paused','usr_zhanglan','acct_zl_household','payee_internet',19900,'monthly','2024-01-03',NULL,'2026-07-03','paused'),
('rec_zl_property_old','usr_zhanglan','acc_CMB_20200820_7KqM','payee_hj_property_old',186000,'monthly','2025-01-10','2026-03-31','2026-03-10','ended'),
('rec_zl_insurance_yearly','usr_zhanglan','acct_zl_household','payee_home_insurer',68000,'monthly','2026-03-05','2026-03-05','2026-03-05','ended');
COMMIT;

BEGIN TRANSACTION;
INSERT INTO transactions(tx_id,account_id,posted_at,amount_minor,kind,counterparty,memo,balance_after_minor) VALUES
('tx_zl_hinge_purchase','acct_zl_household','2026-05-12T10:39:00+08:00',-13500,'payment','translated source text','translated source text',3286500),
('tx_zl_hinge_refund','acct_zl_household','2026-05-19T16:32:00+08:00',12900,'transfer_in','translated source text','translated source text',3299400);
COMMIT;
