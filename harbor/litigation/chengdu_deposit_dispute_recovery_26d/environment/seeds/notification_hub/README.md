# notification_hub_mock env: chengdu_deposit_dispute_recovery_26d

- Core tables: notifications (~200, mostly background noise), subscriptions(4), official_accounts(1)+posts(3). Small-table exceptions: subscriptions/official_accounts business-natural.
- Server NEVER fabricates notifications; new rows + status transitions arrive ONLY via runtime SQL mutation.
- Key facts: notif_dispute_open (status=open at D0). The direct-utility payment is NOT pre-announced (surfaces via M3 banking insert).
- M2 (runtime mutation, NOT in this seed): insert ONE notification row 'awaiting_tenant + countdown' AND flip notion db-settlement-502 DisputeStatus -> awaiting_tenant; calendar carries the absolute deadline. No single source announces 'thissubmit/fastdetail'.
- Distractors: ~198 background notifications across listing/maps/shopping/system, drowning the dispute row.
- No keys/tokens. No conclusion fields.
