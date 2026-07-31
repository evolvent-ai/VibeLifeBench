# 龙舟队新人上肢耐力准备
# Dragon Boat Newcomer Upper-Body Endurance Preparation

## 任务概述 / Task Overview

龙舟队新人上肢耐力准备任务，持续处理肩部疼痛降载、雷暴水上安全、队伍邮件授权、场地维护变化、健康数据真实性和最终跨服务复盘。

A long-horizon training task for a new dragon-boat paddler, covering upper-body endurance, shoulder-pain deloading, thunderstorm water safety, team authorization, venue changes, and health-data integrity.

- **Task ID:** `dragon_boat_newcomer_upper_body_endurance_037`
- **Category / 领域:** `fitness`
- **Difficulty / 难度:** `hard`
- **Language / 语言:** 中文与英文 / Chinese and English

## 任务目标 / Objectives

- 持续协调训练负荷、恢复、天气、场地和日历。 / Coordinate training load, recovery, weather, venue, and calendar state over time.
- 在疼痛、疲劳或安全条件变化时主动降载和复查。 / Deload and recheck proactively when pain, fatigue, or safety conditions change.
- 保持健康数据、授权记录和最终复盘的一致性。 / Keep health data, authorization records, and final review consistent.

## 场景与角色 / Scenario and Actors

本任务由一个持续存在的用户目标、相关个人或机构、多个结构化服务以及可写工作区共同构成。角色身份、初始背景、长期偏好和业务边界记录在 `workspace/` 中；Agent 需要在不重复询问已知信息的前提下持续维护状态。

The scenario combines a persistent user objective, relevant people or organizations, multiple structured services, and a writable workspace. Identity, initial context, long-term preferences, and operating boundaries are defined in `workspace/`; the agent is expected to maintain continuity without repeatedly asking for known information.

## 时间线 / Timeline

- **Scenario window / 场景时间:** `2026-07-06` → `2026-08-17`
- **Timezone / 时区:** `Asia/Shanghai`
- **Stages / 阶段数:** `28`
- **Events / 事件数:** `34`
- **Mutation events / 动态状态变更:** `12`

每个 Stage 是一个评分检查点，不必等同于自然日。事件可能包括用户消息、业务通知、外部世界变化和静默后端 mutation；Agent 必须基于当前可见状态行动，不能使用未来 Stage 的事实。

Each Stage is an evaluation checkpoint rather than necessarily a calendar day. Events may include user messages, business notifications, world changes, and silent backend mutations. The agent must act on currently visible state and must not rely on future-stage facts.

## 服务与环境 / Services and Environments

| Service | Task-local environment | Role / 作用 |
|---|---|---|
| `calendar` | `dragon_boat_newcomer_upper_body_endurance_037` | 日程、提醒、冲突与期限管理 / schedules, reminders, conflicts, and deadlines |
| `health_tracker` | `dragon_boat_newcomer_upper_body_endurance_037` | 训练、疲劳、疼痛与健康记录 / training, fatigue, pain, and health records |
| `weather` | `dragon_boat_newcomer_upper_body_endurance_037` | 天气、预警、海况和户外条件 / weather, alerts, sea state, and outdoor conditions |
| `email` | `dragon_boat_newcomer_upper_body_endurance_037` | 历史邮件、通知、草稿和往来证据 / historical mail, notices, drafts, and correspondence evidence |
| `notion` | `dragon_boat_newcomer_upper_body_endurance_037` | 结构化工作台、决策记录和持续归档 / structured workspace, decision records, and durable archival |
| `review_platform` | `dragon_boat_newcomer_upper_body_endurance_037` | 供应商、场地、商品或服务评价 / vendor, venue, product, or service reviews |

所有 seed 数据均位于本任务自己的 `envs/<service>/<env_name>/`，发布包不依赖共享顶层 env。

All seed data is stored under this task's own `envs/<service>/<env_name>/`; the release bundle does not rely on a shared top-level environment directory.

## 核心挑战 / Core Challenges

- **长程一致性 / Long-horizon consistency:** 在 `28` 个 Stage 中持续维护事实、决定、待办和证据。
- **跨服务核验 / Cross-service verification:** 不能依赖单一通知，需要结合多个后端和工作区记录交叉确认。
- **动态恢复 / Dynamic recovery:** mutation 发生后重新查询受影响状态，更新计划、日历、预算、风险或归档。
- **可观察结果 / Observable outcomes:** 评分关注工具调用、后端终态、持久化文件和用户可见回复之间的一致性。

The task tests durable state across many stages, cross-service verification, recovery after backend mutations, and consistency among tool use, backend outcomes, workspace artifacts, and user-facing responses.

## 动态事件 / Dynamic Events

`event.yaml` 定义 `34` 个事件，其中 `12` 个会直接改变可查询环境或工作区状态。`task.py` 按 Stage 和时间顺序分发事件，`mutations/` 或 event 内联操作负责落实后端变化。后续通知不能替代实际状态变更，Agent 需要主动复查受影响服务。

`event.yaml` defines 34 events, including 12 events that change queryable backend or workspace state. `task.py` dispatches them in Stage and timestamp order. Later notices do not substitute for actual state changes; the agent is expected to re-query affected services.

## 授权、安全与隐私边界 / Authorization, Safety, and Privacy

不得把训练建议包装为医学诊断；疼痛、雷暴、低温或明显疲劳出现时必须优先降低风险。 / Do not present training guidance as medical diagnosis; pain, thunderstorms, cold, or material fatigue must trigger risk reduction.

所有外部沟通、支付、签署、预订、提交或其他不可逆动作都必须区分“准备材料或草稿”与“真正执行”。敏感信息仅在完成当前任务所必需的最小范围内使用。

External communication, payment, signing, booking, submission, and other irreversible actions must distinguish preparation or drafting from actual execution. Sensitive data is used only to the minimum extent required for the current task.

## 工作区交付物 / Workspace Deliverables

初始工作区包含 18 个文件：`AGENTS.md`, `BUDGET_AUTH.md`, `HEALTH_BOUNDARIES.md`, `IDENTITY.md`, `PERSONA.md`, `PRIVACY.md`, `SOUL.md`, `TOOLS.md`, `TRAINING_PRINCIPLES.md`, `USER.md`, `auth_log.md`, `calendar_change_log.md`, `equipment_budget.md`, `final_review.md`, `risk_log.md`, `service_consistency_matrix.md`, `stage_progress.md`, `venue_weather_log.md`。这些文件提供角色、约束、工具使用原则和任务模板；运行过程中 Agent 需要按照场景要求更新或新增持久化记录。

The initial workspace contains 18 files: `AGENTS.md`, `BUDGET_AUTH.md`, `HEALTH_BOUNDARIES.md`, `IDENTITY.md`, `PERSONA.md`, `PRIVACY.md`, `SOUL.md`, `TOOLS.md`, `TRAINING_PRINCIPLES.md`, `USER.md`, `auth_log.md`, `calendar_change_log.md`, `equipment_budget.md`, `final_review.md`, `risk_log.md`, `service_consistency_matrix.md`, `stage_progress.md`, `venue_weather_log.md`. They define identity, constraints, tool-use principles, and task templates. During execution, the agent is expected to maintain or create durable records required by the scenario.

## 评分结构 / Scoring

- **Mode / 模式:** `flat_pool` — 原子检查加权汇总 / weighted aggregation of atomic checks
- **Atomic checks / 原子检查数:** `44`
- **Declared total weight / 声明总权重:** `68.5`

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
