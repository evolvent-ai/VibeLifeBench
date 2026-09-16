        # visa_and_advisory env for family_rv_australia_childseat_trial

        Purpose: supports Australian entry requirements, the family visa application, the additional-documents status, and the granted closure.

        Time range and timezone: 2026-09-01 to 2026-09-27; user communication uses Asia/Shanghai, and the Australia itinerary uses Australia/Sydney.

        Key objects:

        - `VAC_LC_2026_09_AU` is initially submitted; Stage 4 becomes additional_info_required; Stage 15 becomes granted.
- `AU_VISITOR_600_SYNTH` provides the required documents and the processing time.

        Relation to task/rubric: task.py binds this env through `agent_caps_config(visa_and_advisory_mock="family_rv_australia_childseat_trial")`; the mutations in event.yaml and the rubrics reference these stable objects. The distractor data ensures the agent has to search, filter, and re-check rather than face single-line answers.

        Status and amount conventions: amounts are stored in the native fields of the corresponding server, and the budget conversion is fixed by the workspace at AUD 1 = CNY 4.80. Statuses such as pending/held/confirmed/reversed follow init.sql and later mutations.

        Loading and smoke test: init.sql in this directory runs when the server cold-starts. The key objects can be verified through the list/search/get tools of the corresponding mock server.

        Data source: all synthetic offline data, with no real personal privacy and no external network dependency.
