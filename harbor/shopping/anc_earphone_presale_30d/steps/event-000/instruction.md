[2026-06-15T09:00:00+08:00] Message from Tessa Teng

I need to get three related matters under control, and they are becoming difficult to track:

1. The final payable price and deposit bonus for the prepaid SonicPod Max ANC earphone presale order `ord_psea_0001` do not reconcile. I need the presale price and verification code checked.
2. The final-payment window for SonicPod Max ANC earphone presale order `ord_psea_0002` is approaching, but the deposit bonus and threshold discount do not reconcile. I need an evidence-based review.
3. The price-protection refund, deposit deduction, secondhand listing, and marketplace payout must be reconciled under separate accounting categories, with continued tracking of `lst_psea_0001`.

First review the workspace and the current state of each system. Set up a durable tracking framework that keeps these three workstreams separate.

Use the workspace's durable record field names consistently: `thread_id`, `current_status`, `next_action`, `source_refs`, `authorization_state`, `last_verified_stage`, and `first_seen_stage`. Decision option rows use `option_id`, `amount_minor`, `cycle_days`, and `evidence_basis`; budget rows use `line_id`; evidence rows use `evidence_status`; the heartbeat uses `due_at`. Keep these as labels only and obtain all IDs, amounts, and dates from the systems or the user's messages.
