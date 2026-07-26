# `credit_card/hsa_medical_bill_liquidity_guard_30d`

## 中文说明

这是任务 `finance/hsa_medical_bill_liquidity_guard_30d`（HSA 医疗账单与流动性防护计划）使用的 task-local `credit_card` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `hsa_medical_bill_liquidity_guard_30d`。场景窗口为 `2026-06-15` 至 `2026-07-05`，时区为 `America/Phoenix`。

## English Summary

This is the task-local `credit_card` environment for `finance/hsa_medical_bill_liquidity_guard_30d` (HSA Medical Bill Liquidity Guard — 30-Day Plan). It contains the offline synthetic business state available at scenario start. The environment name is `hsa_medical_bill_liquidity_guard_30d`, the scenario window is `2026-06-15` through `2026-07-05`, and the timezone is `America/Phoenix`.

## 关联任务 / Associated Task

- **Task / 任务:** `finance/hsa_medical_bill_liquidity_guard_30d`
- **中文标题 / Chinese title:** HSA 医疗账单与流动性防护计划
- **English title / 英文标题:** HSA Medical Bill Liquidity Guard — 30-Day Plan
- **Service / 服务:** `credit_card`
- **Environment / 环境名:** `hsa_medical_bill_liquidity_guard_30d`
- **Scenario window / 场景窗口:** `2026-06-15` → `2026-07-05`
- **Timezone / 时区:** `America/Phoenix`

## 场景作用 / Scenario Role

保存信用卡账户、账单、交易、支付与争议状态。

Stores card accounts, statements, transactions, payments, and dispute state.

## 初始数据 / Seed Contents

初始文件为 `init.sql`。下表的行数来自对应服务 SQLite schema 与 `init.sql` 的全新内存加载；包括空表，以明确初始状态边界。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| 业务表 / Table | 初始行数 / Initial Rows |
|---|---:|
| `_counters` | 3 |
| `cards` | 2 |
| `disputes` | 2 |
| `payments` | 20 |
| `rewards_balances` | 2 |
| `rewards_ledger` | 42 |
| `statement_lines` | 235 |
| `statements` | 24 |
| `unbilled_transactions` | 40 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `statement_lines` | 235 | `line_id` |
| `rewards_ledger` | 42 | `ledger_id` |
| `unbilled_transactions` | 40 | `tx_id` |
| `statements` | 24 | `statement_id` |
| `payments` | 20 | `payment_id` |
| `cards` | 2 | `card_id` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 中有 2 个事件会更新此服务 / 2 events in `event.yaml` update this service:

| Stage | Time / 时间 | Kind / 类型 | Update method / 更新方式 |
|---:|---|---|---|
| 5 | `2026-06-18T08:00` | `mutation` | inline `insert` on `unbilled_transactions`; inline `update` on `cards` |
| 18 | `2026-06-30T08:30` | `mutation` | inline `insert` on `unbilled_transactions`; inline `update` on `cards` |

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 97178 bytes |

## 加载说明 / Loading

兼容运行时应将 `credit_card` 绑定到环境 `hsa_medical_bill_liquidity_guard_30d`，从任务目录内的 `envs/credit_card/hsa_medical_bill_liquidity_guard_30d/` 读取数据。本次数据审计使用外部服务实现提供的 `SCHEMA_SQL` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `credit_card` to environment `hsa_medical_bill_liquidity_guard_30d` and read `envs/credit_card/hsa_medical_bill_liquidity_guard_30d/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
