-- Generated credit_card seed for central_ac_install_30d
BEGIN;
INSERT INTO cards (card_id, user_id, issuer, product_name, masked_no, type, credit_limit_minor, available_credit_minor, statement_balance_minor, unbilled_balance_minor, min_payment_due_minor, due_date, cycle_start_day, cycle_end_day, grace_period_days, status, interest_apr_bp) VALUES ('card_iscac_01', 'usr_luo_wei', '招商银行', '招行 Young 卡 (Visa)', '**** **** **** 2074', 'Visa', 3000000, 2200000, 1899900, 105600, 50000, '2026-07-08', 6, 5, 25, 'active', 1800);
INSERT INTO statements (statement_id, card_id, period_start, period_end, opening_balance_minor, new_charges_minor, payments_minor, closing_balance_minor, min_payment_due_minor, due_date, status) VALUES ('stmt_iscac', 'card_iscac_01', '2026-06-06', '2026-07-05', 0, 1899900, 0, 1899900, 50000, '2026-07-08', 'open');
INSERT INTO statement_lines (line_id, statement_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('line_iscac_1', 'stmt_iscac', '2026-06-12T19:20:05+08:00', 1899900, 'CoolMax 官方旗舰店', '5732', '家用电器', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_iscac_1', 'card_iscac_01', '2026-06-12T10:05:08+08:00', 84000, 'CoolMax 官方店', '5732', '家用电器', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_iscac_fx', 'card_iscac_01', '2026-06-13T11:30:00+08:00', 21600, 'PAYPAL US', '4814', '家用电器', 'purchase');
INSERT INTO rewards_balances (card_id, points_balance, ytd_earned, lifetime_earned, updated_at) VALUES ('card_iscac_01', 18420, 9650, 54200, '2026-06-15T00:00:00Z');
INSERT INTO rewards_ledger (ledger_id, card_id, posted_at, kind, delta, balance_after, note) VALUES ('rl_iscac_1', 'card_iscac_01', '2026-06-12T19:20:05+08:00', 'earn', 6899, 18420, '采购积分');
INSERT INTO _counters (key,value) VALUES ('payment_seq',0),('line_seq',1),('dispute_seq',0),('ledger_seq',1);
COMMIT;
