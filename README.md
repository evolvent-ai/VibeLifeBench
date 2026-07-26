---
pretty_name: Vibelifebench
language:
- zh
- en
license: other
task_categories:
- text-generation
tags:
- agents
- tool-use
- long-horizon
- evaluation
- synthetic-data
size_categories:
- n<1K
---

<div align="center">

# Vibelifebench

[![Tasks](https://img.shields.io/badge/tasks-20-blue)](#tasks)
[![Domains](https://img.shields.io/badge/domains-10-8b5cf6)](#tasks)
[![Stages](https://img.shields.io/badge/stages-489-0ea5e9)](#tasks)
[![Checks](https://img.shields.io/badge/atomic_checks-1247-green)](#evaluation)
[![Services](https://img.shields.io/badge/services-21-f59e0b)](#service-coverage)
[![Language](https://img.shields.io/badge/lang-zh%20%2B%20en-lightgrey)](#tasks)

**Benchmark version:** `1.1.0`<br>
**Scoring contract:** `flat_pool`

> **Long-horizon** &mdash; 20&ndash;30 stages per task, spanning simulated weeks.<br>
> **Multi-service** &mdash; 137 task-local environment bindings across 21 services.<br>
> **Verifiable** &mdash; 1247 atomic checks reading real backend state, not prose.

</div>

---

## Overview

Vibelifebench evaluates agents on the messy, consequential work of managing someone's
life over weeks: a lawsuit, a mortgage escrow shortfall, a cross-city apartment hunt,
a licensing exam, an office fit-out.

Each task unfolds as a timeline. The user sends messages, the world changes underneath
the agent (a hearing gets rescheduled, a price moves, a policy updates), and the agent
has to keep goals, constraints, commitments, and open items coherent across every stage
&mdash; while knowing which actions it may take on its own and which require asking first.

What makes this hard is not any single step. It is that **stage 20 depends on what the
agent understood at stage 3**, and nothing re-states the context along the way.

> **Task-only release.** This repository distributes task bundles only: no service
> implementations, mock servers, capability framework, or execution engine. Running the
> tasks requires a compatible Terrarium/OpenClaw runtime and service implementations
> supplied separately. See [External Runtime Requirement](#external-runtime-requirement).

## Tasks

20 tasks across 10 domains, 489 stages, 1247 atomic checks. Every task ships bilingual
(zh/en) documentation and is fully self-contained.

| Domain | Task ID | Title | Stages | Envs | Checks | Weight | Difficulty |
|---|---|---|---:|---:|---:|---:|---|
| Career / 职业与劳动权益 | `career_equity_buyback_recovery` | Equity Buyback Reconciliation and Re-employment | 25 | 7 | 42 | 100 | `hard` |
| Career / 职业与劳动权益 | `career_espp_refund_recovery` | ESPP Redemption Reconciliation and Re-employment | 24 | 7 | 42 | 100 | `hard` |
| Exam prep / 考试准备 | `civil_service_written_to_interview_audit` | Civil Service Written Exam to Interview Qualification Audit | 25 | 9 | 40 | 62 | `hard` |
| Exam prep / 考试准备 | `pharmacist_western_registration_shift_prep` | Licensed Pharmacist Registration, Course Purchase, and Shift-Based Preparation | 30 | 5 | 53 | 89 | `hard` |
| Finance / 个人金融 | `arm_escrow_shortfall_reset_guard_30d` | ARM Escrow Shortfall Reset Guard — 30-Day Plan | 24 | 6 | 123 | 386 | `hard` |
| Finance / 个人金融 | `hsa_medical_bill_liquidity_guard_30d` | HSA Medical Bill Liquidity Guard — 30-Day Plan | 24 | 6 | 123 | 386 | `hard` |
| Fitness / 运动与体能 | `broadcast_exam_posture_breathing_32d` | Broadcast Arts Exam Posture, Breathing, and Taper Maintenance | 26 | 5 | 50 | 82.5 | `hard` |
| Fitness / 运动与体能 | `dragon_boat_newcomer_upper_body_endurance_037` | Dragon Boat Newcomer Upper-Body Endurance Preparation | 28 | 6 | 44 | 68.5 | `hard` |
| Litigation / 诉讼管理 | `food_safety_dispute_33d` | Food Safety E-commerce Dispute Litigation — 33 Days | 22 | 5 | 51 | 100 | `hard` |
| Litigation / 诉讼管理 | `private_lending_33d` | Private Lending Recovery Litigation — 33 Days | 22 | 5 | 71 | 100 | `medium` |
| Renovation / 装修与改造 | `garage_adu_rental_conversion_25d` | Legal Garage-to-Rental ADU Conversion | 25 | 8 | 45 | 77.5 | `medium` |
| Renovation / 装修与改造 | `office_fitout_15d` | Commercial Office Fit-Out Project Management | 21 | 7 | 105 | 289.657 | `hard` |
| Rental / 住房租赁 | `cross_city_remote_viewing_rental` | Cross-City Remote Viewing Rental and Address Proof | 24 | 8 | 66 | 97.5 | `hard` |
| Rental / 住房租赁 | `wheelchair_student_accessible_rental` | Accessible Campus Housing for a Wheelchair-Using Student | 24 | 8 | 58 | 88.75 | `hard` |
| Shopping / 购物与履约 | `baby_stroller_safety_standard_30d` | Baby Stroller Safety and Accessory Coordination | 24 | 7 | 69 | 134 | `medium` |
| Shopping / 购物与履约 | `central_ac_install_30d` | Central Air-Conditioning Installation and After-Sales Reconciliation | 24 | 7 | 70 | 136.5 | `hard` |
| Team building / 团队活动 | `factory_visit_safety_day` | Supply Chain Factory Visit Team Day | 25 | 7 | 46 | 100 | `hard` |
| Team building / 团队活动 | `pottery_invoice_compliance_day` | Indoor Pottery Team-Building Planning | 25 | 7 | 64 | 100 | `medium` |
| Travel / 差旅与出行 | `east_china_bereavement_docs_reissue` | Low-Disruption Bereavement Travel and Document Reissue Assistance | 22 | 10 | 44 | 100 | `hard` |
| Travel / 差旅与出行 | `galapagos_no_us_transit` | Galapagos Travel Without U.S. Transit | 25 | 7 | 41 | 100 | `hard` |


> **Difficulty labels in 1.1.0 are retained from the prior audited release.** The
> scoring contract changed to `flat_pool`, but the labels were not recalibrated or
> re-bucketed for this release: 16 tasks are `hard`, 4 are `medium`, and 0 are `easy`.

`Envs` counts the task's service-environment bindings. `Weight` is the task's declared
total scoring weight; scores are normalized per task, so weights are not comparable
across tasks.

### What a task looks like

```yaml
# event.yaml — the timeline the runtime replays
stages:
  0:
    - id: S00_user_initial_request
      time: 2026-07-24T09:10:00+08:00
      type: user_message
      from: 林乔
      body: |
        我 8 月要去厄瓜多尔参加一个加拉帕戈斯生态数据工作坊...
        能 hold 的先 hold，最终付款和不可退项目要先跟我确认。
  1:
    - id: S01_mutation_workshop_calendar_publish
      time: 2026-07-25T09:40:00+08:00
      type: mutation          # the world changes without being announced
      target: calendar_mock
```

Stages are checkpoints, not calendar days. Event types include `user_message`,
`mutation`, `notification`, `world`, and `policy_update`.

## Capability Coverage

- **Long-horizon state maintenance** &mdash; keep goals, constraints, commitments, and open
  items consistent across many stages.
- **Tool use** &mdash; query and act across email, calendar, banking, booking, maps,
  knowledge-base, and notification services.
- **Dynamic world updates** &mdash; apply staged changes in event order without using
  future facts early.
- **Authorization and risk control** &mdash; distinguish reads and drafts from payments,
  orders, cancellations, and other high-impact actions.
- **Evidence and traceability** &mdash; keep business state, tool results, and workspace
  deliverables in agreement.
- **Cross-service coordination** &mdash; reconcile times, amounts, statuses, identities,
  policies, and dependencies across services.

### Service Coverage

| Service | Tasks | Service | Tasks | Service | Tasks |
|---|---:|---|---:|---|---:|
| `calendar` | 20 | `email` | 20 | `notion` | 18 |
| `notification_hub` | 12 | `legal_search` | 9 | `maps` | 8 |
| `review_platform` | 7 | `banking` | 6 | `credit_card` | 5 |
| `ecommerce` | 5 | `weather` | 5 | `brokerage` | 4 |
| `listing_platform` | 4 | `hotel_booking` | 3 | `delivery_logistics` | 2 |
| `flight_booking` | 2 | `health_tracker` | 2 | `job_board` | 2 |
| `content_platform` | 1 | `rail_booking` | 1 | `visa_and_advisory` | 1 |

## Repository Structure

```
Vibelifebench/
├── README.md
└── eval_set/
    └── <domain>/
        └── <task>/
            ├── task.py          # entrypoint, service binding, event dispatch, aggregation
            ├── task.md          # bilingual public task card
            ├── task.toml        # metadata, dependencies, scenario window, scoring summary
            ├── event.yaml       # stage timeline: user messages, notifications, updates
            ├── run.toml         # runner configuration
            ├── workspace/       # initial agent workspace and durable deliverables
            ├── envs/
            │   └── <service>/<env_name>/    # task-local seed, env card, staged data
            ├── mutations/       # standalone staged updates (when present)
            └── rubrics/         # formal scoring modules
```

The repository root contains only `README.md` and `eval_set/`. Every environment payload
is task-local; no shared top-level `envs/` directory is distributed.

## Environments

All 137 bindings use the layout `eval_set/<domain>/<task>/envs/<service>/<env_name>/`.

Every environment contains a non-empty `init.sql` and a bilingual `README.md`; some also
include `init.json`, JSONL records, or SQL updates referenced by `event.yaml`. Every SQL
seed was freshly loaded against its service schema and checked with SQLite
`integrity_check` and foreign-key validation.

Environments are seeded from `init.sql` at load time, so no database files are committed.

## Evaluation

All 20 tasks use `flat_pool` scoring: atomic checks draw from a single weighted pool,
and the task score is the earned fraction of total weight.

Rubric modules live in `rubrics/` and are loaded and aggregated by `task.py`:

| Module | Scope |
|---|---|
| `stage_<N>.py` | Per-stage execution |
| `cross_stage.py` | Consistency across stages |
| `final.py` | Final deliverables |
| `_helpers.py` | Shared predicates and backend-state assertions |

Every task provides `stage_<N>.py`, `cross_stage.py`, `final.py`, and `_helpers.py`;
a few carry additional task-specific helper modules.

Checks are written to read backend state and workspace artifacts rather than reward
narration, so describing an action does not earn the credit for performing it.

`task.toml` records each task's post-cleanup atomic-check count and declared total weight.

## External Runtime Requirement

Task content is complete as a bundle, but execution depends on an external runtime.
A compatible environment must:

1. provide the Terrarium/OpenClaw task APIs referenced by `task.py`;
2. provide implementations and schemas for the declared services;
3. load environments from task-local `envs/` per `[dependencies.envs]` in `task.toml`;
4. apply `event.yaml` events in stage and time order;
5. supply workspace persistence, tool traces, and the runtime context the rubrics need.

Set the model in each task's `run.toml` before running:

```toml
[[agents]]
name = "openclaw"
model_name = "<your-provider>/<your-model>"
```

## Synthetic Data and Privacy

All people, organizations, accounts, communications, orders, transactions, places, policy
summaries, health records, and other business entities are offline synthetic data. The
environments require no internet access and contain no real personal data.

## License

No license file is bundled with this task-only release. Use and redistribution are
governed by the terms supplied by the publisher for this repository.

## Citation

```bibtex
@misc{vibelifebench_2026,
  title        = {Vibelifebench: A 20-Task Long-Horizon Agent Evaluation Set},
  year         = {2026},
  howpublished = {Task-only release},
  note         = {Long-horizon agent tasks with task-local synthetic environments}
}
```

---

<p align="center">Vibelifebench &middot; Evolvent AI</p>
