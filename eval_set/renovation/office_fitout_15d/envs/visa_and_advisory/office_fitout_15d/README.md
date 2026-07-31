# `visa_and_advisory/office_fitout_15d`

## 中文说明

这是任务 `renovation/office_fitout_15d`（商业办公室 Fit-out 项目管理）使用的 task-local `visa_and_advisory` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `office_fitout_15d`。场景窗口为 `2026-07-01` 至 `2026-09-01`，时区为 `Asia/Shanghai`。

## English Summary

This is the task-local `visa_and_advisory` environment for `renovation/office_fitout_15d` (Commercial Office Fit-Out Project Management). It contains the offline synthetic business state available at scenario start. The environment name is `office_fitout_15d`, the scenario window is `2026-07-01` through `2026-09-01`, and the timezone is `Asia/Shanghai`.

## 关联任务 / Associated Task

- **Task / 任务:** `renovation/office_fitout_15d`
- **中文标题 / Chinese title:** 商业办公室 Fit-out 项目管理
- **English title / 英文标题:** Commercial Office Fit-Out Project Management
- **Service / 服务:** `visa_and_advisory`
- **Environment / 环境名:** `office_fitout_15d`
- **Scenario window / 场景窗口:** `2026-07-01` → `2026-09-01`
- **Timezone / 时区:** `Asia/Shanghai`

## 场景作用 / Scenario Role

保存签证、入境、出行建议与政策条件。

Stores visa, entry, travel-advisory, and policy conditions.

## 初始数据 / Seed Contents

初始文件为 `init.sql`。下表的行数来自对应服务 SQLite schema 与 `init.sql` 的全新内存加载；包括空表，以明确初始状态边界。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| 业务表 / Table | 初始行数 / Initial Rows |
|---|---:|
| `_counters` | 0 |
| `advisories` | 1 |
| `advisory_subscriptions` | 0 |
| `application_documents` | 2 |
| `entry_requirements` | 2 |
| `notifications` | 0 |
| `scripted_events` | 2 |
| `visa_applications` | 5 |
| `visa_products` | 5 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `visa_applications` | 5 | `application_id` |
| `visa_products` | 5 | `product_id` |
| `application_documents` | 2 | `doc_id` |
| `entry_requirements` | 2 | `origin_nationality`, `destination`, `purpose` |
| `scripted_events` | 2 | `seq` |
| `advisories` | 1 | `country_code` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 中有 21 个事件会更新此服务 / 21 events in `event.yaml` update this service:

| Stage | Time / 时间 | Kind / 类型 | Update method / 更新方式 |
|---:|---|---|---|
| 3 | `06:00` | `mutation` | SQL file `d03_property_design_rfi.sql` |
| 4 | `07:30` | `mutation` | SQL file `d04_noise_complaint_advisory.sql` |
| 5 | `06:05` | `mutation` | SQL file `d05_insurance_in_force.sql` |
| 5 | `06:15` | `mutation` | SQL file `d05_rainstorm_window_compressed.sql` |
| 5 | `06:30` | `mutation` | SQL file `d05_bim_lod400_demanded.sql` |
| 5 | `06:45` | `mutation` | SQL file `d05_noise_window_advisory.sql` |
| 6 | `05:45` | `mutation` | SQL file `d06_filing_approved.sql` |
| 8 | `06:50` | `mutation` | SQL file `d08_board_cut_insurance.sql` |
| 9 | `06:25` | `mutation` | SQL file `d09_g20_zone_curfew.sql` |
| 10 | `06:15` | `mutation` | SQL file `d10_fire_drawing_second_reject.sql` |
| 11 | `06:45` | `mutation` | SQL file `d11_lobby_badge_lead_time.sql` |
| 12 | `06:25` | `mutation` | SQL file `d12_electrical_load_insufficient.sql` |
| 13 | `06:00` | `mutation` | SQL file `d13_fire_inspection_partial_fail.sql` |
| 13 | `07:15` | `mutation` | SQL file `d13_internal_layout_advisory.sql` |
| 13 | `09:05` | `mutation` | SQL file `d13_handover_recheck_advisory.sql` |
| 13 | `17:05` | `mutation` | SQL file `d13_dual_recheck_approvals.sql` |
| 14 | `07:30` | `mutation` | SQL file `d14_handover_conditional.sql` |
| 15 | `06:30` | `mutation` | SQL file `d15_hvac_punch_item.sql` |
| 16 | `06:20` | `mutation` | SQL file `d16_voc_exceed.sql` |
| 18 | `05:45` | `mutation` | SQL file `d18_electrical_condition_cleared.sql` |
| 19 | `07:45` | `mutation` | SQL file `d19_closeout_gate_approvals.sql` |

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 16454 bytes |

## 加载说明 / Loading

兼容运行时应将 `visa_and_advisory` 绑定到环境 `office_fitout_15d`，从任务目录内的 `envs/visa_and_advisory/office_fitout_15d/` 读取数据。本次数据审计使用外部服务实现提供的 `_SCHEMA` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `visa_and_advisory` to environment `office_fitout_15d` and read `envs/visa_and_advisory/office_fitout_15d/` from the task directory. For this data audit, the external service implementation supplied `_SCHEMA`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
