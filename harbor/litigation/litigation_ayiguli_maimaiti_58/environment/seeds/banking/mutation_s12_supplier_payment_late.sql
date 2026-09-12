INSERT OR IGNORE INTO transactions
  (tx_id, account_id, posted_at, amount_minor, kind, counterparty, memo, balance_after_minor)
VALUES
  ('tx_aygul_pay_0723_28000', 'acct_aygul_store_mercury', '2026-07-23T14:35:00+08:00', -(28000 * 100), 'payment', 'evidence record', '6evidence record；evidence record，evidence record', ((123001 * 100) + 50));
UPDATE accounts
SET balance_minor=((123001 * 100) + 50)
WHERE account_id='acct_aygul_store_mercury';
