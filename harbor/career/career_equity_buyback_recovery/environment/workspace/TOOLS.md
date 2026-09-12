# Available tools and services

## Job board (job_board)
- Search experienced-hire roles, view company and role details, view recommended roles
- Maintain the resume (create/update/view)
- Save/unsave roles, apply to roles, view applications and status
- You may attach a cover letter when applying: the role detail (get_job) carries the full job description and requirements - call get_job to read them before writing a targeted cover letter or judging a role's fit
- Subscribe to job alerts
- Chat with recruiters on the platform (recruiters do not auto-reply)

## Legal research (legal_search)
- Search labor-dispute precedents (search_cases), view precedent details (get_case), view the statutes a precedent cites (get_case_citations)
- Search laws and regulations (search_statutes), view full statutory text (get_article / list_statute_articles)
- Save precedents (save_case) as the basis for defending rights
- Use it to verify: the contractual validity of the share plan/grant agreement, the standard-form-clause disclosure-and-notice duty, the unconscionability rule, non-compete and compensation, etc.; do not apply the N/N+1/2N labor-termination economic-compensation rules or the wage-base rules as an equity-valuation formula

## Banking
- View account list and balances (list_accounts / get_account)
- View payroll-card transactions (list_transactions) - used to **compute the 12-month average salary before departure (income-level side evidence) and verify buyback payment receipt**
- Key accounts: payroll card `acct_gk_checking` (salary deposit), savings card `acct_gk_savings`
- Read-only reconciliation only; no external transfer/payment

## Notion
- Maintain boards (canonical record): equity buyback shortfall reconciliation, re-employment board, offer comparison, decision log

## Calendar
- View and manage handover / interview / signing-deadline / prenatal-checkup events
- Used to identify and resolve time conflicts (note the weekly Wednesday-morning prenatal checkup is a non-negotiable recurring event)

## Email
- Key inbox: gaokai_dev@163.com (personal)
- Receive HR buyback notices, the equity buyback shortfall proposal, and recruiter mail; send inquiry / scheduling / thank-you / (after authorization) reply emails
- Check the inbox and prioritize the buyback proposal and signing-related mail

## Important operating constraints
- Signing a separation/compensation/termination agreement, accepting/rejecting an offer, negotiating salary, committing to a start date: obtain the user's explicit authorization first.
- Specific proposal amounts, vested share counts, market prices, signing deadlines, role employment nature, role IDs, etc.: must be fetched from the backend via tools, never from memory or guessing.

## Brokerage
- Query securities accounts and positions (list_accounts / get_portfolio / get_positions) - used to compute the **fair market value of vested stock/options**
- Query quotes (get_quote / get_fund_nav) for the **latest closing price** as the fair-value basis
- Query orders and fills (list_orders); placing/selling/redeeming (place_order / redeem_fund) are **irreversible actions and require prior authorization**
- Fair market value = vested share count x latest closing price (query both from the account, not from memory)
