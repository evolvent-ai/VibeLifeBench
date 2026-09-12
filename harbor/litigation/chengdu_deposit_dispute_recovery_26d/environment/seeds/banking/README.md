# banking_mock env: chengdu_deposit_dispute_recovery_26d

- User: usr_chenrui. Accounts(2): checking Ryan Chensalary card, savings savings account. Money in minor units (fen).
- Core tables: transactions (~205 incl. noise), payees(3 pre-existing utility payees), accounts(2). Small-table exception: accounts(2).
- Key facts (no conclusions):
  - security deposit ¥6000 (600000fen) detail Leo Wang personaldetail (2025-05).
  - 13 detailmonthdetail ¥2600, detailLeo Wang (detailmonthdetailpaiddetail).
  - thisdetailpaid directlyutilities ¥480 (48000fen) is NOT pre-seeded; M3 (stage 7) inserts it at runtime as the duplicate-charge proof (discover by re-polling).
  - detaillease termsecurity deposit ¥5500 alreadydetail (distractor, detail).
- Leo Wang/indetail NOT pre-added as payees; transfer is same-user-only. HC2 checked via 'no add_payee+pay_payee to other party, no transfer to other party'.
- Distractors: salary, detail, detail, daydetail noise; prior-lease deposit.
- No keys/tokens. No conclusion fields.
