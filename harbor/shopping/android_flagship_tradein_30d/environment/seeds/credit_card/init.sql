-- Stage 0 card state for Pan Yu on 2026-06-15; future duplicate charge and dispute outcome are event-gated.
BEGIN;
INSERT INTO cards (card_id,user_id,issuer,product_name,masked_no,type,credit_limit_minor,available_credit_minor,statement_balance_minor,unbilled_balance_minor,min_payment_due_minor,due_date,cycle_start_day,cycle_end_day,grace_period_days,status,interest_apr_bp) VALUES
('card_andt_01','usr_pan_yu','China Merchants Bank','multi-currency Visa Gold Card','**** **** **** 7426','Visa',5000000,3810000,699900,151200,69990,'2026-07-10',8,7,25,'active',1800),
('CARD-CMB-1183-2269','usr_pan_yu','Bank of Hangzhou','English business noteUnionPay Card','**** **** **** 1183','UnionPay',3000000,2573000,253600,56800,253600,'2026-06-29',18,17,12,'active',1680);
INSERT INTO statements (statement_id,card_id,period_start,period_end,opening_balance_minor,new_charges_minor,payments_minor,closing_balance_minor,min_payment_due_minor,due_date,status) VALUES
('stmt_andt','card_andt_01','2026-06-08','2026-07-07',0,699900,0,699900,69990,'2026-07-10','open'),
('HZB-1183-20260617-R8M3','CARD-CMB-1183-2269','2026-05-18','2026-06-17',112300,253600,112300,253600,253600,'2026-06-29','open');
INSERT INTO statement_lines (line_id,statement_id,posted_at,amount_minor,merchant_name,mcc,category,kind) VALUES
('SL-1183-260519-M4R8','HZB-1183-20260617-R8M3','2026-05-19T08:30:00+08:00',5200,'HangzhouEnglish business note','4111','English business note','purchase'),
('SL-1183-260522-C9V3','HZB-1183-20260617-R8M3','2026-05-22T12:15:00+08:00',6980,'English business note','5812','English business note','purchase'),
('SL-1183-260526-H2Q7','HZB-1183-20260617-R8M3','2026-05-26T20:00:00+08:00',12900,'English business note','4899','English business note','purchase'),
('SL-1183-260530-F8N5','HZB-1183-20260617-R8M3','2026-05-30T18:40:00+08:00',18600,'English business note','5411','English business note','purchase'),
('SL-1183-260603-T3W9','HZB-1183-20260617-R8M3','2026-06-03T21:10:00+08:00',32900,'daysEnglish business note','5311','dayEnglish business note','purchase'),
('SL-1183-260609-P6D4','HZB-1183-20260617-R8M3','2026-06-09T18:30:00+08:00',23800,'English business note','7997','English business note','purchase'),
('SL-1183-260613-J5X8','HZB-1183-20260617-R8M3','2026-06-13T09:10:00+08:00',82220,'English business note','4814','English business note','purchase'),
('SL-1183-260520-B9L2','HZB-1183-20260617-R8M3','2026-05-20T17:40:00+08:00',12800,'English business note','4784','English business note','purchase'),
('SL-1183-260601-R7C5','HZB-1183-20260617-R8M3','2026-06-01T10:25:00+08:00',18600,'English business note','7699','English business note','purchase'),
('SL-1183-260606-K3M6','HZB-1183-20260617-R8M3','2026-06-06T18:15:00+08:00',7600,'English business note','5942','English business note','purchase'),
('SL-1183-260611-V8P4','HZB-1183-20260617-R8M3','2026-06-11T08:05:00+08:00',32000,'English business note','7523','English business note','purchase');
INSERT INTO unbilled_transactions (tx_id,card_id,posted_at,amount_minor,merchant_name,mcc,category,kind) VALUES
('UB-1183-260612-M7Q4','card_andt_01','2026-06-14T12:20:00+08:00',3860,'English business note','5499','English business note','purchase'),
('UB-1183-260613-C5R8','CARD-CMB-1183-2269','2026-06-13T19:00:00+08:00',26800,'English business note','4121','English business note','purchase'),
('UB-1183-260614-T9K2','CARD-CMB-1183-2269','2026-06-15T08:10:00+08:00',30000,'English business note','5311','English business note','purchase');
INSERT INTO payments (payment_id,card_id,posted_at,amount_minor,source_hint,applied_to_statement_minor,applied_to_unbilled_minor) VALUES
('PMT-7426-260610-A8K3','CARD-CMB-1183-2269','2026-05-29T08:30:00+08:00',112300,'Bank of HangzhouEnglish business note',112300,0),
('PMT-1183-260612-P5V9','card_andt_01','2026-05-10T09:00:00+08:00',318500,'China Merchants BankEnglish business note',318500,0);
INSERT INTO disputes (dispute_id,card_id,tx_id,reason,status,opened_at,expected_resolution_date,resolved_at) VALUES
('DSP-1183-20260422-T6V9','CARD-CMB-1183-2269','UB-1183-260613-C5R8','English business notenot yetEnglish business note','approved','2026-04-22T10:00:00+08:00','2026-04-29','2026-04-26T15:20:00+08:00');
INSERT INTO rewards_balances (card_id,points_balance,ytd_earned,lifetime_earned,updated_at) VALUES
('card_andt_01',23680,12400,71800,'2026-06-15T00:00:00Z'),('CARD-CMB-1183-2269',8840,4520,33600,'2026-06-15T00:00:00Z');
INSERT INTO rewards_ledger (ledger_id,card_id,posted_at,kind,delta,balance_after,note) VALUES
('RWD-1183-260613-C5K7','CARD-CMB-1183-2269','2026-06-13T09:10:00+08:00','earn',822,8840,'English business notestatementEnglish business note'),
('RDM-1183-260601-P3V9','CARD-CMB-1183-2269','2026-06-01T09:00:00+08:00','redeem',-1500,8018,'English business note'),
('RWD-7426-260531-H6T2','card_andt_01','2026-05-31T09:00:00+08:00','earn',560,9682,'monthEnglish business note');
INSERT INTO _counters (key,value) VALUES ('payment_seq',2),('line_seq',12),('dispute_seq',1),('ledger_seq',4);
COMMIT;
