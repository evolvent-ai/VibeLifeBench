# `weather/broadcast_exam_posture_breathing_32d`

## 中文说明

这是任务 `fitness/broadcast_exam_posture_breathing_32d`（播音主持艺考生姿态呼吸与考前减量维护）使用的 task-local `weather` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `broadcast_exam_posture_breathing_32d`。场景窗口为 `2026-10-05` 至 `2026-11-05`，时区为 `Asia/Shanghai`。

## English Summary

This is the task-local `weather` environment for `fitness/broadcast_exam_posture_breathing_32d` (Broadcast Arts Exam Posture, Breathing, and Taper Maintenance). It contains the offline synthetic business state available at scenario start. The environment name is `broadcast_exam_posture_breathing_32d`, the scenario window is `2026-10-05` through `2026-11-05`, and the timezone is `Asia/Shanghai`.

## 关联任务 / Associated Task

- **Task / 任务:** `fitness/broadcast_exam_posture_breathing_32d`
- **中文标题 / Chinese title:** 播音主持艺考生姿态呼吸与考前减量维护
- **English title / 英文标题:** Broadcast Arts Exam Posture, Breathing, and Taper Maintenance
- **Service / 服务:** `weather`
- **Environment / 环境名:** `broadcast_exam_posture_breathing_32d`
- **Scenario window / 场景窗口:** `2026-10-05` → `2026-11-05`
- **Timezone / 时区:** `Asia/Shanghai`

## 场景作用 / Scenario Role

保存地点天气、预报、预警与观测数据。

Stores location weather, forecasts, alerts, and observations.

## 初始数据 / Seed Contents

初始文件为 `init.sql`。下表的行数来自对应服务 SQLite schema 与 `init.sql` 的全新内存加载；包括空表，以明确初始状态边界。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| 业务表 / Table | 初始行数 / Initial Rows |
|---|---:|
| `_counters` | 2 |
| `_sim_clock` | 0 |
| `alert_subscriptions` | 0 |
| `alerts` | 0 |
| `climate_profiles` | 1 |
| `daily_aqi` | 15 |
| `daily_weather` | 15 |
| `hourly_weather` | 108 |
| `locations` | 1 |
| `notifications` | 0 |
| `typhoon_tracks` | 0 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `hourly_weather` | 108 | `geo_key`, `datetime` |
| `daily_aqi` | 15 | `geo_key`, `date` |
| `daily_weather` | 15 | `geo_key`, `date` |
| `climate_profiles` | 1 | `profile_id` |
| `locations` | 1 | `geo_key` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 中有 3 个事件会更新此服务 / 3 events in `event.yaml` update this service:

| Stage | Time / 时间 | Kind / 类型 | Update method / 更新方式 |
|---:|---|---|---|
| 11 | `2026-10-18T16:59:00+08:00` | `mutation` | SQL file `s11_weather_cold_wind_watch.sql` |
| 12 | `2026-10-19T06:20:00+08:00` | `mutation` | SQL file `s12_weather_cold_front.sql` |
| 23 | `2026-11-01T07:59:00+08:00` | `mutation` | SQL file `s23_weather_exam_cold_rain.sql` |

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 76473 bytes |

## 加载说明 / Loading

兼容运行时应将 `weather` 绑定到环境 `broadcast_exam_posture_breathing_32d`，从任务目录内的 `envs/weather/broadcast_exam_posture_breathing_32d/` 读取数据。本次数据审计使用外部服务实现提供的 `DDL` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `weather` to environment `broadcast_exam_posture_breathing_32d` and read `envs/weather/broadcast_exam_posture_breathing_32d/` from the task directory. For this data audit, the external service implementation supplied `DDL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
