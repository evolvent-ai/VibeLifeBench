-- Generated credit_card seed for beauty_prepaid_rights_30d
BEGIN;
INSERT INTO cards (card_id, user_id, issuer, product_name, masked_no, type, credit_limit_minor, available_credit_minor, statement_balance_minor, unbilled_balance_minor, min_payment_due_minor, due_date, cycle_start_day, cycle_end_day, grace_period_days, status, interest_apr_bp) VALUES ('card_ppbeauty_01', 'usr_shen_e', 'China Merchants Bank', 'China Merchants Bank Young additional local detail (Visa)', '**** **** **** 4963', 'Visa', 3000000, 1019200, 1880000, 100800, 50000, '2026-07-10', 6, 5, 25, 'active', 1800);
INSERT INTO statements (statement_id, card_id, period_start, period_end, opening_balance_minor, new_charges_minor, payments_minor, closing_balance_minor, min_payment_due_minor, due_date, status) VALUES ('stmt_ppbeauty', 'card_ppbeauty_01', '2026-06-06', '2026-07-05', 0, 1880000, 0, 1880000, 50000, '2026-07-10', 'open');
INSERT INTO statement_lines (line_id, statement_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('line_ppbeauty_1', 'stmt_ppbeauty', '2026-06-15T19:20:05+08:00', 1880000, 'GlowSpa official flagship store', '5732', 'beauty service', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_ppbeauty_1', 'card_ppbeauty_01', '2026-06-15T10:05:08+08:00', 84000, 'GlowSpa official store', '5732', 'beauty service', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_ppbeauty_fx', 'card_ppbeauty_01', '2026-06-15T11:30:00+08:00', 16800, 'PAYPAL US', '4814', 'beauty service', 'purchase');
INSERT INTO rewards_balances (card_id, points_balance, ytd_earned, lifetime_earned, updated_at) VALUES ('card_ppbeauty_01', 18420, 9650, 54200, '2026-06-15T00:00:00Z');
INSERT INTO rewards_ledger (ledger_id, card_id, posted_at, kind, delta, balance_after, note) VALUES ('rl_ppbeauty_1', 'card_ppbeauty_01', '2026-06-15T19:20:05+08:00', 'earn', 6899, 18420, 'purchase points');
INSERT INTO _counters (key,value) VALUES ('payment_seq',0),('line_seq',1),('dispute_seq',0),('ledger_seq',1);
COMMIT;

-- Curated paid-statement history: ordinary household spending distinct from the active GlowSpa and PayPal transactions.
BEGIN;
INSERT INTO statements (statement_id,card_id,period_start,period_end,opening_balance_minor,new_charges_minor,payments_minor,closing_balance_minor,min_payment_due_minor,due_date,status) VALUES
('stmt_beauty_winter_cedar','card_ppbeauty_01','2026-01-06','2026-02-05',0,19049,19049,0,0,'2026-02-08','paid'),
('stmt_beauty_spring_maple','card_ppbeauty_01','2026-02-06','2026-03-05',0,25600,25600,0,0,'2026-03-08','paid'),
('stmt_beauty_march_willow','card_ppbeauty_01','2026-03-06','2026-04-05',0,19415,19415,0,0,'2026-04-08','paid'),
('stmt_beauty_april_lotus','card_ppbeauty_01','2026-04-06','2026-05-05',0,17585,17585,0,0,'2026-05-08','paid'),
('stmt_beauty_may_orchid','card_ppbeauty_01','2026-05-06','2026-06-05',0,14665,14665,0,0,'2026-06-08','paid');
INSERT INTO statement_lines (line_id,statement_id,posted_at,amount_minor,merchant_name,mcc,category,kind) VALUES
('line_beauty_cedar_market','stmt_beauty_winter_cedar','2026-01-09T18:26:00+08:00',1580,'additional local detailsupermarket','5411','household goods','purchase'),
('line_beauty_cedar_transit','stmt_beauty_winter_cedar','2026-01-13T08:11:00+08:00',2690,'Hangzhouadditional local detail','4111','public transit','purchase'),
('line_beauty_cedar_books','stmt_beauty_winter_cedar','2026-01-18T15:42:00+08:00',4200,'additional local detail','5942','additional local detail','purchase'),
('line_beauty_cedar_coffee','stmt_beauty_winter_cedar','2026-01-22T10:17:00+08:00',1299,'additional local detail','5814','dining','purchase'),
('line_beauty_cedar_power','stmt_beauty_winter_cedar','2026-01-27T07:50:00+08:00',8600,'additional local detail','4900','utilities','purchase'),
('line_beauty_cedar_bike','stmt_beauty_winter_cedar','2026-01-31T17:33:00+08:00',450,'additional local detail','4121','additional local detail','purchase'),
('line_beauty_cedar_pharmacy','stmt_beauty_winter_cedar','2026-02-02T19:05:00+08:00',3210,'additional local detail','5912','additional local detail','purchase'),
('line_beauty_cedar_refund','stmt_beauty_winter_cedar','2026-02-04T13:28:00+08:00',-2980,'additional local detailrefund','5411','fresh groceries','refund'),
('line_beauty_maple_fuel','stmt_beauty_spring_maple','2026-02-08T12:15:00+08:00',2280,'additional local detailRoadStation','5541','additional local detailservice','purchase'),
('line_beauty_maple_grocery','stmt_beauty_spring_maple','2026-02-12T18:49:00+08:00',5600,'additional local detail','5411','household goods','purchase'),
('line_beauty_maple_lunch','stmt_beauty_spring_maple','2026-02-16T12:22:00+08:00',1890,'additional local detailRoadadditional local detail','5812','dining','purchase'),
('line_beauty_maple_parking','stmt_beauty_spring_maple','2026-02-19T20:06:00+08:00',760,'additional local detail','7523','parking service','purchase'),
('line_beauty_maple_insurance','stmt_beauty_spring_maple','2026-02-23T09:31:00+08:00',12600,'additional local detailinsuranceservice','6300','insuranceadditional local detail','purchase'),
('line_beauty_maple_stationery','stmt_beauty_spring_maple','2026-02-27T16:44:00+08:00',3280,'additional local detail','5943','additional local detail','purchase'),
('line_beauty_maple_movie','stmt_beauty_spring_maple','2026-03-01T19:18:00+08:00',990,'additional local detailcenter','7832','additional local detail','purchase'),
('line_beauty_maple_refund','stmt_beauty_spring_maple','2026-03-04T11:05:00+08:00',-1800,'additional local detailRoadadditional local detail','4112','intercity transit','refund'),
('line_beauty_willow_water','stmt_beauty_march_willow','2026-03-08T07:42:00+08:00',3100,'Hangzhouadditional local detail','4900','utilities','purchase'),
('line_beauty_willow_breakfast','stmt_beauty_march_willow','2026-03-11T08:36:00+08:00',845,'additional local detail','5812','dining','purchase'),
('line_beauty_willow_household','stmt_beauty_march_willow','2026-03-15T16:55:00+08:00',6800,'additional local detail','5311','additional local detail','purchase'),
('line_beauty_willow_mobile','stmt_beauty_march_willow','2026-03-20T09:10:00+08:00',2450,'Zhejiang Mobile','4814','additional local detailservice','purchase'),
('line_beauty_willow_fruit','stmt_beauty_march_willow','2026-03-24T18:12:00+08:00',1120,'additional local detailRoadadditional local detail','5499','fresh groceries','purchase'),
('line_beauty_willow_cleaning','stmt_beauty_march_willow','2026-03-28T14:37:00+08:00',3990,'additional local detailservice','7349','familyservice','purchase'),
('line_beauty_willow_museum','stmt_beauty_march_willow','2026-04-01T10:28:00+08:00',1760,'additional local detail','5947','additional local detail','purchase'),
('line_beauty_willow_adjust','stmt_beauty_march_willow','2026-04-04T15:49:00+08:00',-650,'additional local detail','7523','parking service','adjustment'),
('line_beauty_lotus_dental','stmt_beauty_april_lotus','2026-04-08T10:15:00+08:00',4600,'additional local detail','8021','additional local detail','purchase'),
('line_beauty_lotus_flower','stmt_beauty_april_lotus','2026-04-12T17:26:00+08:00',1380,'additional local detail','5992','additional local detail','purchase'),
('line_beauty_lotus_bus','stmt_beauty_april_lotus','2026-04-16T08:04:00+08:00',925,'Hangzhouadditional local detail','4111','public transit','purchase'),
('line_beauty_lotus_course','stmt_beauty_april_lotus','2026-04-20T20:11:00+08:00',7200,'additional local detail','8299','education and training','purchase'),
('line_beauty_lotus_pet','stmt_beauty_april_lotus','2026-04-24T12:39:00+08:00',2660,'additional local detailpet suppliesadditional local detail','5995','pet supplies','purchase'),
('line_beauty_lotus_laundry','stmt_beauty_april_lotus','2026-04-28T19:03:00+08:00',1540,'additional local detail','7210','additional local detailservice','purchase'),
('line_beauty_lotus_cloud','stmt_beauty_april_lotus','2026-05-02T09:24:00+08:00',480,'additional local detail','7372','additional local detailservice','purchase'),
('line_beauty_lotus_refund','stmt_beauty_april_lotus','2026-05-04T16:18:00+08:00',-1200,'pet suppliesadditional local detail','5995','pet supplies','refund'),
('line_beauty_orchid_gas','stmt_beauty_may_orchid','2026-05-08T07:58:00+08:00',1980,'Hangzhouadditional local detail','4900','utilities','purchase'),
('line_beauty_orchid_album','stmt_beauty_may_orchid','2026-05-12T14:46:00+08:00',3500,'additional local detail','7221','additional local detail','purchase'),
('line_beauty_orchid_noodle','stmt_beauty_may_orchid','2026-05-16T12:08:00+08:00',785,'additional local detail','5812','dining','purchase'),
('line_beauty_orchid_donation','stmt_beauty_may_orchid','2026-05-20T08:32:00+08:00',1560,'additional local detail','8398','charityadditional local detail','purchase'),
('line_beauty_orchid_repair','stmt_beauty_may_orchid','2026-05-24T15:54:00+08:00',4300,'additional local detailservice','7629','additional local detail','purchase'),
('line_beauty_orchid_train','stmt_beauty_may_orchid','2026-05-28T06:41:00+08:00',2880,'additional local detailRoadadditional local detail','4112','intercity transit','purchase'),
('line_beauty_orchid_snack','stmt_beauty_may_orchid','2026-06-01T18:17:00+08:00',640,'additional local detail','5411','additional local detail','purchase'),
('line_beauty_orchid_credit','stmt_beauty_may_orchid','2026-06-04T10:22:00+08:00',-980,'courseadditional local detailrefund','8299','education and training','refund');
INSERT INTO payments (payment_id,card_id,posted_at,amount_minor,source_hint,applied_to_statement_minor,applied_to_unbilled_minor) VALUES
('pay_beauty_cedar_first','card_ppbeauty_01','2026-02-06T08:25:00+08:00',10000,'China Merchants Bank debit card ending 1846',10000,0),
('pay_beauty_cedar_close','card_ppbeauty_01','2026-02-07T19:41:00+08:00',9049,'additional local detailbalanceadditional local detail',9049,0),
('pay_beauty_maple_first','card_ppbeauty_01','2026-03-06T09:06:00+08:00',12000,'China Merchants Bank debit card ending 1846',12000,0),
('pay_beauty_maple_close','card_ppbeauty_01','2026-03-07T18:22:00+08:00',13600,'salary-card autopay',13600,0),
('pay_beauty_willow_first','card_ppbeauty_01','2026-04-06T07:53:00+08:00',9415,'additional local detailbalanceadditional local detail',9415,0),
('pay_beauty_willow_close','card_ppbeauty_01','2026-04-07T20:16:00+08:00',10000,'China Merchants Bank debit card ending 1846',10000,0),
('pay_beauty_lotus_first','card_ppbeauty_01','2026-05-06T08:44:00+08:00',7585,'salary-card autopay',7585,0),
('pay_beauty_lotus_close','card_ppbeauty_01','2026-05-07T16:28:00+08:00',10000,'China Merchants Bank debit card ending 1846',10000,0),
('pay_beauty_orchid_first','card_ppbeauty_01','2026-06-06T09:17:00+08:00',6665,'additional local detailbalanceadditional local detail',6665,0),
('pay_beauty_orchid_close','card_ppbeauty_01','2026-06-07T21:03:00+08:00',8000,'China Merchants Bank debit card ending 1846',8000,0);
INSERT INTO rewards_ledger (ledger_id,card_id,posted_at,kind,delta,balance_after,note) VALUES
('reward_beauty_water','card_ppbeauty_01','2026-01-09T18:27:00+08:00','earn',16,11120,'additional local detailsupermarketadditional local detail'),
('reward_beauty_transit','card_ppbeauty_01','2026-01-13T08:12:00+08:00','earn',27,11147,'additional local detail'),
('reward_beauty_books','card_ppbeauty_01','2026-01-18T15:43:00+08:00','earn',42,11189,'additional local detail'),
('reward_beauty_power','card_ppbeauty_01','2026-01-27T07:51:00+08:00','earn',86,11275,'utilitiesadditional local detail'),
('reward_beauty_pharmacy','card_ppbeauty_01','2026-02-02T19:06:00+08:00','earn',32,11307,'additional local detail'),
('reward_beauty_grocery','card_ppbeauty_01','2026-02-12T18:50:00+08:00','earn',56,11363,'additional local detail'),
('reward_beauty_insurance','card_ppbeauty_01','2026-02-23T09:32:00+08:00','earn',126,11489,'insuranceadditional local detail'),
('reward_beauty_stationery','card_ppbeauty_01','2026-02-27T16:45:00+08:00','earn',33,11522,'additional local detailpurchase points'),
('reward_beauty_waterbill','card_ppbeauty_01','2026-03-08T07:43:00+08:00','earn',31,11553,'additional local detail'),
('reward_beauty_household','card_ppbeauty_01','2026-03-15T16:56:00+08:00','earn',68,11621,'additional local detail'),
('reward_beauty_mobile','card_ppbeauty_01','2026-03-20T09:11:00+08:00','earn',25,11646,'additional local detail'),
('reward_beauty_cleaning','card_ppbeauty_01','2026-03-28T14:38:00+08:00','earn',40,11686,'additional local detailserviceadditional local detail'),
('reward_beauty_dental','card_ppbeauty_01','2026-04-08T10:16:00+08:00','earn',46,11732,'additional local detail'),
('reward_beauty_course','card_ppbeauty_01','2026-04-20T20:12:00+08:00','earn',72,11804,'additional local detailcourseadditional local detail'),
('reward_beauty_pet','card_ppbeauty_01','2026-04-24T12:40:00+08:00','earn',27,11831,'pet suppliesadditional local detail'),
('reward_beauty_cloud','card_ppbeauty_01','2026-05-02T09:25:00+08:00','earn',5,11836,'additional local detail'),
('reward_beauty_gas','card_ppbeauty_01','2026-05-08T07:59:00+08:00','earn',20,11856,'additional local detail'),
('reward_beauty_album','card_ppbeauty_01','2026-05-12T14:47:00+08:00','earn',35,11891,'photo albumadditional local detail'),
('reward_beauty_donation','card_ppbeauty_01','2026-05-20T08:33:00+08:00','earn',16,11907,'charityadditional local detail'),
('reward_beauty_repair','card_ppbeauty_01','2026-05-24T15:55:00+08:00','earn',43,11950,'additional local detailserviceadditional local detail'),
('reward_beauty_train','card_ppbeauty_01','2026-05-28T06:42:00+08:00','earn',29,11979,'additional local detailRoadadditional local detail'),
('reward_beauty_market_reversal','card_ppbeauty_01','2026-02-04T13:29:00+08:00','adjust',-30,11949,'additional local detailrefundadditional local detail'),
('reward_beauty_pet_reversal','card_ppbeauty_01','2026-05-04T16:19:00+08:00','adjust',-12,11937,'pet suppliesrefundadditional local detail'),
('reward_beauty_expire_notice','card_ppbeauty_01','2026-05-31T23:10:00+08:00','expire',-120,11817,'additional local detailyearadditional local detail'),
('reward_beauty_bonus','card_ppbeauty_01','2026-06-05T11:30:00+08:00','adjust',80,11897,'monthadditional local detail');
UPDATE _counters SET value=50 WHERE key='line_seq';
UPDATE _counters SET value=10 WHERE key='payment_seq';
UPDATE _counters SET value=26 WHERE key='ledger_seq';
COMMIT;
