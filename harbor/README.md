# Harbor-format task subset

The open benchmark — **100 tasks, 10 per domain** — in
[Harbor](https://github.com/laude-institute/harbor) task format. The 20-task
native-format subset in [`eval_set/`](../eval_set) (run through the Terrarium
harness) is a subset of this 100, shipped in the other format.

Same world as the rest of VibeLifeBench: each task replays a multi-week personal
timeline of user messages, silent world mutations, and policy changes, and is
scored by atomic checks that read backend state and workspace artifacts — not
prose.

## Layout

```
harbor/<domain>/<task>/
├── task.toml            # multi-step task definition (schema 1.3, final-step reward)
├── environment/         # docker compose stack: task-local mock servers, DB seeds,
│                        # world controller, evidence collector, agent workspace
├── steps/event-*/       # one directory per stage:
│   ├── instruction.md   # what the user asks at this stage
│   ├── workdir/         # per-stage world mutations (setup.sh)
│   └── solution/        # oracle reference trajectory (solve.sh, oracle.py) + verifier
└── tests/               # rubrics/ + run_verifier.py — the final scorer
```

Scoring uses `multi_step_reward_strategy = "final"`: the last step recomputes every
stage's rubrics from the immutable evidence tree, so the reward reflects the whole
timeline rather than just the ending. Per-trial diagnostics land in
`reward.json` / `checks.json`.

## Requirements

- **Docker** — each task builds its own compose stack; everything runs offline.
- **Harbor CLI** — `uv tool install harbor`
  ([Harbor on GitHub](https://github.com/laude-institute/harbor)).
- **An agent** — e.g. the `claude-code` or `codex` CLI on `PATH`, with its
  credentials in the environment (or pass `--env-file .env`).

## Quickstart

```bash
# smoke test — one task
scripts/run_harbor.sh --domain career --include '*espp*'

# one domain
scripts/run_harbor.sh --domain finance

# all 10 domains, 100 tasks
scripts/run_harbor.sh --model anthropic/claude-opus-4-8 --agent claude-code
```

The script is a thin loop of `harbor run --path harbor/<domain>`; its flags map
1:1. Or drive Harbor directly:

```bash
harbor run --path harbor/travel --agent claude-code --model <model> -n 4
```

## Task inventory

| Domain | Tasks |
|---|---|
| `career` | `campus_ai_infra_offer_deadline_tradeoff`, `career_background_check_consent`, `career_chronic_disclosure_boundary`, `career_equity_buyback_recovery`, `career_espp_refund_recovery`, `career_jobhop_tax_reconcile`, `career_onboarding_medical_privacy`, `career_option_exercise_window`, `career_relocation_reimburse_reconcile`, `career_seed_017_sqe_to_supply_chain_data` |
| `exam_preparation` | `bank_teller_dual_subject_cert_prep`, `campus_retake_makeup_deferral_rule_guard_015`, `civil_service_written_to_interview_audit`, `clinical_dietitian_rd_exam_prep`, `constructor_exam_site_project_safety`, `fund_practitioner_broker_intern_conversion_012`, `gmat_focus_mba_r2_schedule_003`, `grad_exam_prep_and_family_care`, `interpreter_cert_oral_exam_travel_equipment`, `pharmacist_western_registration_shift_prep` |
| `finance` | `arm_escrow_shortfall_reset_guard_30d`, `auto_loan_gap_refi_guard_30d`, `college_529_room_board_guard_30d`, `credit_card_minimum_payment_escape_guard_30d`, `disability_leave_income_gap_guard_30d`, `divorce_asset_rebuild_30d`, `ev_auto_balloon_refi_guard_30d`, `finance_shen_zhixing_45`, `hsa_medical_bill_liquidity_guard_30d`, `inherited_ira_rmd_tax_guard_30d` |
| `fitness` | `airport_ground_staff_baggage_shift_recovery`, `bike_commute_safety_adaptation_016`, `broadcast_exam_posture_breathing_32d`, `choir_member_low_impact_knee_privacy_049`, `dragon_boat_newcomer_upper_body_endurance_037`, `fit_pool_player_wrist_shoulder_stance_036`, `fit_programmer_posture_microtraining_002`, `fit_triathlon_intro_multisport_adaptation_052`, `flight_attendant_jetlag_circulation_recovery_051`, `go_teacher_neck_eye_microbreak_033` |
| `litigation` | `chengdu_deposit_dispute_recovery_26d`, `estate_will_capacity_conflict_26d_repair`, `food_safety_dispute_33d`, `house_lease_dispute_30d`, `litigation_ayiguli_maimaiti_58`, `litigation_chen_wangshu_58`, `litigation_diego_morales_47`, `litigation_fatima_alkhatib_59`, `litigation_han_yushan_57`, `private_lending_33d` |
| `renovation` | `apartment_renovation_20d`, `bath_total_reno_v4_30d`, `bathroom_reno_30d`, `bed_total_reno_v4_30d`, `floor_total_reno_v4_30d`, `garage_adu_rental_conversion_25d`, `garden_total_reno_v4_30d`, `highrise_handover_v5_30d`, `home_livestream_studio_noise_privacy_011_v4`, `office_fitout_15d` |
| `rental` | `cross_city_remote_viewing_rental`, `family_kindergarten_low_voc`, `nanjing_relocation_remote_lease_22d_refined`, `old_home_renovation_rental_28d_refined_upload_clean`, `renewal_negotiation_repair_rental`, `rental_seed_013_task`, `rental_seed_015_task`, `rental_seed_018_task`, `rental_seed_019_task`, `wheelchair_student_accessible_rental` |
| `shopping` | `anc_earphone_presale_30d`, `android_flagship_tradein_30d`, `apple_watch_tradein_30d`, `baby_stroller_safety_standard_30d`, `beauty_prepaid_rights_30d`, `camera_resale_30d`, `camping_gear_resale_30d`, `camping_trip_procure_30d`, `central_ac_install_30d`, `community_household_groupbuy_30d` |
| `team_building` | `alcohol_free_sales_celebration`, `bilingual_city_culture_day`, `budget_cocreation_camp_21d`, `coastal_sailing_teamday_26d`, `community_service_volunteer_26d`, `cross_dept_book_club_dinner_26d`, `customer_success_recovery_lunch`, `factory_visit_safety_day`, `family_office_open_day`, `pottery_invoice_compliance_day` |
| `travel` | `bali_22d`, `east_asia_group_trip_24d`, `east_china_bereavement_docs_reissue`, `family_medical_accessible_japan_53d`, `family_rv_australia_childseat_trial`, `galapagos_no_us_transit`, `hard_biz_trip_24d_v4_hybrid_gate_diff_20260627`, `italy_wedding_guest_strike_22d`, `japan_20d`, `lin_ming_sf_summit` |

## Notes

- Stage instructions (`steps/*/instruction.md`) are in English.
- `steps/*/solution/` ships the reference (oracle) trajectory for each stage —
  useful for calibration and debugging. The graded signal comes only from
  `tests/run_verifier.py` over `tests/rubrics/`.
- All people, organizations, accounts, messages, and transactions are offline
  synthetic data; no real personal data and no network access beyond your model
  endpoint.
