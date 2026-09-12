# banking_mock — east_asia_group_trip_24d

## Key IDs

| Item | ID | Notes |
|------|----|-------|
| Li Tingaccount | `acct_li_ting_001` | balance ¥8,542（CNY 854,200 fen）|
| Chen Yuaccount | `acct_chen_yu_001` | balance ¥12,380 |
| **Wang Haoaccount** | **`acct_wang_hao_001`** | **S17_pre mutation     ** |
| Zhao Minaccount | `acct_zhao_min_001` | balance ¥15,760 |

## S17 Mutation   

```sql
-- S17_pre:   Wang Haoaccount
UPDATE accounts SET frozen=1 WHERE account_id='acct_wang_hao_001';
```

   ，agent    `transfer(from_account_id='acct_wang_hao_001', ...)`     `ACCOUNT_FROZEN`   。

## account  

| account | user_id | frozen | balance (fen) |
|------|---------|--------|-----------|
| acct_li_ting_001 | usr_li_ting | 0 | 854,200 |
| acct_chen_yu_001 | usr_chen_yu | 0 | 1,238,000 |
| acct_wang_hao_001 | usr_wang_hao | **0→1** | 621,500 |
| acct_zhao_min_001 | usr_zhao_min | 0 | 1,576,000 |

##   record  

      15    ，  ：salary  、rent/  、    、  purchase。  
   ~60    record。

## Schema（  ）

```sql
accounts(account_id, user_id, owner_name, currency, balance_minor,
         account_type, status, frozen, created_at)
transactions(tx_id, account_id, amount_minor, direction, kind,
             memo, balance_after_minor, created_at)
payees(payee_id, user_id, name, account_no, bank_name, created_at)
recurring_schedules(schedule_id, account_id, payee_id, amount_minor,
                    freq, start_date, end_date, status, created_at)
```

direction: `credit` / `debit`  
kind: `deposit` / `withdrawal` / `transfer_in` / `transfer_out` / `payment` / `fee` / `interest`
