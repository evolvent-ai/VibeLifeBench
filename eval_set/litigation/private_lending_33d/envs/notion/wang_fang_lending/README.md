# `notion/wang_fang_lending`

## 中文说明

这是任务 `litigation/private_lending_33d`（民间借贷追偿一审与二审管理）使用的 task-local `notion` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `wang_fang_lending`。场景窗口为 `2026-05-20` 至 `2026-06-22`，时区为 `Asia/Shanghai`。

## English Summary

This is the task-local `notion` environment for `litigation/private_lending_33d` (Private Lending Recovery Litigation — 33 Days). It contains the offline synthetic business state available at scenario start. The environment name is `wang_fang_lending`, the scenario window is `2026-05-20` through `2026-06-22`, and the timezone is `Asia/Shanghai`.

## 关联任务 / Associated Task

- **Task / 任务:** `litigation/private_lending_33d`
- **中文标题 / Chinese title:** 民间借贷追偿一审与二审管理
- **English title / 英文标题:** Private Lending Recovery Litigation — 33 Days
- **Service / 服务:** `notion`
- **Environment / 环境名:** `wang_fang_lending`
- **Scenario window / 场景窗口:** `2026-05-20` → `2026-06-22`
- **Timezone / 时区:** `Asia/Shanghai`

## 场景作用 / Scenario Role

保存页面、数据库、区块以及持续维护的结构化记录。

Stores pages, databases, blocks, and durable structured records.

## 初始数据 / Seed Contents

初始文件为 `init.sql`。下表的行数来自对应服务 SQLite schema 与 `init.sql` 的全新内存加载；包括空表，以明确初始状态边界。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| 业务表 / Table | 初始行数 / Initial Rows |
|---|---:|
| `blocks` | 440 |
| `comments` | 0 |
| `counters` | 2 |
| `database_rows` | 0 |
| `databases` | 0 |
| `pages` | 221 |
| `users` | 2 |
| `workspaces` | 1 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `blocks` | 440 | `block_id` |
| `pages` | 221 | `page_id` |
| `counters` | 2 | `key` |
| `users` | 2 | `user_id` |
| `workspaces` | 1 | `workspace_id` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 中有 8 个事件会更新此服务 / 8 events in `event.yaml` update this service:

| Stage | Time / 时间 | Kind / 类型 | Update method / 更新方式 |
|---:|---|---|---|
| 0 | `2026-05-20T08:30:00+08:00` | `mutation` | SQL file `mutation_s0_case_home.sql` |
| 8 | `2026-06-01T09:30:00+08:00` | `mutation` | SQL file `mutation_s8_case_docket.sql` |
| 9 | `2026-06-02T09:20:00+08:00` | `mutation` | SQL file `mutation_s9_preservation_register.sql` |
| 10 | `2026-06-04T09:00:00+08:00` | `mutation` | SQL file `mutation_s10_defense_register.sql` |
| 13 | `2026-06-10T09:00:00+08:00` | `mutation` | SQL file `mutation_s13_lawyer_switch.sql` |
| 16 | `2026-06-16T09:50:00+08:00` | `mutation` | SQL file `mutation_s16_judgment_register.sql` |
| 18 | `2026-06-18T13:50:00+08:00` | `mutation` | SQL file `mutation_s18_second_instance.sql` |
| 19 | `2026-06-20T08:50:00+08:00` | `mutation` | SQL file `mutation_s19_appeal_response.sql` |

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 321851 bytes |
| `mutation_s0_case_home.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1927 bytes |
| `mutation_s10_defense_register.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1039 bytes |
| `mutation_s13_lawyer_switch.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1010 bytes |
| `mutation_s16_judgment_register.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1154 bytes |
| `mutation_s18_second_instance.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 900 bytes |
| `mutation_s19_appeal_response.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1040 bytes |
| `mutation_s8_case_docket.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 954 bytes |
| `mutation_s9_preservation_register.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1024 bytes |

## 加载说明 / Loading

兼容运行时应将 `notion` 绑定到环境 `wang_fang_lending`，从任务目录内的 `envs/notion/wang_fang_lending/` 读取数据。本次数据审计使用外部服务实现提供的 `SCHEMA_SQL` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `notion` to environment `wang_fang_lending` and read `envs/notion/wang_fang_lending/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
