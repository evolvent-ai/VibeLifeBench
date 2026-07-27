<div align="center">

# Vibelifebench

[![Tasks](https://img.shields.io/badge/tasks-200-blue)](#tasks)
[![Open subset](https://img.shields.io/badge/open_subset-20-06b6d4)](#tasks)
[![Domains](https://img.shields.io/badge/domains-10-8b5cf6)](#tasks)
[![Services](https://img.shields.io/badge/services-21-f59e0b)](#service-coverage)
[![Language](https://img.shields.io/badge/lang-zh%20%2B%20en-lightgrey)](#tasks)

**Benchmark version:** `1.1.0`<br>
**Scoring contract:** `flat_pool`

> **Long-horizon** &mdash; 20&ndash;30 stages per task, spanning simulated weeks.<br>
> **Multi-service** &mdash; task-local environment bindings across 21 services.<br>
> **Verifiable** &mdash; atomic checks reading real backend state, not prose.

</div>

---

## Why it is hard

Vibelifebench evaluates agents on the messy, consequential work of managing someone's
life over weeks: a lawsuit, a mortgage escrow shortfall, a cross-city apartment hunt,
a licensing exam, an office fit-out.

Each task unfolds as a timeline. The user sends messages, the world changes underneath
the agent (a hearing gets rescheduled, a price moves, a policy updates), and the agent
has to keep goals, constraints, commitments, and open items coherent across every stage
&mdash; while knowing which actions it may take on its own and which require asking first.

- **Stage 20 depends on what the agent understood at stage 3.** Nothing re-states the
  context along the way. Constraints given once, in passing, are still binding twenty
  stages later.
- **The world moves silently.** Many changes arrive with no notification at all. Only an
  agent that re-checks discovers the discrepancy in time to act on it.
- **Narration earns nothing.** Checks read backend state and workspace artifacts. An
  agent that says it booked the flight, but did not, scores zero for that check.
- **Some actions need permission.** Reads and drafts are free; payments, orders, and
  cancellations are not. Acting without asking is penalised, and so is asking about
  everything.
- **Nothing is retrieval.** Every environment is offline synthetic data, so no answer
  exists in pretraining, across 21 services.

Run it yourself in about fifteen minutes of setup &mdash; [Quickstart](#quickstart).

## Tasks

The full benchmark is **200 tasks** across 10 domains. This repository ships a
**20-task open subset**, two per domain, that is complete and runnable on its own.
Every task ships bilingual (zh/en) documentation and is fully self-contained.

To evaluate against all 200, email
**[vibelife@evolvent.co](mailto:vibelife@evolvent.co)** &mdash; see
[Want us to run it instead?](#want-us-to-run-it-instead).

### The open subset

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

Task counts are for the 20-task open subset in this repository.

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
├── servers/                     # 22 mock services (MCP), one directory each
│   └── <service>_mock/
│       ├── src/                 # service implementation
│       ├── Dockerfile           # image the capability layer launches
│       └── SPEC.md              # tool surface and schema
├── capabilities/                # Terrarium capability per service + shared base
├── scripts/
│   └── materialize_envs.py      # build the top-level envs/ tree (run this first)
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

Every environment payload is committed task-locally. The top-level `envs/` tree the
capability layer reads from is generated, not committed — see [Quickstart](#quickstart).

## Quickstart

You need **Docker**, **Python 3.12+**, and [**uv**](https://docs.astral.sh/uv/). The
whole benchmark runs offline against local containers &mdash; the only network traffic is
to your own model endpoint.

### Setup

One-time, about fifteen minutes &mdash; most of it waiting on the image builds.

```bash
git clone https://github.com/evolvent-ai/VibeLifeBench.git
cd VibeLifeBench

# Install the harness and build the world
uv sync                              # Terrarium, pinned to a validated commit
python3 scripts/materialize_envs.py  # the envs/ tree the services load from
./build_images.sh                    # 22 mock service images (~10 min, once)

# Point it at your model
cp models.json.example models.json
chmod 600 models.json                # then edit: keep one provider, fill in its apiKey
```

`uv sync` installs [**Terrarium**](https://github.com/evolvent-ai/Terrarium), the
sandboxed execution engine that runs each trial. The agent itself runs as
**OpenClaw 2026.7.1** in a workspace image Terrarium pulls on first use. Both that
image and the Terrarium commit are pinned, so everyone measures the same harness.

### Run the benchmark

```bash
# Smoke-test first — one task, proves the whole stack works
python3 scripts/run_eval.py --model anthropic/claude-opus-4-8 --tasks galapagos_no_us_transit

# The whole open subset (20 tasks, single attempt)
python3 scripts/run_eval.py --model anthropic/claude-opus-4-8

# Standard reporting protocol (three attempts per task, averaged)
python3 scripts/run_eval.py --model anthropic/claude-opus-4-8 --attempts 3

# One domain, three in parallel
python3 scripts/run_eval.py --model openai/gpt-5.5 --domains travel --concurrent 3

# Re-print the score table for a finished or in-flight run
python3 scripts/run_eval.py --report outputs/<job>
```

The runner preflights your setup and, when something is missing, prints the exact
command that fixes it. A full 20-task pass is many hours of wall-clock &mdash; each trial
replays a multi-week timeline. Watch it with `tail -f outputs/<job>/job.log`.

Key flags: `--list` (all task ids), `--tasks ID [ID ...]`, `--domains D [D ...]`,
`--attempts N`, `--concurrent N` (default `4`), `--think off…xhigh` (default `xhigh`),
`--timeout SEC` (default `14400`), `--dry-run`, `--report DIR`.

### Want us to run it instead?

The 20 tasks here are an open subset. To evaluate against the **full 200-task
benchmark** &mdash; or if you would rather not stand up the harness at all &mdash; email
**[vibelife@evolvent.co](mailto:vibelife@evolvent.co)** with the model name, an endpoint
we can reach, and any inference settings you want used. We run it and send back the
per-domain breakdown.

### Models

The template ships four models, one per provider. **Delete the ones you do not use**,
then fill in the `apiKey` of the one you keep. Reference a model as
`<provider>/<model id>`:

| Provider | `--model` | Notes |
|---|---|---|
| `anthropic` | `anthropic/claude-opus-4-8` | native `anthropic-messages`; thinking is set for you |
| `openai` | `openai/gpt-5.5` | `reasoning_effort` in `params` |
| `moonshot` | `moonshot/kimi-k2.6` | 256K context, the model's own ceiling; use `api.moonshot.cn` inside mainland China |
| `deepseek` | `deepseek/deepseek-v4-pro` | needs `thinkingFormat: "deepseek"` |

Model `id`s must match what your endpoint expects &mdash; some gateways rename them, and
vendors ship new versions. Any OpenAI-compatible gateway also works: keep
`"api": "openai-completions"`, point `baseUrl` at it, and keep `authHeader: true`
(native Anthropic is the exception, which authenticates without it).

Reasoning depth has two independent knobs, and both ship at their maximum:
`reasoning_effort` in `models.json` goes to the model, while `--think` sets OpenClaw's
own level. Both default to `xhigh`. OpenClaw also accepts `max`, but only passes it
through when the model itself declares support for that effort &mdash; otherwise it falls
back to `xhigh`. If your endpoint does accept `max`, add it to
`supportedReasoningEfforts` and set `reasoning_effort` to match. Lower both together
for a cheaper run.

`models.json` is git-ignored &mdash; never commit it.

### Scoring

Each task scores as the earned fraction of its total check weight (`flat_pool`), so
scores are comparable across tasks. The reported figure is the mean over tasks; with
`--attempts 3` each task is averaged over its attempts first, which is the standard
`avg@3` protocol.

`run_eval.py` only generates a Terrarium config and summarises results. To customise
beyond the flags above, use `--dry-run` and edit the generated TOML, then:

```bash
.venv/bin/terrarium run -c outputs/<job>.toml
```

### Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `RuntimeError: Could not locate ... project root` | `envs/` was never generated. Run `python3 scripts/materialize_envs.py`. |
| `FileNotFoundError: env dir not found` | `envs/` is stale after editing a task-local env. Re-run `materialize_envs.py`; `--check` reports drift without writing. |
| `'X' MCP not ready` | That service's image is missing or its container exited. Re-run `./build_images.sh X`, then `docker logs` the exited container. |
| Trials end at exactly the timeout | Long tasks hitting `--timeout` (default 4h). Raise it, or lower `--concurrent` if the host is saturated. |
| Every task scores 0.0 | Almost always model config: a wrong `model_name`, or an endpoint rejecting the key. Check `outputs/<job>/*/trial.log`. |

Environments are committed task-locally, but `capabilities/base.py` resolves them from a
single top-level `envs/<service>/<env_name>/` tree; `materialize_envs.py` flattens all
137 bindings into it. The task-local copies are the source of truth, and `envs/` is a
git-ignored build artifact.

## Environments

All 137 bindings use the layout `eval_set/<domain>/<task>/envs/<service>/<env_name>/`.

Every environment contains a non-empty `init.sql` and a bilingual `README.md`; some also
include `init.json`, JSONL records, or SQL updates referenced by `event.yaml`. Every SQL
seed was freshly loaded against its service schema and checked with SQLite
`integrity_check` and foreign-key validation.

Environments are seeded from `init.sql` at load time, so no database files are committed.

## Evaluation

All tasks use `flat_pool` scoring: atomic checks draw from a single weighted pool,
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

The services and their capability bindings ship here, but the engine that drives them
does not. Execution still depends on an external runtime, which must:

1. provide the [Terrarium](https://github.com/evolvent-ai/Terrarium)/OpenClaw task APIs
   referenced by `task.py`;
2. build the `servers/` images and launch them per `capabilities/`;
3. apply `event.yaml` events in stage and time order;
4. supply workspace persistence, tool traces, and the runtime context the rubrics need.

The pin is Terrarium commit
[`7d641ea`](https://github.com/evolvent-ai/Terrarium/tree/7d641ea587687e7360f2bf74951b9353c2894b18),
which in turn pins the OpenClaw 2026.7.1 workspace image. Later builds can change
session and runner behaviour, so track the pin rather than `main`.

Service resolution is declared by `[dependencies.envs]` in each `task.toml` and read
from the generated top-level `envs/` tree (see [Quickstart](#quickstart)).

`scripts/run_eval.py` writes the run config for you. Each task also ships a `run.toml`
for running it standalone; set the model there before using one directly:

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

No repository-level license file is bundled. Use and redistribution of the task bundles
are governed by the terms supplied by the publisher for this repository.

The mock services under `servers/` carry their own MIT license files (19 of 22;
`car_rental_mock`, `flight_booking_mock`, and `rail_booking_mock` ship without one).

## Citation

```bibtex
@misc{vibelifebench_2026,
  title        = {Vibelifebench: A 20-Task Long-Horizon Agent Evaluation Set},
  year         = {2026},
  note         = {Long-horizon agent tasks with task-local synthetic environments,
                  22 mock services, and the Terrarium capability layer}
}
```

---

<p align="center">Vibelifebench &middot; Evolvent AI</p>
