-- Generated credit_card seed for bathroom_reno_30d
BEGIN;
INSERT INTO cards (card_id, user_id, issuer, product_name, masked_no, type, credit_limit_minor, available_credit_minor, statement_balance_minor, unbilled_balance_minor, min_payment_due_minor, due_date, cycle_start_day, cycle_end_day, grace_period_days, status, interest_apr_bp) VALUES ('card_r2bth_01', 'usr_gan_mei', 'China Merchants Bank', 'CMB Young Card (Visa)', '**** **** **** 3729', 'Visa', 3000000, 2200000, 2200000, 105600, 50000, '2026-07-08', 6, 5, 25, 'active', 1800);
INSERT INTO statements (statement_id, card_id, period_start, period_end, opening_balance_minor, new_charges_minor, payments_minor, closing_balance_minor, min_payment_due_minor, due_date, status) VALUES ('stmt_r2bth', 'card_r2bth_01', '2026-06-06', '2026-07-05', 0, 2200000, 0, 2200000, 50000, '2026-07-08', 'open');
INSERT INTO statement_lines (line_id, statement_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('line_r2bth_1', 'stmt_r2bth', '2026-06-15T19:20:05+08:00', 2200000, 'AquaSeal Official Flagship Store', '5732', 'Home renovation supervision', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_r2bth_1', 'card_r2bth_01', '2026-06-15T10:05:08+08:00', 84000, 'AquaSeal Official Store', '5732', 'Home renovation supervision', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_r2bth_fx', 'card_r2bth_01', '2026-06-15T11:30:00+08:00', 21600, 'PAYPAL US', '4814', 'Home renovation supervision', 'purchase');
INSERT INTO rewards_balances (card_id, points_balance, ytd_earned, lifetime_earned, updated_at) VALUES ('card_r2bth_01', 18420, 9650, 54200, '2026-06-15T00:00:00Z');
INSERT INTO rewards_ledger (ledger_id, card_id, posted_at, kind, delta, balance_after, note) VALUES ('rl_r2bth_1', 'card_r2bth_01', '2026-06-15T19:20:05+08:00', 'earn', 6899, 18420, 'Purchase points');
INSERT INTO _counters (key,value) VALUES ('payment_seq',0),('line_seq',1),('dispute_seq',0),('ledger_seq',1);

-- HANDBOOK_REMEDIATION_V113_credit_card
DELETE FROM unbilled_transactions WHERE tx_id NOT IN ('tx_r2bth_fx');
INSERT OR IGNORE INTO cards VALUES ('card_r2bth_02','usr_gan_mei','China Merchants Bank','Backup UnionPay card','**** 8842','UnionPay',6000000,5750000,125000,25000,12500,'2026-07-12',5,4,15,'active',1650);
INSERT OR IGNORE INTO statements VALUES
 ('stmt_r2bth_02','card_r2bth_02','2026-05-05','2026-06-04',0,125000,0,125000,12500,'2026-06-19','paid');
INSERT OR IGNORE INTO statement_lines(line_id,statement_id,posted_at,amount_minor,merchant_name,mcc,category,kind) VALUES
 ('ln_material_0518_a4k2','stmt_r2bth','2026-05-18T10:00:00+08:00',46800,'Xuhui building-materials warehouse','5211','Waterproofing materials','purchase'),
 ('ln_material_0520_n7c5','stmt_r2bth','2026-05-20T10:00:00+08:00',46800,'Xuhui building-materials warehouse','5211','Waterproofing materials','purchase'),
 ('ln_fixture_0528_p3m8','stmt_r2bth','2026-05-28T14:20:00+08:00',26700,'Official marketplace','5712','Bathroom materials','purchase'),
 ('ln_changeauth_0601_v6r1','stmt_r2bth','2026-06-01T09:00:00+08:00',98000,'Anlan Bathroom change-order preauthorization','1799','Renovation service','purchase'),
 ('ln_authrelease_0602_h9d4','stmt_r2bth','2026-06-02T11:00:00+08:00',-98000,'Anlan Bathroom preauthorization cancellation','1799','Renovation service','adjustment'),
 ('ln_property_0512_t5q7','stmt_r2bth_02','2026-05-12T08:00:00+08:00',32000,'Property-management renovation registration','9399','Property-management service','purchase'),
 ('ln_inspection_0522_c8w3','stmt_r2bth_02','2026-05-22T09:00:00+08:00',68000,'Heng''an quality inspection','8999','Quality inspection service','purchase'),
 ('ln_freight_0530_k2p6','stmt_r2bth_02','2026-05-30T12:00:00+08:00',25000,'Urban delivery logistics','4215','Material transportation','purchase'),
 ('ln_autopay_0603_m4x9','stmt_r2bth_02','2026-06-03T18:00:00+08:00',-125000,'Automatic repayment','6012','Repayment','payment');
INSERT OR IGNORE INTO unbilled_transactions VALUES
 ('tx_r2bth_material','card_r2bth_01','2026-06-15T10:30:00+08:00',93600,'Xuhui building-materials warehouse','5211','Waterproofing materials','purchase'),
 ('tx_r2bth_inspect','card_r2bth_01','2026-06-15T14:00:00+08:00',68000,'Heng''an quality inspection','8999','Quality inspection service','purchase'),
 ('tx_r2bth_property','card_r2bth_02','2026-06-15T15:00:00+08:00',30000,'Property-management renovation deposit','9399','Property-management service','purchase'),
 ('tx_r2bth_logistics','card_r2bth_02','2026-06-15T16:00:00+08:00',22000,'Urban delivery logistics','4215','Material transportation','purchase');
INSERT OR IGNORE INTO disputes VALUES ('DSP-260510-R2N6P','card_r2bth_02','TX-260509-R2C7V','Duplicate charge for a previous delivery fee','approved','2026-05-10T09:00:00+08:00','2026-05-18','2026-05-15T16:00:00+08:00');

COMMIT;

-- REMEDIATION_20260730_RENOVATION_CARD_CONTEXT
BEGIN;
UPDATE unbilled_transactions SET amount_minor=22800, merchant_name='Huju Engineering Cloud Archive', mcc='7399', category='Project documentation service' WHERE tx_id='tx_r2bth_fx';
COMMIT;
