-- Stage 0 card state for  translated text  on 2026-06-15; future duplicate charge, dispute approval and credits are absent.
BEGIN;
INSERT INTO cards (card_id,user_id,issuer,product_name,masked_no,type,credit_limit_minor,available_credit_minor,statement_balance_minor,unbilled_balance_minor,min_payment_due_minor,due_date,cycle_start_day,cycle_end_day,grace_period_days,status,interest_apr_bp) VALUES
('card_awch_01','usr_mo_fan','China Merchants Bank','Classic White Visa','**** **** **** 8634','Visa',4000000,3120000,459900,113600,45990,'2026-07-10',8,7,25,'active',1800),
('card_awch_02','usr_mo_fan','SPDB Shanghai Life UnionPay',' translated text ','**** **** **** 2751','UnionPay',3000000,2586600,266800,42600,266800,'2026-06-29',18,17,12,'active',1700);
INSERT INTO statements (statement_id,card_id,period_start,period_end,opening_balance_minor,new_charges_minor,payments_minor,closing_balance_minor,min_payment_due_minor,due_date,status) VALUES
('stmt_awch','card_awch_01','2026-06-08','2026-07-07',0,459900,0,459900,45990,'2026-07-10','open'),
('SPDB-2751-20260617-L5C8','card_awch_02','2026-05-18','2026-06-17',95400,266800,95400,266800,266800,'2026-06-29','open');
INSERT INTO statement_lines (line_id,statement_id,posted_at,amount_minor,merchant_name,mcc,category,kind) VALUES
('line_awch_1','stmt_awch','2026-06-15T19:20:05+08:00',459900,'Apple official translated text ','5732','wearable electronics','purchase'),
('SPDB-METRO-0519-H2Q7','SPDB-2751-20260617-L5C8','2026-05-19T08:25:00+08:00',4200,' translated text ','4111',' translated text ','purchase'),
('SPDB-LUNCH-0522-C8M4','SPDB-2751-20260617-L5C8','2026-05-22T12:40:00+08:00',7280,' translated text ','5812',' translated text ','purchase'),
('SPDB-CLOUD-0526-P5R9','SPDB-2751-20260617-L5C8','2026-05-26T20:10:00+08:00',11800,' translated text ','4899',' translated text ','purchase'),
('SPDB-ALDI-0530-W3K6','SPDB-2751-20260617-L5C8','2026-05-30T18:20:00+08:00',19800,' translated text ','5411',' translated text ','purchase'),
('SPDB-IKEA-0603-N7V2','SPDB-2751-20260617-L5C8','2026-06-03T21:30:00+08:00',25900,' translated text Home translated text ','5712','Home translated text ','purchase'),
('SPDB-SPORTS-0609-F4L8','SPDB-2751-20260617-L5C8','2026-06-09T18:30:00+08:00',26800,' translated text ','7997',' translated text ','purchase'),
('SPDB-TELECOM-0613-J6T1','SPDB-2751-20260617-L5C8','2026-06-13T09:10:00+08:00',62620,' translated text ','4814',' translated text ','purchase'),
('SPDB-ARTPASS-0521-B9D5','SPDB-2751-20260617-L5C8','2026-05-21T14:20:00+08:00',16800,' translated text ','7991',' translated text ','purchase'),
('SPDB-OPTICAL-0605-X2S7','SPDB-2751-20260617-L5C8','2026-06-05T18:40:00+08:00',68000,' translated text ','8043',' translated text ','purchase'),
('SPDB-PETCLINIC-0612-M8C3','SPDB-2751-20260617-L5C8','2026-06-12T09:35:00+08:00',23600,' translated text ','0742',' translated text ','purchase');
INSERT INTO unbilled_transactions (tx_id,card_id,posted_at,amount_minor,merchant_name,mcc,category,kind) VALUES
('tx_awch_1','card_awch_01','2026-06-15T10:05:08+08:00',92000,'Apple Store','5732','wearable electronics','purchase'),
('tx_awch_fx','card_awch_01','2026-06-15T11:30:00+08:00',14800,'GAZELLE US','4814','wearable electronics','purchase'),
('CMB-LAWSON-0614-Q4N8','card_awch_01','2026-06-14T12:20:00+08:00',3460,' translated text ','5499',' translated text ','purchase'),
('SPDB-TAXI-0613-V7H2','card_awch_02','2026-06-13T19:00:00+08:00',17600,' translated text ','4121',' translated text ','purchase'),
('SPDB-GROCERY-0615-K3P9','card_awch_02','2026-06-15T08:10:00+08:00',25000,' translated text ','5411',' translated text ','purchase');
INSERT INTO payments (payment_id,card_id,posted_at,amount_minor,source_hint,applied_to_statement_minor,applied_to_unbilled_minor) VALUES
('pay_awch_01','card_awch_02','2026-05-29T08:30:00+08:00',95400,' translated text account',95400,0),
('pay_awch_02','card_awch_01','2026-05-10T09:00:00+08:00',268500,'China Merchants Bank translated text ',268500,0);
INSERT INTO disputes (dispute_id,card_id,tx_id,reason,status,opened_at,expected_resolution_date,resolved_at) VALUES
('DSP-2751-20260613-P3H6','card_awch_02','SPDB-TAXI-0613-V7H2',' translated text ','approved','2026-06-13T20:00:00+08:00','2026-06-20','2026-06-14T15:20:00+08:00');
INSERT INTO rewards_balances (card_id,points_balance,ytd_earned,lifetime_earned,updated_at) VALUES
('card_awch_01',20480,10800,65200,'2026-06-15T00:00:00Z'),('card_awch_02',7350,3980,30100,'2026-06-15T00:00:00Z');
INSERT INTO rewards_ledger (ledger_id,card_id,posted_at,kind,delta,balance_after,note) VALUES
('rl_awch_1','card_awch_01','2026-06-15T19:20:05+08:00','earn',9198,20480,' translated text tableorder translated text confirm'),
('rl_awch_2','card_awch_02','2026-06-13T09:10:00+08:00','earn',626,7350,' translated text statement translated text '),
('rl_awch_3','card_awch_02','2026-06-01T09:00:00+08:00','redeem',-1000,6724,' translated text coupon'),
('rl_awch_4','card_awch_01','2026-05-31T09:00:00+08:00','earn',480,11282,' translated text active translated text ');
INSERT INTO _counters (key,value) VALUES ('payment_seq',2),('line_seq',11),('dispute_seq',1),('ledger_seq',4);
COMMIT;
