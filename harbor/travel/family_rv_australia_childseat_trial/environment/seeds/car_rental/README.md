        # car_rental env for family_rv_australia_childseat_trial

        Purpose: supports Australian motorhome offers, child restraints, insurance, road policies, one-way return, and deposit/return requirements.

        Time range and timezone: 2026-09-01 to 2026-09-27; user communication uses Asia/Shanghai, and the Australia itinerary uses Australia/Sydney.

        Key objects:

        - `CRO_SC4B_260915` is the compliant, cancellable SouthernCross 4B offer.
- `CRO_TASMAN_SAVER_260915` is the non-refundable bait offer with an uncertain restraint.
- `INS_FULL_PLUS` gains the strong-wind awning exclusion addendum at Stage 12.
- `road_policy_child_restraint` provides the child restraint rule for age 4.

        Relation to task/rubric: task.py binds this env through `agent_caps_config(car_rental_mock="family_rv_australia_childseat_trial")`; the mutations in event.yaml and the rubrics reference these stable objects. The distractor data ensures the agent has to search, filter, and re-check rather than face single-line answers.

        Status and amount conventions: amounts are stored in the native fields of the corresponding server, and the budget conversion is fixed by the workspace at AUD 1 = CNY 4.80. Statuses such as pending/held/confirmed/reversed follow init.sql and later mutations.

        Loading and smoke test: init.sql in this directory runs when the server cold-starts. The key objects can be verified through the list/search/get tools of the corresponding mock server.

        Data source: all synthetic offline data, with no real personal privacy and no external network dependency.
