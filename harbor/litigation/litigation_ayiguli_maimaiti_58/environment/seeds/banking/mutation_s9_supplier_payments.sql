INSERT OR IGNORE INTO transactions
  (tx_id, account_id, posted_at, amount_minor, kind, counterparty, memo, balance_after_minor)
VALUES
  ('tx_aygul_pay_0710_32000', 'acct_aygul_store_mercury', '2026-07-10T10:10:00+08:00', -(32000 * 100), 'payment', 'evidence record', '5evidence record；evidence record', ((166001 * 100) + 50));
INSERT OR IGNORE INTO transactions
  (tx_id, account_id, posted_at, amount_minor, kind, counterparty, memo, balance_after_minor)
VALUES
  ('tx_aygul_pay_0711_15000', 'acct_aygul_store_mercury', '2026-07-11T09:25:00+08:00', -(15000 * 100), 'payment', 'evidence record', '7evidence record；evidence record', ((151001 * 100) + 50));
UPDATE accounts
SET balance_minor=((151001 * 100) + 50)
WHERE account_id='acct_aygul_store_mercury';
