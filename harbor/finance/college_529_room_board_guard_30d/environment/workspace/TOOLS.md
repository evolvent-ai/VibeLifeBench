# Tool Use

Available services cover banking, brokerage, credit cards, email, calendar, Notion, and workspace files. Use `usr_fin` where a finance endpoint asks for `user_id`. Reads are for verification; writes require a valid business reason and the current user authorization. After a write, re-read the affected object and record the result.
