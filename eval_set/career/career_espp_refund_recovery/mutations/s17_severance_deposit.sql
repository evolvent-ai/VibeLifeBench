-- s17: 公司按单方低价方案支付 200300 元；公允价值对账为 297300 元，差额 97000 元。
-- 使用临时 marker + 显式事务保证首次执行原子落库，重复执行不重复增加余额。
BEGIN IMMEDIATE;
CREATE TEMP TABLE IF NOT EXISTS _s17_apply(flag INTEGER NOT NULL);
DELETE FROM _s17_apply;
INSERT INTO _s17_apply(flag)
SELECT 1 WHERE NOT EXISTS (
  SELECT 1 FROM transactions WHERE tx_id='tx_gk_severance'
);
INSERT INTO transactions
  (tx_id, account_id, posted_at, amount_minor, kind, counterparty, memo, balance_after_minor)
SELECT 'tx_gk_severance', 'acct_gk_checking', '2026-07-16T08:00:00Z', 20030000, 'deposit',
       '矽鸣半导体技术(上海)有限公司', '持股计划赎回款(公司方案)',
       (SELECT balance_minor FROM accounts WHERE account_id='acct_gk_checking') + 20030000
FROM _s17_apply;
UPDATE accounts
SET balance_minor = balance_minor + 20030000
WHERE account_id='acct_gk_checking' AND EXISTS (SELECT 1 FROM _s17_apply);
UPDATE _counters
SET value = (SELECT COUNT(*) FROM transactions)
WHERE key='tx_seq' AND EXISTS (SELECT 1 FROM _s17_apply);
DROP TABLE _s17_apply;
COMMIT;
