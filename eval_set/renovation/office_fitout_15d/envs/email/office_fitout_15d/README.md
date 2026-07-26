# `email/office_fitout_15d`

## 中文说明

这是任务 `renovation/office_fitout_15d`（商业办公室 Fit-out 项目管理）使用的 task-local `email` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `office_fitout_15d`。场景窗口为 `2026-07-01` 至 `2026-09-01`，时区为 `Asia/Shanghai`。

## English Summary

This is the task-local `email` environment for `renovation/office_fitout_15d` (Commercial Office Fit-Out Project Management). It contains the offline synthetic business state available at scenario start. The environment name is `office_fitout_15d`, the scenario window is `2026-07-01` through `2026-09-01`, and the timezone is `Asia/Shanghai`.

## 关联任务 / Associated Task

- **Task / 任务:** `renovation/office_fitout_15d`
- **中文标题 / Chinese title:** 商业办公室 Fit-out 项目管理
- **English title / 英文标题:** Commercial Office Fit-Out Project Management
- **Service / 服务:** `email`
- **Environment / 环境名:** `office_fitout_15d`
- **Scenario window / 场景窗口:** `2026-07-01` → `2026-09-01`
- **Timezone / 时区:** `Asia/Shanghai`

## 场景作用 / Scenario Role

保存邮箱文件夹、消息、会话、附件与草稿状态。

Stores mail folders, messages, threads, attachments, and drafts.

## 初始数据 / Seed Contents

初始文件为 `init.json`、`init.sql`。下表的行数来自对应服务 SQLite schema 与 `init.sql` 的全新内存加载；包括空表，以明确初始状态边界。

Initial files: `init.json`, `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| 业务表 / Table | 初始行数 / Initial Rows |
|---|---:|
| `_counters` | 0 |
| `account_config` | 1 |
| `attachments` | 0 |
| `drafts` | 0 |
| `folders` | 3 |
| `messages` | 4 |
| `sent_log` | 0 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `messages` | 4 | `id` |
| `folders` | 3 | `id` |
| `account_config` | 1 | `id` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 未声明直接写入此服务的阶段更新；运行期间由 Agent 工具调用产生的状态变化仍由兼容运行时持久化。

No staged event directly writes this service in `event.yaml`; state changes caused by agent tool calls are still persisted by the compatible runtime.

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.json` | 结构化初始 seed / structured initial seed | 8466 bytes |
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 7236 bytes |

## 加载说明 / Loading

兼容运行时应将 `email` 绑定到环境 `office_fitout_15d`，从任务目录内的 `envs/email/office_fitout_15d/` 读取数据。本次数据审计使用外部服务实现提供的 `SCHEMA_SQL` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `email` to environment `office_fitout_15d` and read `envs/email/office_fitout_15d/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
