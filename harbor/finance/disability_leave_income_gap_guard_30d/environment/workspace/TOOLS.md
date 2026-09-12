# Tool use

Available services are banking, credit_card, brokerage, email, calendar, notion, and workspace.

- Use `user_id=usr_fin` when a tool requests a user identifier.
- Public account identifiers: `acct_checking_main`, `acct_savings_reserve`, `acct_protected`, `acct_billpay`, `card_primary`, `card_travel`, and `acct_brk_main`.
- `acct_protected` is the Medical Reserve account. A credit-card payment authorized from checking should record the card payment result and source account; do not infer success from the call alone.
- Search/list calls are investigation. A durable result requires a successful returned object and, for writes, a backend record visible on a follow-up query.
