# `maps/wheelchair_student_accessible_rental`

## 中文说明

这是任务 `rental/wheelchair_student_accessible_rental`（轮椅学生的校园无障碍住房）使用的 task-local `maps` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `wheelchair_student_accessible_rental`。场景窗口为 `2026-07-14` 至 `2026-08-24`，时区为 `Asia/Shanghai`。

## English Summary

This is the task-local `maps` environment for `rental/wheelchair_student_accessible_rental` (Accessible Campus Housing for a Wheelchair-Using Student). It contains the offline synthetic business state available at scenario start. The environment name is `wheelchair_student_accessible_rental`, the scenario window is `2026-07-14` through `2026-08-24`, and the timezone is `Asia/Shanghai`.

## 关联任务 / Associated Task

- **Task / 任务:** `rental/wheelchair_student_accessible_rental`
- **中文标题 / Chinese title:** 轮椅学生的校园无障碍住房
- **English title / 英文标题:** Accessible Campus Housing for a Wheelchair-Using Student
- **Service / 服务:** `maps`
- **Environment / 环境名:** `wheelchair_student_accessible_rental`
- **Scenario window / 场景窗口:** `2026-07-14` → `2026-08-24`
- **Timezone / 时区:** `Asia/Shanghai`

## 场景作用 / Scenario Role

保存地点、道路、公共交通、路线与临时通行事件。

Stores places, roads, public transit, routes, and temporary mobility events.

## 初始数据 / Seed Contents

初始文件为 `init.sql`。下表的行数来自对应服务 SQLite schema 与 `init.sql` 的全新内存加载；包括空表，以明确初始状态边界。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| 业务表 / Table | 初始行数 / Initial Rows |
|---|---:|
| `notifications` | 0 |
| `place_reviews` | 0 |
| `places` | 230 |
| `road_events` | 2 |
| `roads` | 3 |
| `transit_events` | 2 |
| `transit_lines` | 3 |
| `transit_schedule` | 100 |
| `transit_stops` | 8 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `places` | 230 | `place_id` |
| `transit_schedule` | 100 | `schedule_id` |
| `transit_stops` | 8 | `stop_id` |
| `roads` | 3 | `road_id` |
| `transit_lines` | 3 | `line_id` |
| `road_events` | 2 | `event_id` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 中有 6 个事件会更新此服务 / 6 events in `event.yaml` update this service:

| Stage | Time / 时间 | Kind / 类型 | Update method / 更新方式 |
|---:|---|---|---|
| 6 | `2026-07-20T08:50:00+08:00` | `mutation` | SQL file `stage06_maps_route.sql` |
| 9 | `2026-07-23T08:50:00+08:00` | `mutation` | SQL file `stage09_clear_route.sql` |
| 12 | `2026-07-26T08:50:00+08:00` | `mutation` | SQL file `stage12_maps_gate.sql` |
| 16 | `2026-07-30T08:50:00+08:00` | `mutation` | SQL file `stage16_clear_gate.sql` |
| 18 | `2026-08-01T08:50:00+08:00` | `mutation` | SQL file `stage18_maps_late_route.sql` |
| 22 | `2026-08-11T08:50:00+08:00` | `mutation` | SQL file `stage22_clear_route.sql` |

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 88580 bytes |

## 加载说明 / Loading

兼容运行时应将 `maps` 绑定到环境 `wheelchair_student_accessible_rental`，从任务目录内的 `envs/maps/wheelchair_student_accessible_rental/` 读取数据。本次数据审计使用外部服务实现提供的 `SCHEMA_SQL` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `maps` to environment `wheelchair_student_accessible_rental` and read `envs/maps/wheelchair_student_accessible_rental/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
