# Agent 操作指南

本任务是长周期旅行运营任务。目标不是一次性给攻略，而是持续维护可执行、可恢复、可审计的旅行状态。

## 启动时要做

1. 阅读 `USER.md`、`DOCUMENTS.md`、`TOOLS.md`、`PERSONA.md`、`SOUL.md`、`IDENTITY.md`。OpenClaw 的主 workspace 通常是 `/terrarium/openclaw/workspace`；若 `/workspace/DOCUMENTS.md` 不存在，改读 `/terrarium/openclaw/workspace/DOCUMENTS.md` 或相对路径 `DOCUMENTS.md`。
2. 建立或维护 Notion journal：`Galapagos Workshop Trip 2026 - Journal`。
3. 创建并持续更新必要的 workspace 文件。
4. 每次收到新消息或通知后，先复查相关长期状态，再决定是否需要查工具或执行授权内动作。

## 需要维护的 workspace 文件

- `/workspace/itinerary.md`：航班、酒店、接送、登记和返程时间线。
- `/workspace/decision_log.md`：重要取舍、选项、推荐理由和授权状态。
- `/workspace/risk_register.md`：证件、过境、天气、航班、接送、付款和健康舒适度风险。
- `/workspace/budget.md`：会议可报销费用、私人费用、共同费用和状态。
- `/workspace/evidence_log.md`：邮件、行程单、酒店确认、接送凭证、支付和收据。
- `/workspace/incident_log.md`：途中突发事件、处理动作和结果。
- `/workspace/final_summary.md`：返程后的最终归档。
- `/workspace/HEARTBEAT.md`：每个检查点的当前状态、待办、阻塞和下一次复查。
- `/workspace/DOCUMENTS.md` 或 `/terrarium/openclaw/workspace/DOCUMENTS.md`：用户上传的证件、签证、会议邀请、付款授权和邮件要点，只读参考。

## 工作原则

- 不要只在回复里承诺记录；需要长期保留的信息要写入 workspace 或 Notion。
- 查询结果要转化成可执行结论：谁、何时、去哪、状态是什么、还差什么。
- 航班、酒店、天气、接送、邮件和支付状态会变化；关键节点要主动复查工具。
- 任何低价方案都要和证件、过境、衔接、取消政策、准时登记和安全一起比较。
- 对未授权的不可逆动作，只能说明风险、选项和建议，不能擅自执行。
- 不要向用户暴露内部实现细节、数据库原始长表或完整日志。

## 每次处理事件的建议顺序

1. 读取近期 workspace 状态和 Notion journal。
2. 判断本次事件涉及哪些系统：航班、酒店、地图、天气、邮件、日历、费用或证件。
3. 调用必要工具核验当前状态。
4. 如果在授权范围内，执行 hold、提醒、记录或更新。
5. 更新相关 workspace 文件和 Notion。
6. 给用户短回复：结论、动作、风险、下一步。

## 状态命名

统一使用以下状态，避免混淆：

- `candidate`：候选方案。
- `held`：已 hold，还未付款或出票。
- `booked`：已预订。
- `ticketed`：已出票。
- `paid`：已付款。
- `frozen`：预授权或押金冻结。
- `pending confirmation`：待确认。
- `pending refund`：待退款或押金释放。
- `settled`：已结清。

## 最终归档要求

返程后需要形成完整归档，至少包括：

- 实际航班、酒店、接送和登记结果。
- 会议可报销、私人费用、共同费用和待退项目。
- 发生过的风险、触发时间、处理动作和结果。
- 凭证清单及缺失项。
- 下次类似岛屿/跨国工作坊旅行 checklist。
