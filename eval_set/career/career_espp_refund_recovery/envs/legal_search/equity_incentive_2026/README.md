# `legal_search/equity_incentive_2026`

## 中文说明

这是任务 `career/career_espp_refund_recovery`（离职员工持股计划赎回争议核对与再就业）使用的 task-local `legal_search` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `equity_incentive_2026`。场景窗口为 `2026-06-08` 至 `2026-08-25`，时区为 `Asia/Shanghai`。

## English Summary

This is the task-local `legal_search` environment for `career/career_espp_refund_recovery` (ESPP Redemption Reconciliation and Re-employment). It contains the offline synthetic business state available at scenario start. The environment name is `equity_incentive_2026`, the scenario window is `2026-06-08` through `2026-08-25`, and the timezone is `Asia/Shanghai`.

## 关联任务 / Associated Task

- **Task / 任务:** `career/career_espp_refund_recovery`
- **中文标题 / Chinese title:** 离职员工持股计划赎回争议核对与再就业
- **English title / 英文标题:** ESPP Redemption Reconciliation and Re-employment
- **Service / 服务:** `legal_search`
- **Environment / 环境名:** `equity_incentive_2026`
- **Scenario window / 场景窗口:** `2026-06-08` → `2026-08-25`
- **Timezone / 时区:** `Asia/Shanghai`

## 场景作用 / Scenario Role

保存法规、政策、案例、检索索引与收藏记录。

Stores statutes, policies, cases, search indexes, and saved legal records.

## 初始数据 / Seed Contents

初始文件为 `init.sql`。下表的行数来自对应服务 SQLite schema 与 `init.sql` 的全新内存加载；包括空表，以明确初始状态边界。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| 业务表 / Table | 初始行数 / Initial Rows |
|---|---:|
| `_counters` | 2 |
| `cases` | 76 |
| `citations` | 117 |
| `courts` | 10 |
| `saved_cases` | 2 |
| `statute_articles` | 18 |
| `statutes` | 3 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `citations` | 117 | `citation_id` |
| `cases` | 76 | `case_id` |
| `statute_articles` | 18 | `article_id` |
| `courts` | 10 | `court_id` |
| `statutes` | 3 | `statute_id` |
| `saved_cases` | 2 | `saved_id` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 未声明直接写入此服务的阶段更新；运行期间由 Agent 工具调用产生的状态变化仍由兼容运行时持久化。

No staged event directly writes this service in `event.yaml`; state changes caused by agent tool calls are still persisted by the compatible runtime.

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 98232 bytes |

## 加载说明 / Loading

兼容运行时应将 `legal_search` 绑定到环境 `equity_incentive_2026`，从任务目录内的 `envs/legal_search/equity_incentive_2026/` 读取数据。本次数据审计使用外部服务实现提供的 `SCHEMA_SQL` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `legal_search` to environment `equity_incentive_2026` and read `envs/legal_search/equity_incentive_2026/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
