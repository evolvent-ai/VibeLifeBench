# calendar env for rental_seed_013_task

Scenario purpose: support the “cross-city onboarding short-term rental to long-term rental dual-track housing” task, covering 2026-08-03 to 2026-09-06, in the Asia/Shanghai time zone. Key object IDs include short_101/102/103, long_201-205, onboard_pm_001, office_a_nanshan, office_b_bantian, shipment_cd_sz_001.

Relationship to task/rubric: this env provides the offline facts that the agent needs to query, filter, restore, and finally archive; the correct actions are jointly determined by workspace constraints, event stimuli, and MCP state, and the workspace does not contain the answers.

| Table name | Core | Initial row count | Dependent capability axis/check | Interference strategy | Meets standard |
|---|---|---:|---|---|---|
| `events` | Yes | 223 | Schedule conflicts and reminders/check s3/s11/s16/s22 | Dense interference from training, moving, and daily-life matters | Yes |

Loading and smoke test: `init.sql` is executed when the server starts, and the SQL referenced by `event.yaml` injects mutations at the corresponding stage.

Data source: offline synthetic data, with no real personal privacy information or real-time external web data.
