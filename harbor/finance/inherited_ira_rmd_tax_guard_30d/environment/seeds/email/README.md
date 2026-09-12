# email env for inherited_ira_rmd_tax_guard_30d

This init.sql is task-specific and seeded from the real-data anchors in task.md.
It includes realistic distractor rows so the answer is not available from a tiny table.

Key IDs: user_id usr_fin, acct_protected, card_primary, acct_brk_main.

Task-specific source anchors:
- irs_pub590b_inherited_ira: IRS Publication 590-B covers IRA beneficiary and RMD rules. URL: https://www.irs.gov/publications/p590b

Source refresh and task-hardening notes:
- irs_pub590b_inherited_ira: IRS Publication 590-B covers IRA beneficiary and RMD rules. URL: https://www.irs.gov/publications/p590b
- irs_estimated_tax_dates: IRS estimated tax payment periods use April 15, June 15, September 15, and January 15 due dates. URL: https://www.irs.gov/faqs/estimated-tax/individuals/individuals-2
- cfpb_credit_minimum: CFPB says paying only the minimum can take years and paying more reduces interest over time. URL: https://www.consumerfinance.gov/ask-cfpb/a-box-on-my-credit-card-bill-says-that-i-will-pay-off-the-balance-in-three-years-if-i-pay-a-certain-amount-what-does-that-mean-do-i-have-to-pay-that-much-if-i-pay-that-much-and-make-new-purchases-will-i-still-owe-nothing-after-three-years-en-36/
- The environment contains distractor rows plus task-specific official-source rows; agents should query tools rather than infer answers from the prompt.
- Late mutations and source conflicts are intentional user-facing workflow events and should be reconciled in durable files.

Offline official-source cache:
- OFFICIAL_SOURCE_CACHE_V2 irs_pub590b_inherited_ira: https://www.irs.gov/publications/p590b | anchors: inherited IRA; RMD; beneficiary; 10-year rule; taxable distribution
- OFFICIAL_SOURCE_CACHE_V2 irs_estimated_tax_dates: https://www.irs.gov/faqs/estimated-tax/individuals/individuals-2 | anchors: April 15; June 15; September 15; January 15; estimated tax
- OFFICIAL_SOURCE_CACHE_V2 cfpb_credit_minimum: https://www.consumerfinance.gov/ask-cfpb/a-box-on-my-credit-card-bill-says-that-i-will-pay-off-the-balance-in-three-years-if-i-pay-a-certain-amount-what-does-that-mean-do-i-have-to-pay-that-much-if-i-pay-that-much-and-make-new-purchases-will-i-still-owe-nothing-after-three-years-en-36/ | anchors: minimum payment; 36 months; less interest; credit card
These rows were added after an official-source crawl and are frozen into init.sql so the task remains reproducible without external network access.
