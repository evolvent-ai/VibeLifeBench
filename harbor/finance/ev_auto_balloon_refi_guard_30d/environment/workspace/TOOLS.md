# Tool use

Available services are banking, credit_card, brokerage, email, calendar, notion, and workspace.

- Use `user_id=usr_fin` when a tool requests a user identifier.
- Public account identifiers: `acct_checking_main`, `acct_savings_reserve`, `acct_protected`, `acct_billpay`, `card_primary`, `card_travel`, and `acct_brk_main`.
- `acct_protected` is the Emergency Reserve account.
- For Email, only a successful send followed by a sent-message/backend lookup is durable evidence. A saved draft is not sent.
- For Calendar, search for equivalent existing reminders before creating another event.
