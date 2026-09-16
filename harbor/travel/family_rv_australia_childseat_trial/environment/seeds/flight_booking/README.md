        # flight_booking env for family_rv_australia_childseat_trial

        Purpose: supports search, booking, and pre-departure status changes for cancellable flights from Shanghai to Sydney and from Melbourne back to Shanghai.

        Time range and timezone: 2026-09-01 to 2026-09-27; user communication uses Asia/Shanghai, and the Australia itinerary uses Australia/Sydney.

        Key objects:

        - `SC888` PVG to SYD is initially 20:30; Stage 13 moves it earlier to 19:45.
- `SC889` MEL to PVG is the return flight.
- Several noise flights and fare buckets support filtering.

        Relation to task/rubric: task.py binds this env through `agent_caps_config(flight_booking_mock="family_rv_australia_childseat_trial")`; the mutations in event.yaml and the rubrics reference these stable objects. The distractor data ensures the agent has to search, filter, and re-check rather than face single-line answers.

        Status and amount conventions: amounts are stored in the native fields of the corresponding server, and the budget conversion is fixed by the workspace at AUD 1 = CNY 4.80. Statuses such as pending/held/confirmed/reversed follow init.sql and later mutations.

        Loading and smoke test: init.sql in this directory runs when the server cold-starts. The key objects can be verified through the list/search/get tools of the corresponding mock server.

        Data source: all synthetic offline data, with no real personal privacy and no external network dependency.
