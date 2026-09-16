        # maps env for family_rv_australia_childseat_trial

        Purpose: supports right-hand-drive acclimation in Sydney, the Sydney-Canberra-Melbourne route, parking locations, and strong-wind route adjustments.

        Time range and timezone: 2026-09-01 to 2026-09-27; user communication uses Asia/Shanghai, and the Australia itinerary uses Australia/Sydney.

        Key objects:

        - `place_syd_practice` is the low-speed right-hand-drive practice location.
- `place_canberra_external_rv` is the parking recovery alternative.
- `road_evt_act_wind_rv_0918` supports splitting or postponing the strong-wind day.

        Relation to task/rubric: task.py binds this env through `agent_caps_config(maps_mock="family_rv_australia_childseat_trial")`; the mutations in event.yaml and the rubrics reference these stable objects. The distractor data ensures the agent has to search, filter, and re-check rather than face single-line answers.

        Status and amount conventions: amounts are stored in the native fields of the corresponding server, and the budget conversion is fixed by the workspace at AUD 1 = CNY 4.80. Statuses such as pending/held/confirmed/reversed follow init.sql and later mutations.

        Loading and smoke test: init.sql in this directory runs when the server cold-starts. The key objects can be verified through the list/search/get tools of the corresponding mock server.

        Data source: all synthetic offline data, with no real personal privacy and no external network dependency.
