# calendar_mock env: chengdu_deposit_dispute_recovery_26d

- Core tables: events (~200 incl. noise), reminders (~40), calendars(1). Small-table exception: calendars(1).
- Key facts: cal_dispute_deadline (D17 detailsubmitdeadline, reminder 1detail); cal_mediation_reply (D9 settlementresponse deadline); cal_countdown_reminder (D19 countdowndetail, scheduled trigger).
- No 'must submit'/conclusion wording; dates are neutral world facts. The scheduled reminder pairs with stage checker verifying timely submission.
- Distractors: ~197 background routine events.
- No keys/tokens. No conclusion fields.
