# `email/wang_fang_lending`

## 中文说明

这是任务 `litigation/private_lending_33d`（民间借贷追偿一审与二审管理）使用的 task-local `email` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `wang_fang_lending`。场景窗口为 `2026-05-20` 至 `2026-06-22`，时区为 `Asia/Shanghai`。

## English Summary

This is the task-local `email` environment for `litigation/private_lending_33d` (Private Lending Recovery Litigation — 33 Days). It contains the offline synthetic business state available at scenario start. The environment name is `wang_fang_lending`, the scenario window is `2026-05-20` through `2026-06-22`, and the timezone is `Asia/Shanghai`.

## 关联任务 / Associated Task

- **Task / 任务:** `litigation/private_lending_33d`
- **中文标题 / Chinese title:** 民间借贷追偿一审与二审管理
- **English title / 英文标题:** Private Lending Recovery Litigation — 33 Days
- **Service / 服务:** `email`
- **Environment / 环境名:** `wang_fang_lending`
- **Scenario window / 场景窗口:** `2026-05-20` → `2026-06-22`
- **Timezone / 时区:** `Asia/Shanghai`

## 场景作用 / Scenario Role

保存邮箱文件夹、消息、会话、附件与草稿状态。

Stores mail folders, messages, threads, attachments, and drafts.

## 初始数据 / Seed Contents

初始文件为 `init.sql`。下表的行数来自对应服务 SQLite schema 与 `init.sql` 的全新内存加载；包括空表，以明确初始状态边界。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| 业务表 / Table | 初始行数 / Initial Rows |
|---|---:|
| `_counters` | 1 |
| `account_config` | 1 |
| `attachments` | 0 |
| `drafts` | 0 |
| `folders` | 7 |
| `messages` | 211 |
| `sent_log` | 0 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `messages` | 211 | `id` |
| `folders` | 7 | `id` |
| `account_config` | 1 | `id` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 中有 10 个事件会更新此服务 / 10 events in `event.yaml` update this service:

| Stage | Time / 时间 | Kind / 类型 | Update method / 更新方式 |
|---:|---|---|---|
| 4 | `2026-05-24T09:20:00+08:00` | `mutation` | SQL file `mutation_s4_bank_record_ready.sql` |
| 7 | `2026-05-30T09:00:00+08:00` | `mutation` | SQL file `mutation_s7_jurisdiction_objection.sql` |
| 8 | `2026-06-01T09:30:00+08:00` | `mutation` | SQL file `mutation_s8_case_accepted.sql` |
| 9 | `2026-06-02T09:20:00+08:00` | `mutation` | SQL file `mutation_s9_evidence_preservation.sql` |
| 10 | `2026-06-04T09:00:00+08:00` | `mutation` | SQL file `mutation_s10_defense.sql` |
| 12 | `2026-06-08T09:40:00+08:00` | `mutation` | SQL file `mutation_s12_hearing_notice.sql` |
| 13 | `2026-06-10T09:00:00+08:00` | `mutation` | SQL file `mutation_s13_lawyer_conflict.sql` |
| 16 | `2026-06-16T09:50:00+08:00` | `mutation` | SQL file `mutation_s16_judgment_delivery.sql` |
| 18 | `2026-06-18T13:50:00+08:00` | `mutation` | SQL file `mutation_s18_appeal_delivery.sql` |
| 19 | `2026-06-20T08:50:00+08:00` | `mutation` | SQL file `mutation_s19_second_instance_delivery.sql` |

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 103502 bytes |
| `mutation_s10_defense.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1154 bytes |
| `mutation_s12_hearing_notice.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1108 bytes |
| `mutation_s13_lawyer_conflict.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1122 bytes |
| `mutation_s16_judgment_delivery.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1209 bytes |
| `mutation_s18_appeal_delivery.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1088 bytes |
| `mutation_s19_second_instance_delivery.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1159 bytes |
| `mutation_s4_bank_record_ready.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1106 bytes |
| `mutation_s7_jurisdiction_objection.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1107 bytes |
| `mutation_s8_case_accepted.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1153 bytes |
| `mutation_s9_evidence_preservation.sql` | 由事件时间线引用的阶段更新 / staged update referenced by the event timeline | 1156 bytes |

## 加载说明 / Loading

兼容运行时应将 `email` 绑定到环境 `wang_fang_lending`，从任务目录内的 `envs/email/wang_fang_lending/` 读取数据。本次数据审计使用外部服务实现提供的 `SCHEMA_SQL` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `email` to environment `wang_fang_lending` and read `envs/email/wang_fang_lending/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
