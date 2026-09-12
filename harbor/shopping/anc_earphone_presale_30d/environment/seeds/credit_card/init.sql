-- Stage 0 card state for [translated note] on 2026-06-15; later duplicate charge/dispute/refunds are absent.
BEGIN;
INSERT INTO cards (card_id,user_id,issuer,product_name,masked_no,type,credit_limit_minor,available_credit_minor,statement_balance_minor,unbilled_balance_minor,min_payment_due_minor,due_date,cycle_start_day,cycle_end_day,grace_period_days,status,interest_apr_bp) VALUES
('card_psea_01','usr_teng_qi',char(25307) || char(21830) || char(38134) || char(34892),'Young ' || char(21345) || ' Visa','**** **** **** 3957','Visa',3000000,2442140,229900,327960,50000,'2026-07-10',6,5,25,'active',1800),
('card_psea_02','usr_teng_qi',char(20013) || char(22269) || char(38134) || char(34892),char(38271) || char(22478) || char(38134) || char(32852) || char(30333) || char(37329) || char(21345),'**** **** **** 6812','UnionPay',5000000,4466600,172100,37600,172100,'2026-06-28',16,15,13,'active',1650);
INSERT INTO statements (statement_id,card_id,period_start,period_end,opening_balance_minor,new_charges_minor,payments_minor,closing_balance_minor,min_payment_due_minor,due_date,status) VALUES
('CMB-3957-202606','card_psea_01','2026-05-06','2026-06-05',0,229900,0,229900,50000,'2026-07-10','open'),
('BOC-6812-20260615-E7Q4','card_psea_02','2026-05-16','2026-06-15',84300,172100,84300,172100,172100,'2026-06-28','open');
INSERT INTO statement_lines (line_id,statement_id,posted_at,amount_minor,merchant_name,mcc,category,kind) VALUES
('CMB3957-0603-K8Q2','CMB-3957-202606','2026-06-03T19:20:05+08:00',229900,char(21271) || char(20140) || char(21548) || char(28572) || char(25968) || char(30721) || char(22478),'5732',char(25968) || char(30721) || char(24433) || char(38899),'purchase'),
('BOC6812-0518-M7R4','BOC-6812-20260615-E7Q4','2026-05-18T08:10:00+08:00',2860,char(21271) || char(20140) || char(22320) || char(38081) || char(20056) || char(36710) || char(30721),'4111',char(20132) || char(36890),'purchase'),
('BOC6812-0520-C4N8','BOC-6812-20260615-E7Q4','2026-05-20T12:20:00+08:00',4580,char(36731) || char(39135) || char(30740) || char(31350) || char(25152),'5812',char(39184) || char(39278),'purchase'),
('BOC6812-0523-V9L2','BOC-6812-20260615-E7Q4','2026-05-23T21:00:00+08:00',6990,char(20113) || char(38899) || char(20048) || char(20250) || char(21592),'4899',char(25968) || char(23383) || char(26381) || char(21153),'purchase'),
('BOC6812-0527-H5T1','BOC-6812-20260615-E7Q4','2026-05-27T18:30:00+08:00',12800,char(30418) || char(39532) || char(40092) || char(29983),'5411',char(21830) || char(36229),'purchase'),
('BOC6812-0601-D3P7','BOC-6812-20260615-E7Q4','2026-06-01T10:15:00+08:00',39900,char(26397) || char(38451) || char(38376) || char(21475) || char(33108) || char(38376) || char(35786),'8021',char(21307) || char(30103),'purchase'),
('BOC6812-0608-J6W3','BOC-6812-20260615-E7Q4','2026-06-08T09:00:00+08:00',29800,char(20140) || char(19996) || char(21040) || char(23478),'5411',char(26085) || char(29992),'purchase'),
('BOC6812-0612-S2F9','BOC-6812-20260615-E7Q4','2026-06-12T19:40:00+08:00',29770,char(39034) || char(20016) || char(20248) || char(36873),'4215',char(29983) || char(27963) || char(26381) || char(21153),'purchase'),
('BOC6812-0525-A8X6','BOC-6812-20260615-E7Q4','2026-05-25T19:30:00+08:00',26800,char(21271) || char(20140) || char(29233) || char(20048) || char(38899) || char(20048) || char(21381),'7922',char(25991) || char(21270) || char(23089) || char(20048),'purchase'),
('BOC6812-0606-B4K5','BOC-6812-20260615-E7Q4','2026-06-06T11:15:00+08:00',18600,char(21452) || char(20117) || char(33258) || char(34892) || char(36710) || char(24037) || char(22346),'7699',char(32500) || char(20462) || char(26381) || char(21153),'purchase');
INSERT INTO unbilled_transactions (tx_id,card_id,posted_at,amount_minor,merchant_name,mcc,category,kind) VALUES
('tx-SNP-0610-MAIN','card_psea_01','2026-06-10T19:27:00+08:00',229900,'SonicPod ' || char(23448) || char(26041) || char(26071) || char(33328) || char(24215),'5732',char(25968) || char(30721) || char(24433) || char(38899),'purchase'),
('tx-SNP-0612-DEP','card_psea_01','2026-06-12T10:09:00+08:00',84000,'SonicPod ' || char(23448) || char(26041) || char(24215) || '（' || char(39044) || char(21806) || char(23450) || char(37329) || '）','5732',char(25968) || char(30721) || char(24433) || char(38899),'purchase'),
('tx_psea_fx','card_psea_01','2026-06-15T08:30:00+08:00',10800,'PAYPAL US','4814',char(25968) || char(30721) || char(24433) || char(38899),'purchase'),
('tx-CVS-0614-3N8Q','card_psea_01','2026-06-14T12:35:00+08:00',3260,char(20415) || char(21033) || char(34562) || char(22269) || char(36152) || char(24215),'5499',char(20415) || char(21033) || char(24215),'purchase'),
('tx-DIDI-0613-6V2M','card_psea_02','2026-06-13T18:10:00+08:00',12800,char(28404) || char(28404) || char(20986) || char(34892),'4121',char(20132) || char(36890),'purchase'),
('tx-JDH-0615-9K4R','card_psea_02','2026-06-15T07:50:00+08:00',21540,char(20140) || char(19996) || char(20581) || char(24247),'5912',char(20581) || char(24247),'purchase');
INSERT INTO payments (payment_id,card_id,posted_at,amount_minor,source_hint,applied_to_statement_minor,applied_to_unbilled_minor) VALUES
('PAY-BOC6812-0528','card_psea_02','2026-05-28T09:00:00+08:00',84300,char(24037) || char(36164) || char(21345) || char(33258) || char(21160) || char(36824) || char(27454),84300,0),
('PAY-CMB3957-0508','card_psea_01','2026-05-08T08:30:00+08:00',156400,char(25307) || char(21830) || char(38134) || char(34892) || char(20648) || char(33988) || char(21345),156400,0);
INSERT INTO disputes (dispute_id,card_id,tx_id,reason,status,opened_at,expected_resolution_date,resolved_at) VALUES
('DSP-6812-20260502-N4K7','card_psea_02','tx-DIDI-0613-6V2M',char(32593) || char(32422) || char(36710) || char(21462) || char(28040) || char(21518) || char(26410) || char(21450) || char(26102) || char(25764) || char(38144) || char(39044) || char(25480) || char(26435),'approved','2026-05-02T11:00:00+08:00','2026-05-09','2026-05-06T16:00:00+08:00');
INSERT INTO rewards_balances (card_id,points_balance,ytd_earned,lifetime_earned,updated_at) VALUES
('card_psea_01',18420,9650,54200,'2026-06-15T00:00:00Z'),('card_psea_02',7630,3120,28800,'2026-06-15T00:00:00Z');
INSERT INTO rewards_ledger (ledger_id,card_id,posted_at,kind,delta,balance_after,note) VALUES
('RWD-CMB3957-0610','card_psea_01','2026-06-10T19:27:05+08:00','earn',6899,18420,'SonicPod ' || char(35746) || char(21333) || char(31215) || char(20998) || char(24453) || char(30830) || char(35748)),
('RWD-BOC6812-0612','card_psea_02','2026-06-12T19:40:00+08:00','earn',298,7630,char(29983) || char(27963) || char(28040) || char(36153) || char(31215) || char(20998)),
('RWD-BOC6812-0601','card_psea_02','2026-06-01T09:00:00+08:00','redeem',-1200,7332,char(20817) || char(25442) || char(22320) || char(38081) || char(21048)),
('RWD-CMB3957-0530','card_psea_01','2026-05-30T09:00:00+08:00','earn',420,11521,char(26376) || char(24230) || char(27963) || char(21160) || char(31215) || char(20998));
INSERT INTO _counters (key,value) VALUES ('payment_seq',2),('line_seq',10),('dispute_seq',1),('ledger_seq',4);
COMMIT;
