-- Stage 19: 一笔此前冻结的可退住宿预授权释放并正式入账；铁路候补退款仍未到账。
INSERT OR REPLACE INTO transactions (tx_id, account_id, posted_at, amount_minor, kind, counterparty, memo, balance_after_minor) VALUES ('tx_card_hold_release_001', 'acct_lin_main_cny', '2026-04-23T10:55:00+08:00', 39500, 'transfer_in', '上海安静客房预授权', '可退住宿预授权释放；铁路候补退款仍待处理', 2239500);
