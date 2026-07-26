# `notification_hub/pharmacist_western_registration_shift_prep`

## 中文说明

这是任务 `exam_preparation/pharmacist_western_registration_shift_prep`（执业药师西药类报名初审、正版课程采购与倒班备考）使用的 task-local `notification_hub` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `pharmacist_western_registration_shift_prep`。场景窗口为 `2026-08-01` 至 `2026-10-11`，时区为 `Asia/Shanghai`。

## English Summary

This is the task-local `notification_hub` environment for `exam_preparation/pharmacist_western_registration_shift_prep` (Licensed Pharmacist Registration, Course Purchase, and Shift-Based Preparation). It contains the offline synthetic business state available at scenario start. The environment name is `pharmacist_western_registration_shift_prep`, the scenario window is `2026-08-01` through `2026-10-11`, and the timezone is `Asia/Shanghai`.

## 关联任务 / Associated Task

- **Task / 任务:** `exam_preparation/pharmacist_western_registration_shift_prep`
- **中文标题 / Chinese title:** 执业药师西药类报名初审、正版课程采购与倒班备考
- **English title / 英文标题:** Licensed Pharmacist Registration, Course Purchase, and Shift-Based Preparation
- **Service / 服务:** `notification_hub`
- **Environment / 环境名:** `pharmacist_western_registration_shift_prep`
- **Scenario window / 场景窗口:** `2026-08-01` → `2026-10-11`
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
| `notifications` | 1 |
| `official_account_posts` | 220 |
| `official_account_subscriptions` | 2 |
| `official_accounts` | 3 |
| `price_alerts` | 0 |
| `subscriptions` | 2 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `official_account_posts` | 220 | `post_id` |
| `official_accounts` | 3 | `account_id` |
| `official_account_subscriptions` | 2 | `user_id`, `account_id` |
| `subscriptions` | 2 | `subscription_id` |
| `notifications` | 1 | `notification_id` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 中有 10 个事件会更新此服务 / 10 events in `event.yaml` update this service:

| Stage | Time / 时间 | Kind / 类型 | Update method / 更新方式 |
|---:|---|---|---|
| 1 | `2026-08-03T08:59:00+08:00` | `mutation` | SQL file `stage_1_registration_notice.sql` |
| 6 | `2026-08-15T08:00:00+08:00` | `mutation` | SQL file `stage_6_schema_org_code.sql` |
| 10 | `2026-08-24T10:20:00+08:00` | `mutation` | SQL file `stage_10_law_update_post.sql` |
| 13 | `2026-08-30T20:51:00+08:00` | `mutation` | SQL file `stage_13_submission_pending.sql` |
| 15 | `2026-09-04T09:00:00+08:00` | `mutation` | SQL file `stage_15_review_reject.sql` |
| 16 | `2026-09-04T21:26:00+08:00` | `mutation` | SQL file `stage_16_resubmitted.sql` |
| 20 | `2026-09-18T09:00:00+08:00` | `mutation` | SQL file `stage_20_payment_open.sql` |
| 21 | `2026-09-18T21:11:00+08:00` | `mutation` | SQL file `stage_21_payment_complete.sql` |
| 26 | `2026-10-06T08:00:00+08:00` | `mutation` | SQL file `stage_26_ticket_open.sql`; SQL file `stage_26_ticket_window_post.sql` |
| 27 | `2026-10-08T09:00:00+08:00` | `mutation` | SQL file `stage_27_ticket_ready.sql` |

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 76147 bytes |

## 加载说明 / Loading

兼容运行时应将 `notification_hub` 绑定到环境 `pharmacist_western_registration_shift_prep`，从任务目录内的 `envs/notification_hub/pharmacist_western_registration_shift_prep/` 读取数据。本次数据审计使用外部服务实现提供的 `SCHEMA_SQL` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `notification_hub` to environment `pharmacist_western_registration_shift_prep` and read `envs/notification_hub/pharmacist_western_registration_shift_prep/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
