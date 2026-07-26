# `banking/career_espp_refund_recovery`

## 中文说明

这是任务 `career/career_espp_refund_recovery`（离职员工持股计划赎回争议核对与再就业）使用的 task-local `banking` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `career_espp_refund_recovery`。场景窗口为 `2026-06-08` 至 `2026-08-25`，时区为 `Asia/Shanghai`。

## English Summary

This is the task-local `banking` environment for `career/career_espp_refund_recovery` (ESPP Redemption Reconciliation and Re-employment). It contains the offline synthetic business state available at scenario start. The environment name is `career_espp_refund_recovery`, the scenario window is `2026-06-08` through `2026-08-25`, and the timezone is `Asia/Shanghai`.

## 关联任务 / Associated Task

- **Task / 任务:** `career/career_espp_refund_recovery`
- **中文标题 / Chinese title:** 离职员工持股计划赎回争议核对与再就业
- **English title / 英文标题:** ESPP Redemption Reconciliation and Re-employment
- **Service / 服务:** `banking`
- **Environment / 环境名:** `career_espp_refund_recovery`
- **Scenario window / 场景窗口:** `2026-06-08` → `2026-08-25`
- **Timezone / 时区:** `Asia/Shanghai`

## 场景作用 / Scenario Role

保存银行账户、收支流水、收款方与支付状态。

Stores bank accounts, cash-flow history, payees, and payment state.

## 初始数据 / Seed Contents

初始文件为 `init.sql`。下表的行数来自对应服务 SQLite schema 与 `init.sql` 的全新内存加载；包括空表，以明确初始状态边界。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| 业务表 / Table | 初始行数 / Initial Rows |
|---|---:|
| `_counters` | 4 |
| `accounts` | 2 |
| `payees` | 2 |
| `pending_payments` | 0 |
| `recurring_payments` | 0 |
| `transactions` | 240 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `transactions` | 240 | `tx_id` |
| `accounts` | 2 | `account_id` |
| `payees` | 2 | `payee_id` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 中有 1 个事件会更新此服务 / 1 events in `event.yaml` update this service:

| Stage | Time / 时间 | Kind / 类型 | Update method / 更新方式 |
|---:|---|---|---|
| 17 | `2026-07-16T08:00` | `mutation` | SQL file `s17_severance_deposit.sql` |

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 60032 bytes |

## 加载说明 / Loading

兼容运行时应将 `banking` 绑定到环境 `career_espp_refund_recovery`，从任务目录内的 `envs/banking/career_espp_refund_recovery/` 读取数据。本次数据审计使用外部服务实现提供的 `SCHEMA_SQL` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `banking` to environment `career_espp_refund_recovery` and read `envs/banking/career_espp_refund_recovery/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
