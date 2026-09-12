# Resolved Findings

All historical smoke findings were the same setup readiness/race defect and are
resolved by the shared setup contract now present in every step.

1. Round 1 rollout compose/setup failure: every `steps/event-XXX/workdir/setup.sh`,
   lines 7-18, now waits for `world-controller` health and fails explicitly after
   60 seconds; lines 20-49 provide bounded controller POST handling.
2. Round 2 `event-000` setup exit 22: `steps/event-000/workdir/setup.sh:7-49`
   adds the readiness gate and retries transient connection, 409, and 5xx
   responses while preserving immediate failure for permanent errors.
3. Round 3 env smoke failure: all `steps/event-000` through `event-024`
   `workdir/setup.sh:7-49` use the same readiness and retry implementation.
4. Round 4 env smoke failure: release-bearing setup scripts, including
   `steps/event-003/workdir/setup.sh:20-49`, retry the post-release race before
   returning exit 22.
5. Round 5 env smoke failure: the final shared fix is recorded at
   `steps/event-003/workdir/setup.sh:7-49` and mirrored in all 25 setup files.

Verification: `python3 /data/pipeline/gates/env.py baby_stroller_safety_standard_30d`
returned `env gate: PASS (0 findings)` after a full 25-step nop smoke run.

## Round 3 scoring findings

6. Round 2 `paraphrase_drop` on `event-000/s0_result`, `event-001/s1_result`,
   `event-024/s0_result`, and `event-024/s1_result`: these checks now consume
   the frozen `delivery_logistics` and `credit_card` backend state through
   `tests/rubrics/_helpers.py:343-378` (`_backend_tracking_numbers_present`),
   instead of depending on response wording.  `_compact_identifier` at
   `tests/rubrics/_helpers.py:301-303` canonicalizes backend identifiers and
   accepts the service's masked-card field variants without weakening the
   expected values.

Verification: `verify.py` and `fail2test.py` both report PASS after the change;
the targeted backend fixture remains bidirectional.
