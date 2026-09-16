        # credit_card env for family_rv_australia_childseat_trial

        Purpose: supports card benefit exclusions, the AUD 600 motorhome deposit, the duplicate pending authorization, and reversal reconciliation.

        Time range and timezone: 2026-09-01 to 2026-09-27; user communication uses Asia/Shanghai, and the Australia itinerary uses Australia/Sydney.

        Key objects:

        - `card_world_travel_plus_2609` is the user travel card.
- `txn_sc_hold_0920_a` is the normal AUD 600 hold.
- `txn_sc_hold_dup_0920_b` is the duplicate hold; Stage 22 inserts the reversal.

        Relation to task/rubric: task.py binds this env through `agent_caps_config(credit_card_mock="family_rv_australia_childseat_trial")`; the mutations in event.yaml and the rubrics reference these stable objects. The distractor data ensures the agent has to search, filter, and re-check rather than face single-line answers.

        Status and amount conventions: amounts are stored in the native fields of the corresponding server, and the budget conversion is fixed by the workspace at AUD 1 = CNY 4.80. Statuses such as pending/held/confirmed/reversed follow init.sql and later mutations.

        Loading and smoke test: init.sql in this directory runs when the server cold-starts. The key objects can be verified through the list/search/get tools of the corresponding mock server.

        Data source: all synthetic offline data, with no real personal privacy and no external network dependency.
