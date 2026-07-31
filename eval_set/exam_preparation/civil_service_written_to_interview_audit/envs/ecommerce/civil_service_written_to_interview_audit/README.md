# `ecommerce/civil_service_written_to_interview_audit`

## 中文说明

这是任务 `exam_preparation/civil_service_written_to_interview_audit`（公务员笔试到面试资格审核长程管理）使用的 task-local `ecommerce` 环境。它保存场景起点可用的离线合成业务状态，环境名为 `civil_service_written_to_interview_audit`。场景窗口为 `2026-07-08` 至 `2026-08-31`，时区为 `Asia/Shanghai`。

## English Summary

This is the task-local `ecommerce` environment for `exam_preparation/civil_service_written_to_interview_audit` (Civil Service Written Exam to Interview Qualification Audit). It contains the offline synthetic business state available at scenario start. The environment name is `civil_service_written_to_interview_audit`, the scenario window is `2026-07-08` through `2026-08-31`, and the timezone is `Asia/Shanghai`.

## 关联任务 / Associated Task

- **Task / 任务:** `exam_preparation/civil_service_written_to_interview_audit`
- **中文标题 / Chinese title:** 公务员笔试到面试资格审核长程管理
- **English title / 英文标题:** Civil Service Written Exam to Interview Qualification Audit
- **Service / 服务:** `ecommerce`
- **Environment / 环境名:** `civil_service_written_to_interview_audit`
- **Scenario window / 场景窗口:** `2026-07-08` → `2026-08-31`
- **Timezone / 时区:** `Asia/Shanghai`

## 场景作用 / Scenario Role

保存商品、购物车、订单、优惠、退款与售后状态。

Stores products, carts, orders, promotions, refunds, and after-sales state.

## 初始数据 / Seed Contents

初始文件为 `init.sql`。下表的行数来自对应服务 SQLite schema 与 `init.sql` 的全新内存加载；包括空表，以明确初始状态边界。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| 业务表 / Table | 初始行数 / Initial Rows |
|---|---:|
| `_counters` | 0 |
| `addresses` | 0 |
| `applied_coupons` | 0 |
| `cart_items` | 0 |
| `carts` | 1 |
| `coupons` | 0 |
| `order_items` | 0 |
| `order_status_history` | 0 |
| `orders` | 0 |
| `products` | 230 |
| `refunds` | 0 |
| `skus` | 230 |
| `stocks` | 230 |

## 关键对象 / Key Entities

以下列出初始快照中行数较多的主要业务表及其主键字段；它们是普通场景实体，不代表预设结论。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| 业务表 / Table | 初始行数 / Initial Rows | 主键字段 / Primary Key |
|---|---:|---|
| `products` | 230 | `product_id` |
| `skus` | 230 | `sku_id` |
| `stocks` | 230 | `sku_id` |
| `carts` | 1 | `user_id` |

## 初始状态与动态变化 / Initial State and Mutations

`init.*` 只描述事件时间线应用前的初始状态。后续状态变化必须按 `event.yaml` 的 Stage 与时间顺序应用，不能视为已存在于初始 seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` 未声明直接写入此服务的阶段更新；运行期间由 Agent 工具调用产生的状态变化仍由兼容运行时持久化。

No staged event directly writes this service in `event.yaml`; state changes caused by agent tool calls are still persisted by the compatible runtime.

## 文件说明 / Files

| File / 文件 | Purpose / 用途 | Size / 大小 |
|---|---|---:|
| `init.sql` | SQLite 初始 seed / initial SQLite seed | 174753 bytes |

## 加载说明 / Loading

兼容运行时应将 `ecommerce` 绑定到环境 `civil_service_written_to_interview_audit`，从任务目录内的 `envs/ecommerce/civil_service_written_to_interview_audit/` 读取数据。本次数据审计使用外部服务实现提供的 `SCHEMA_SQL` 建表，并加载 `init.sql`；SQLite `integrity_check` 为 `ok`，外键检查为 0 条。若目录包含 `init.json` 或 JSONL 文件，运行时还应按对应服务的数据加载约定保留并读取这些结构化文件。此 task-only 发布包不包含服务实现或执行框架。

A compatible runtime should bind `ecommerce` to environment `civil_service_written_to_interview_audit` and read `envs/ecommerce/civil_service_written_to_interview_audit/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## 数据与隐私声明 / Data and Privacy

本环境中的人物、组织、账号、订单、消息、地点、价格、政策摘要和业务记录均为离线合成数据。文件不包含真实个人隐私，也不需要访问互联网。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
