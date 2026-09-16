        # hotel_booking env for family_rv_australia_childseat_trial

        Purpose: supports a late-arrival family room in Sydney, the Canberra motorhome parking recovery, and archiving the Melbourne stay before the return flight.

        Time range and timezone: 2026-09-01 to 2026-09-27; user communication uses Asia/Shanghai, and the Australia itinerary uses Australia/Sydney.

        Key objects:

        - `sydharbr` is a cancellable Sydney family room with late arrival.
- `cbrlake` initially has a 3.2m outdoor space; Stage 10 changes it to a 2.1m underground garage.
- `cbrmotor` is the recoverable substitute hotel.

        Relation to task/rubric: task.py binds this env through `agent_caps_config(hotel_booking_mock="family_rv_australia_childseat_trial")`; the mutations in event.yaml and the rubrics reference these stable objects. The distractor data ensures the agent has to search, filter, and re-check rather than face single-line answers.

        Status and amount conventions: amounts are stored in the native fields of the corresponding server, and the budget conversion is fixed by the workspace at AUD 1 = CNY 4.80. Statuses such as pending/held/confirmed/reversed follow init.sql and later mutations.

        Loading and smoke test: init.sql in this directory runs when the server cold-starts. The key objects can be verified through the list/search/get tools of the corresponding mock server.

        Data source: all synthetic offline data, with no real personal privacy and no external network dependency.
