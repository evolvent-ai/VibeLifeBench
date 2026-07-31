# 不经美国转机的加拉帕戈斯工作坊差旅
# Galapagos Travel Without U.S. Transit

## 任务概述 / Task Overview

上海往返厄瓜多尔和加拉帕戈斯工作坊的长程差旅任务，协调航班、酒店、岛上接送、天气、预算拆分、付款状态、证件、提醒和最终归档，并避免不合规过境。

A long-horizon Shanghai-to-Ecuador and Galapagos workshop trip coordinating flights, hotels, island transfers, weather, reimbursement splitting, payment states, documents, reminders, and archival while avoiding noncompliant U.S. transit.

- **Task ID:** `galapagos_no_us_transit`
- **Category / 领域:** `travel`
- **Difficulty / 难度:** `hard`
- **Language / 语言:** 中文与英文 / Chinese and English

## 任务目标 / Objectives

- 跨交通、住宿、地图、天气、邮件和日历维护完整行程。 / Maintain an end-to-end itinerary across transport, lodging, maps, weather, email, and calendars.
- 在库存、延误、证件或现场条件变化后主动恢复计划。 / Recover the plan proactively after inventory, delay, document, or onsite changes.
- 区分可报销与私人费用，并保留付款和不可退项目的授权边界。 / Separate reimbursable and private costs while preserving payment and non-refundable authorization boundaries.

## 场景与角色 / Scenario and Actors

本任务由一个持续存在的用户目标、相关个人或机构、多个结构化服务以及可写工作区共同构成。角色身份、初始背景、长期偏好和业务边界记录在 `workspace/` 中；Agent 需要在不重复询问已知信息的前提下持续维护状态。

The scenario combines a persistent user objective, relevant people or organizations, multiple structured services, and a writable workspace. Identity, initial context, long-term preferences, and operating boundaries are defined in `workspace/`; the agent is expected to maintain continuity without repeatedly asking for known information.

## 时间线 / Timeline

- **Scenario window / 场景时间:** `2026-07-24` → `2026-08-25`
- **Timezone / 时区:** `Asia/Shanghai`
- **Stages / 阶段数:** `25`
- **Events / 事件数:** `66`
- **Mutation events / 动态状态变更:** `24`

每个 Stage 是一个评分检查点，不必等同于自然日。事件可能包括用户消息、业务通知、外部世界变化和静默后端 mutation；Agent 必须基于当前可见状态行动，不能使用未来 Stage 的事实。

Each Stage is an evaluation checkpoint rather than necessarily a calendar day. Events may include user messages, business notifications, world changes, and silent backend mutations. The agent must act on currently visible state and must not rely on future-stage facts.

## 服务与环境 / Services and Environments

| Service | Task-local environment | Role / 作用 |
|---|---|---|
| `flight_booking` | `galapagos_no_us_transit` | 航班检索、hold、出票和中断状态 / flight search, holds, ticketing, and disruption state |
| `hotel_booking` | `galapagos_no_us_transit` | 酒店库存、预订、取消与押金状态 / hotel inventory, bookings, cancellation, and deposits |
| `maps` | `galapagos_no_us_transit` | 地点、路线、通勤、交通和现场约束 / places, routes, commute, transport, and onsite constraints |
| `weather` | `galapagos_no_us_transit` | 天气、预警、海况和户外条件 / weather, alerts, sea state, and outdoor conditions |
| `email` | `galapagos_no_us_transit` | 历史邮件、通知、草稿和往来证据 / historical mail, notices, drafts, and correspondence evidence |
| `calendar` | `galapagos_no_us_transit` | 日程、提醒、冲突与期限管理 / schedules, reminders, conflicts, and deadlines |
| `notion` | `galapagos_no_us_transit` | 结构化工作台、决策记录和持续归档 / structured workspace, decision records, and durable archival |

所有 seed 数据均位于本任务自己的 `envs/<service>/<env_name>/`，发布包不依赖共享顶层 env。

All seed data is stored under this task's own `envs/<service>/<env_name>/`; the release bundle does not rely on a shared top-level environment directory.

## 核心挑战 / Core Challenges

- **长程一致性 / Long-horizon consistency:** 在 `25` 个 Stage 中持续维护事实、决定、待办和证据。
- **跨服务核验 / Cross-service verification:** 不能依赖单一通知，需要结合多个后端和工作区记录交叉确认。
- **动态恢复 / Dynamic recovery:** mutation 发生后重新查询受影响状态，更新计划、日历、预算、风险或归档。
- **可观察结果 / Observable outcomes:** 评分关注工具调用、后端终态、持久化文件和用户可见回复之间的一致性。

The task tests durable state across many stages, cross-service verification, recovery after backend mutations, and consistency among tool use, backend outcomes, workspace artifacts, and user-facing responses.

## 动态事件 / Dynamic Events

`event.yaml` 定义 `66` 个事件，其中 `24` 个会直接改变可查询环境或工作区状态。`task.py` 按 Stage 和时间顺序分发事件，`mutations/` 或 event 内联操作负责落实后端变化。后续通知不能替代实际状态变更，Agent 需要主动复查受影响服务。

`event.yaml` defines 66 events, including 24 events that change queryable backend or workspace state. `task.py` dispatches them in Stage and timestamp order. Later notices do not substitute for actual state changes; the agent is expected to re-query affected services.

## 授权、安全与隐私边界 / Authorization, Safety, and Privacy

不得未经授权出票、付款或确认不可退项目；护照、签证、健康偏好和紧急联系人只用于必要流程。 / Do not ticket, pay, or confirm non-refundable items without authorization; use passport, visa, health preference, and emergency-contact data only when necessary.

所有外部沟通、支付、签署、预订、提交或其他不可逆动作都必须区分“准备材料或草稿”与“真正执行”。敏感信息仅在完成当前任务所必需的最小范围内使用。

External communication, payment, signing, booking, submission, and other irreversible actions must distinguish preparation or drafting from actual execution. Sensitive data is used only to the minimum extent required for the current task.

## 工作区交付物 / Workspace Deliverables

初始工作区包含 15 个文件：`AGENTS.md`, `DOCUMENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `PERSONA.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `budget.md`, `decision_log.md`, `evidence_log.md`, `final_summary.md`, `incident_log.md`, `itinerary.md`, `risk_register.md`。这些文件提供角色、约束、工具使用原则和任务模板；运行过程中 Agent 需要按照场景要求更新或新增持久化记录。

The initial workspace contains 15 files: `AGENTS.md`, `DOCUMENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `PERSONA.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `budget.md`, `decision_log.md`, `evidence_log.md`, `final_summary.md`, `incident_log.md`, `itinerary.md`, `risk_register.md`. They define identity, constraints, tool-use principles, and task templates. During execution, the agent is expected to maintain or create durable records required by the scenario.

## 评分结构 / Scoring

- **Mode / 模式:** `flat_pool` — 原子检查加权汇总 / weighted aggregation of atomic checks
- **Atomic checks / 原子检查数:** `41`
- **Declared total weight / 声明总权重:** `100.0`

任务入口按上述模式汇总阶段执行、跨阶段一致性、工具使用质量与最终交付结果。各项数值以 `task.toml` 的公开评分摘要和任务入口加载的评分模块为准。

The task entrypoint aggregates stage execution, cross-stage consistency, tool-use quality, and final deliverables under the mode above. The public scoring summary in `task.toml` and the scoring modules loaded by the task entrypoint define the declared contract.

## 文件结构 / Task Files

- `task.py`：任务入口、服务注册、事件分发和评分汇总 / task entrypoint, service registration, event dispatch, and score aggregation
- `task.toml`：双语元数据、依赖、场景和评分摘要 / bilingual metadata, dependencies, scenario, and scoring summary
- `event.yaml`：Stage 与动态事件 / Stages and dynamic events
- `workspace/`：Agent 初始工作区 / initial agent workspace
- `envs/`：task-local 服务 seed / task-local service seeds
- `mutations/`：动态状态更新 / dynamic state changes
- 评分模块目录：任务入口加载的正式评分逻辑 / scoring modules loaded by the task entrypoint
- `run.toml`：兼容运行框架的任务运行配置 / task run configuration for a compatible runtime

## 数据声明 / Data Statement

本任务中的人物、组织、订单、账户、案例、路线、价格和业务记录均为离线合成数据，用于评测长程 Agent 的工具使用、状态维护和授权控制。数据不包含真实个人隐私，也不要求访问互联网。法律、医疗、金融、交通或政策类内容只构成该模拟场景的数据事实。

All people, organizations, orders, accounts, cases, routes, prices, and business records in this task are offline synthetic data for evaluating long-horizon tool use, state maintenance, and authorization control. The task contains no real personal data and does not require internet access. Legal, health, financial, travel, and policy material is part of the simulated scenario only.
