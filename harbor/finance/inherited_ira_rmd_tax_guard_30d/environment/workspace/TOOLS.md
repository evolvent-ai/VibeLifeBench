# Tool use

Use banking, credit_card, brokerage, email, calendar, notion, and workspace tools. When a tool requests a user ID, use `usr_fin`.

## Evidence chain

- **banking**: query `acct_checking_main`, `acct_protected`, pending payments, and recent transactions before any cash recommendation. The account IDs are also discoverable with `list_accounts`.
- **credit_card**: query `card_primary`, its statement balance, minimum due, APR, and post-payment state. The card ID is discoverable with `list_cards`.
- **brokerage**: query `acct_brk_main`, positions, orders, and the current SGOV quote. A quote is not trade authority.
- **email**: search and read custodian, CPA, source, and mutation-released messages before relying on them.
- **calendar**: query existing CPA, custodian, card, and tax review events before creating a duplicate.
- **notion**: search the case journal and read relevant blocks as a cross-service memory aid.
- **workspace**: maintain the eight files and exact field locations published in `AGENTS.md`.

## Operating sequence

1. Query before calculating.
2. Calculate before advising.
3. Advise before executing.
4. Execute only after explicit authorization.
5. After mutation stages 5, 11, 16, and 18, re-query the named service in that stage.
6. Record failed or unavailable calls as failed or unavailable; do not replace them with guesses.
7. Keep `estimated`, `pending`, `authorized`, `executed`, `deferred`, and `forbidden` as distinct states.
