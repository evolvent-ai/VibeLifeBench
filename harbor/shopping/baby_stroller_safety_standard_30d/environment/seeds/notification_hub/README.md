# notification_hub environment: baby_stroller_safety_standard_30d

This task-local notification_hub environment stores notifications, subscriptions, official accounts, and delivery state. It contains offline synthetic state at the start of the Baby Stroller Safety and Accessory Coordination scenario.

- Scenario window: 2026-06-15 through 2026-07-14
- Timezone: Asia/Shanghai
- Initial seed: `init.sql` (14 INSERT statements)
- State changes: applied by the ordered world-controller releases at their mapped event boundaries.

The seed is loaded into the vendored mock service before the first event. Later mutations are not included in the initial state and must be applied in timeline order. All records are synthetic and offline; no real personal data or internet access is required.
