# `notification_hub/zhao_meng_litigation`

## 中文说明

这是任务 `litigation/food_safety_dispute_33d`（食品安全网络购物退一赔十纠纷诉讼）使用的 task-local `notification_hub` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `zhao_meng_litigation`。场景窗口为 `2026-05-20` 至 `2026-06-22`，时区为 `Asia/Shanghai`。

## English Summary

This is the task-local `notification_hub` environment for `litigation/food_safety_dispute_33d` (Food Safety E-commerce Dispute Litigation — 33 Days). It contains the offline synthetic business state available at scenario start. The environment name is `zhao_meng_litigation`, the scenario window is `2026-05-20` through `2026-06-22`, and the timezone is `Asia/Shanghai`.

## 关联任务 / Associated Task

- **Task / 任务:** `litigation/food_safety_dispute_33d`
- **中文标题 / Chinese title:** 食品安全网络购物退一赔十纠纷诉讼
- **English title / 英文标题:** Food Safety E-commerce Dispute Litigation — 33 Days
- **Service / 服务:** `notification_hub`
- **Environment / 环境名:** `zhao_meng_litigation`
- **Scenario window / 场景窗口:** `2026-05-20` → `2026-06-22`
- **Timezone / 时区:** `Asia/Shanghai`

## 场景作用 / Scenario Role

保存通知、订阅、官方账号与消息送达状态。

Stores notifications, subscriptions, official accounts, and delivery state.

## 初始数据 / Seed Contents

初始文件为 `init.sql`。下表的行数来自对应服务 SQLite schema 与 `init.sql` 的全新内存加载；包括空表，以明确初始状态边界。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| 业务表 / Table | 初始行数 / Initial Rows |
|---|---:|
| `_counters` | 3 |
| `notifications` | 203 |
| `official_account_posts` | 210 |
| `official_account_subscriptions` | 4 |
| `official_accounts` | 4 |
| `price_alerts` | 0 |
| `subscriptions` | 3 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `official_account_posts` | 210 | `post_id` |
| `notifications` | 203 | `notification_id` |
| `official_account_subscriptions` | 4 | `user_id`, `account_id` |
| `official_accounts` | 4 | `account_id` |
| `subscriptions` | 3 | `subscription_id` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 中有 10 个事件会更新此服务 / 10 events in `event.yaml` update this service:

| Stage | Time / 时间 | Kind / 类型 | Update method / 更新方式 |
|---:|---|---|---|
| 1 | `2026-05-21T08:55:00+08:00` | `mutation` | SQL file `mutation_s1_court_notice.sql` |
| 2 | `2026-05-22T09:20:00+08:00` | `mutation` | SQL file `mutation_s2_regulator_notice.sql` |
| 4 | `2026-05-24T09:50:00+08:00` | `mutation` | SQL file `mutation_s4_evidence_notice.sql` |
| 7 | `2026-05-30T09:00:00+08:00` | `mutation` | SQL file `mutation_s7_seller_vanish.sql` |
| 8 | `2026-06-01T09:30:00+08:00` | `mutation` | SQL file `mutation_s8_case_accepted.sql` |
| 10 | `2026-06-04T09:00:00+08:00` | `mutation` | SQL file `mutation_s10_seller_defense.sql` |
| 12 | `2026-06-08T09:40:00+08:00` | `mutation` | SQL file `mutation_s12_hearing_notice.sql` |
| 13 | `2026-06-10T09:00:00+08:00` | `mutation` | SQL file `mutation_s13_inspect_conflict.sql` |
| 16 | `2026-06-16T09:50:00+08:00` | `mutation` | SQL file `mutation_s16_judgment_notice.sql` |
| 18 | `2026-06-18T13:50:00+08:00` | `mutation` | SQL file `mutation_s18_appeal_notice.sql` |

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 183452 bytes |
| `mutation_s10_seller_defense.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 716 bytes |
| `mutation_s12_hearing_notice.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 703 bytes |
| `mutation_s13_inspect_conflict.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 737 bytes |
| `mutation_s16_judgment_notice.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 730 bytes |
| `mutation_s18_appeal_notice.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 724 bytes |
| `mutation_s1_court_notice.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1137 bytes |
| `mutation_s2_regulator_notice.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1105 bytes |
| `mutation_s4_evidence_notice.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1117 bytes |
| `mutation_s7_seller_vanish.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 719 bytes |
| `mutation_s8_case_accepted.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 735 bytes |

## 加载说明 / Loading

兼容运行时应将 `notification_hub` 绑定到环境 `zhao_meng_litigation`，从任务目录内的 `envs/notification_hub/zhao_meng_litigation/` 读取数据。本次数据审计使用外部服务实现提供的 `SCHEMA_SQL` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `notification_hub` to environment `zhao_meng_litigation` and read `envs/notification_hub/zhao_meng_litigation/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
