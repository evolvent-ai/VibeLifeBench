# listing_platform environment: baby_stroller_safety_standard_30d

This task-local listing_platform environment stores used-item listings, saved items, contacts, and viewings. It contains offline synthetic state at the start of the Baby Stroller Safety and Accessory Coordination scenario.

- Scenario window: 2026-06-15 through 2026-07-14
- Timezone: Asia/Shanghai
- Initial seed: `init.sql` (7 INSERT statements)
- State changes: applied by the ordered world-controller releases at their mapped event boundaries.

The seed is loaded into the vendored mock service before the first event. Later mutations are not included in the initial state and must be applied in timeline order. All records are synthetic and offline; no real personal data or internet access is required.
