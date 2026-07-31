-- Generated credit_card seed for baby_stroller_safety_standard_30d
BEGIN;
INSERT INTO cards (card_id, user_id, issuer, product_name, masked_no, type, credit_limit_minor, available_credit_minor, statement_balance_minor, unbilled_balance_minor, min_payment_due_minor, due_date, cycle_start_day, cycle_end_day, grace_period_days, status, interest_apr_bp) VALUES ('card_strr_01', 'usr_yan_ting', '招商银行', '招行 Young 卡 (Visa)', '**** **** **** 6693', 'Visa', 3000000, 2200000, 269900, 115400, 50000, '2026-07-08', 6, 5, 25, 'active', 1800);
INSERT INTO statements (statement_id, card_id, period_start, period_end, opening_balance_minor, new_charges_minor, payments_minor, closing_balance_minor, min_payment_due_minor, due_date, status) VALUES ('stmt_strr', 'card_strr_01', '2026-06-06', '2026-07-05', 0, 269900, 0, 269900, 50000, '2026-07-08', 'open');
INSERT INTO statement_lines (line_id, statement_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('line_strr_1', 'stmt_strr', '2026-06-12T19:20:05+08:00', 269900, 'GlideBaby 官方旗舰店', '5732', '母婴用品', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_strr_1', 'card_strr_01', '2026-06-12T10:05:08+08:00', 89600, 'GlideBaby 官方店', '5732', '母婴电器', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_strr_fx', 'card_strr_01', '2026-06-13T11:30:00+08:00', 25800, 'BABYJOGGER US', '4814', '母婴用品', 'purchase');
INSERT INTO rewards_balances (card_id, points_balance, ytd_earned, lifetime_earned, updated_at) VALUES ('card_strr_01', 18420, 9650, 54200, '2026-06-15T00:00:00Z');
INSERT INTO rewards_ledger (ledger_id, card_id, posted_at, kind, delta, balance_after, note) VALUES ('rl_strr_1', 'card_strr_01', '2026-06-12T19:20:05+08:00', 'earn', 6899, 18420, '采购积分');
INSERT INTO _counters (key,value) VALUES ('payment_seq',0),('line_seq',1),('dispute_seq',0),('ledger_seq',1);
COMMIT;
