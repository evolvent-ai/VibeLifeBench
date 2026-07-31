# 可用工具与使用方式

先读取，再修改；修改后重新读取确认结果。工具返回的 application ID、event ID、
page ID、document ID 和时间戳应写入项目记录。

## Email

- `get_emails`、`read_email`、`search_emails`：读取和检索邮件。
- `send_email`、`reply_email`、`forward_email`：发送有明确收件人、问题和期限的邮件。
- `save_draft`、`get_drafts`、`update_draft`：在需要批准时保存草稿。

## Calendar

- `list_calendars`、`list_events`、`get_event`、`search_events`：核对已有安排。
- `create_event`、`update_event`、`delete_event`：维护施工、交付、检查和复测日历。

创建或更新前，应检查物业噪音时段、周末许可、货梯预约、前置工作和监管人员可用期。

## Visa and Advisory（商业合规映射）

- `get_visa_application`、`list_visa_applications`：读取备案、消防、强弱电、保险和
  物业交接申请的实时状态、历史和文件。
- `upload_document`：向现有申请上传工作区文档引用。
- `submit_visa_application`：提交已有申请的表单答案和材料。
- `get_advisory`：读取当前物业或区域通告。

本服务中的 application 代表商业审批流程。不得把发邮件或修改工作区当作官方状态
已经变化；必须重新查询申请确认。

## Notion（项目知识库）

工具名以服务实际暴露的 API 名称为准：

- `API-post-search`
- `API-post-database-query`
- `API-retrieve-a-page`
- `API-retrieve-a-page-property`
- `API-post-page`
- `API-patch-page`
- `API-get-block-children`
- `API-patch-block-children`

用于查询物业规则、供应商、材料、项目状态和问题台账。修改页面前先读取当前属性，
避免覆盖他人更新。

## 其他服务

- Maps：核对供应商位置和现场通勤可行性。
- Hotel booking：在本项目中用于可取消的供应商或服务包占位；确认价格、取消条款和
  状态后再记录为承诺。
- Weather：安排材料进场和受天气影响的工序。
- Workspace：维护项目文件和证据引用。

如果工具调用失败，不得把目标状态写成成功；记录错误并在决定前重试或升级。
