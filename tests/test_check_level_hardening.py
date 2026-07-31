from __future__ import annotations

import asyncio
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "eval_set"


def _load_rubric(task: str, module_name: str, alias: str) -> ModuleType:
    task_root = EVAL / task
    package_name = f"_hardening_{alias}_rubrics"
    package = ModuleType(package_name)
    package.__path__ = [str(task_root / "rubrics")]  # type: ignore[attr-defined]
    sys.modules[package_name] = package
    qualified = f"{package_name}.{module_name}"
    spec = importlib.util.spec_from_file_location(
        qualified, task_root / "rubrics" / f"{module_name}.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[qualified] = module
    spec.loader.exec_module(module)
    return module


class FakeFS:
    def __init__(self, files: dict[str, str] | None = None):
        self.files = dict(files or {})

    def exists(self, path: str) -> bool:
        return path in self.files

    def read_file(self, path: str) -> bytes:
        if path not in self.files:
            raise FileNotFoundError(path)
        return self.files[path].encode("utf-8")

    def list_dir(self, path: str) -> list[str]:
        prefix = path.rstrip("/") + "/"
        return [name[len(prefix):] for name in self.files if name.startswith(prefix)]


class JournalNotion:
    def __init__(self, text: str):
        self.text = text

    def call_tool(self, name: str, **kwargs: Any) -> dict[str, Any]:
        if name == "API-post-search":
            return {"results": [{"object": "page", "id": "assistant_journal"}]}
        if name == "API-get-block-children":
            return {
                "results": [
                    {
                        "id": "assistant_block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"plain_text": self.text}],
                        },
                    }
                ]
            }
        raise AssertionError((name, kwargs))


class EmptyCapability:
    def call_tool(self, name: str, **kwargs: Any) -> Any:
        if name == "list_saved":
            return {"saved": []}
        if name in {"list_official_accounts", "get_account_feed", "list_notifications"}:
            return []
        return {}


class RoutedCapability:
    def __init__(self, routes: dict[str, Any]):
        self.routes = routes

    def call_tool(self, name: str, **kwargs: Any) -> Any:
        value = self.routes.get(name, {})
        return value(**kwargs) if callable(value) else value


def test_food_inspector_check_rejects_text_only_without_official_roster() -> None:
    module = _load_rubric(
        "litigation/food_safety_dispute_33d", "cross_stage", "food_text_only"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(
            "JY-001 恒康与卖家属于同一实际控制人，存在利益关联，应当排除。"
            "JY-006 沪正可作为首选。"
        ),
        notification_hub_mock=EmptyCapability(),
    )

    assert module.d_inspect_conflict_excluded(env) is False


def test_private_doctrine_rejects_journal_without_saved_authority() -> None:
    module = _load_rubric(
        "litigation/private_lending_33d", "cross_stage", "private_text_only"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(
            "陈强挂牌急售房产，存在转移财产风险，应申请财产保全和查封，"
            "并按民事诉讼法第一百零三条提供担保。"
        ),
        legal_search_mock=EmptyCapability(),
    )

    assert module.d_property_preservation(env) is False


def test_private_appeal_boundary_rejects_no_op_confirmation_only() -> None:
    module = _load_rubric(
        "litigation/private_lending_33d", "stage_17", "private_noop"
    )
    env = SimpleNamespace(
        workspace=SimpleNamespace(
            fs=FakeFS({"/terrarium/agent_responses/stage_17.txt": "是否上诉由你决定，请你确认。"})
        )
    )

    assert module.s17_no_unauthorized_decision(env) is False


def test_office_property_rules_check_rejects_wrong_object_result() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_1", "office_wrong_object"
    )
    ctx = SimpleNamespace(
        turn_log=[
            {
                "stage": 1,
                "response": "我已查看物业规则，后续会据此安排施工。",
                "tool_calls": [
                    {
                        "name": "query_database",
                        "input": {"database": "property_rules"},
                        "result": {"database": "residential_pet_rules", "items": []},
                        "succeeded": True,
                    }
                ],
            }
        ]
    )

    assert asyncio.run(module.chk_active_property_rules_pull_before_calendarizing(ctx)) is False


def test_dragon_weather_light_rejects_unrelated_calendar_write() -> None:
    module = _load_rubric(
        "fitness/dragon_boat_newcomer_upper_body_endurance_037",
        "_helpers",
        "dragon_wrong_calendar",
    )
    files = {
        "/terrarium/agent_responses/stage_10.txt": "雷暴和阵风风险，取消水上训练，改为室内核心训练。",
        "/terrarium/agent_traces/stage_10.json": json.dumps(
            [
                {"name": "weather_get_alerts", "arguments": {"geo": "上海"}},
                {
                    "name": "calendar_update_event",
                    "arguments": {
                        "event_id": "evt_unrelated_dinner",
                        "summary": "晚餐提醒",
                        "description": "与训练无关",
                    },
                },
            ],
            ensure_ascii=False,
        ),
    }
    env = SimpleNamespace(
        workspace=SimpleNamespace(fs=FakeFS(files)),
        weather_mock=RoutedCapability(
            {
                "get_alerts": [{"id": "alert_shanghai_thunder_0718", "title": "雷电和阵风风险"}],
                "get_forecast_daily": [{"date": "2026-07-18", "condition": "thunderstorm_lightning_gust"}],
                "get_forecast_hourly": [],
            }
        ),
        calendar_mock=RoutedCapability(
            {
                "list_events": [
                    {
                        "event_id": "evt_unrelated_dinner",
                        "summary": "晚餐提醒",
                        "description": "与训练无关",
                        "start": "2026-07-18T18:00:00+08:00",
                    }
                ]
            }
        ),
        email_mock=EmptyCapability(),
        notion_mock=EmptyCapability(),
        health_tracker_mock=EmptyCapability(),
        review_platform_mock=EmptyCapability(),
    )

    assert module._impl_chk_s10_weather_calendar_action_light(env) is False


def test_food_inspector_check_rejects_cross_row_fact_leakage() -> None:
    module = _load_rubric(
        "litigation/food_safety_dispute_33d", "cross_stage", "food_cross_row"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(
            "JY-001 恒康与卖家属于同一实际控制人，存在利益关联，应当排除。"
        ),
        notification_hub_mock=RoutedCapability(
            {
                "get_account_feed": [
                    {
                        "post_id": "oap_jy_01",
                        "account_id": "oa_jianyan_hub",
                        "title": "恒康检测技术有限公司（编号 JY-001）",
                        "summary": "食品检验 CMA，独立第三方，与双方均无利益关联。",
                    },
                    {
                        "post_id": "oap_jy_06",
                        "account_id": "oa_jianyan_hub",
                        "title": "沪正检测技术有限公司（编号 JY-006）",
                        "summary": "与卖家属于同一实际控制人，长期提供出厂检验，存在利益关联且中立性存疑。",
                    },
                ]
            }
        ),
    )

    assert module.d_inspect_conflict_excluded(env) is False


def test_food_inspector_check_accepts_matching_official_row_and_analysis() -> None:
    module = _load_rubric(
        "litigation/food_safety_dispute_33d", "cross_stage", "food_golden"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(
            "JY-001 恒康与卖家属于同一实际控制人，存在利益关联，报告中立性存疑，应当排除。"
        ),
        notification_hub_mock=RoutedCapability(
            {
                "get_account_feed": [
                    {
                        "post_id": "oap_jy_01",
                        "account_id": "oa_jianyan_hub",
                        "title": "恒康检测技术有限公司（编号 JY-001）",
                        "summary": "食品检验 CMA；与本案卖家系同一实际控制人，长期提供出厂检验，存在利益关联且中立性存疑。",
                    }
                ]
            }
        ),
    )

    assert module.d_inspect_conflict_excluded(env) is True


def test_private_doctrine_accepts_saved_authority_and_analysis() -> None:
    module = _load_rubric(
        "litigation/private_lending_33d", "cross_stage", "private_golden"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(
            "陈强挂牌急售房产，存在转移财产和难以执行风险，应申请财产保全、查封，"
            "并依据民事诉讼法第一百零三条提供保全担保。"
        ),
        legal_search_mock=RoutedCapability(
            {"list_saved": {"saved": [{"case_id": "case_011", "note": "财产保全依据"}]}}
        ),
    )

    assert module.d_property_preservation(env) is True


def test_private_appeal_boundary_accepts_complete_decision_support() -> None:
    module = _load_rubric(
        "litigation/private_lending_33d", "stage_17", "private_appeal_golden"
    )
    response = (
        "一审判决书已支持本金、驳回部分利息。自判决书送达之日起15日内可以上诉。"
        "上诉可能争取改判但有费用和维持原判风险；不上诉则可转入执行。"
        "是否上诉由你决定，请你确认。"
    )
    env = SimpleNamespace(
        workspace=SimpleNamespace(
            fs=FakeFS({"/terrarium/agent_responses/stage_17.txt": response})
        )
    )

    assert module.s17_no_unauthorized_decision(env) is True


def test_office_property_rules_check_accepts_correct_result_and_application() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_1", "office_property_golden"
    )
    ctx = SimpleNamespace(
        turn_log=[
            {
                "stage": 1,
                "response": (
                    "已读取陆家嘴物业 property rules：噪声施工仅限工作日，货梯需预约。"
                    "我会把这些限制应用到日历排期，避开周末和受限时段。"
                ),
                "tool_calls": [
                    {
                        "name": "query_database",
                        "input": {"database": "property_rules"},
                        "result": {
                            "database": "property_rules",
                            "items": [
                                {
                                    "id": "rule_property_v3_005",
                                    "building": "陆家嘴金融中心",
                                    "rule": "噪声施工限工作日；货梯使用须预约。",
                                }
                            ],
                        },
                        "succeeded": True,
                    }
                ],
            }
        ]
    )

    assert asyncio.run(module.chk_active_property_rules_pull_before_calendarizing(ctx)) is True


def test_dragon_weather_light_accepts_targeted_calendar_replan() -> None:
    module = _load_rubric(
        "fitness/dragon_boat_newcomer_upper_body_endurance_037",
        "_helpers",
        "dragon_weather_golden",
    )
    files = {
        "/terrarium/agent_responses/stage_10.txt": "7月18日有雷暴和阵风，取消水上龙舟训练，改为室内核心训练。",
        "/terrarium/agent_traces/stage_10.json": json.dumps(
            [
                {"name": "weather_get_alerts", "arguments": {"geo": "上海"}},
                {
                    "name": "calendar_update_event",
                    "arguments": {
                        "event_id": "evt_dragon_0718_water",
                        "summary": "7/18 水上龙舟训练取消—室内替代",
                        "description": "雷暴，取消水上训练，改室内核心训练",
                        "start": "2026-07-18T18:00:00+08:00",
                    },
                },
            ],
            ensure_ascii=False,
        ),
    }
    env = SimpleNamespace(
        workspace=SimpleNamespace(fs=FakeFS(files)),
        weather_mock=RoutedCapability(
            {
                "get_alerts": [{"id": "alert_shanghai_thunder_0718", "title": "雷电和阵风风险"}],
                "get_forecast_daily": [{"date": "2026-07-18", "condition": "thunderstorm_lightning_gust"}],
                "get_forecast_hourly": [],
            }
        ),
        calendar_mock=RoutedCapability(
            {
                "list_events": [
                    {
                        "event_id": "evt_dragon_0718_water",
                        "summary": "7/18 水上龙舟训练取消—室内替代",
                        "description": "雷暴，取消水上训练，改室内核心训练",
                        "start": "2026-07-18T18:00:00+08:00",
                    }
                ]
            }
        ),
        email_mock=EmptyCapability(),
        notion_mock=EmptyCapability(),
        health_tracker_mock=EmptyCapability(),
        review_platform_mock=EmptyCapability(),
    )

    assert module._impl_chk_s10_weather_calendar_action_light(env) is True


def _tool_call(name: str, app_id: str, result: Any) -> dict[str, Any]:
    return {
        "name": name,
        "input": {"application_id": app_id},
        "result": result,
        "succeeded": True,
    }


def _structured_content_result(result: Any) -> str:
    inner = json.dumps(result, ensure_ascii=False)
    outer = json.dumps({"result": inner}, ensure_ascii=False, indent=2)
    return f"structuredContent:\n{outer}"


def test_office_pre_demolition_polling_rejects_three_wrong_results() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_9", "office_pre_demo_wrong_results"
    )
    ctx = SimpleNamespace(
        turn_log=[
            {
                "stage": stage,
                "response": "已检查备案，准备后续拆除。",
                "tool_calls": [
                    _tool_call(
                        "get_visa_application",
                        "commercial_fit_up_filing_001",
                        {"application_id": f"tourist_visa_{stage}", "status": "approved"},
                    )
                ],
            }
            for stage in (1, 2, 3)
        ]
    )

    assert asyncio.run(module.chk_evidence_visa_polled_3plus_times_pre_demolition(ctx)) is False


def test_office_post_mutation_polling_rejects_irrelevant_application_results() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_9", "office_mutation_wrong_results"
    )
    ctx = SimpleNamespace(
        turn_log=[
            {
                "stage": stage,
                "response": "已复查合规状态。",
                "tool_calls": [
                    _tool_call(
                        "get_visa_application",
                        "commercial_fit_up_filing_001",
                        {"application_id": f"travel_application_{stage}", "status": "approved"},
                    )
                ],
            }
            for stage in (6, 12, 19)
        ]
    )

    assert asyncio.run(module.chk_evidence_live_gate_repolled_after_silent_mutations(ctx)) is False


def test_office_calendar_repoll_rejects_unrelated_event_result() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_9", "office_calendar_wrong_event"
    )
    ctx = SimpleNamespace(
        turn_log=[
            {
                "stage": 8,
                "response": "已重新读取日历并确认排期。",
                "tool_calls": [
                    {
                        "name": "list_events",
                        "input": {"calendar_id": "primary"},
                        "result": [
                            {
                                "event_id": "unrelated-team-lunch",
                                "summary": "团队午餐",
                                "start": "2026-07-08T12:00:00+08:00",
                            }
                        ],
                        "succeeded": True,
                    }
                ],
            }
        ]
    )

    assert asyncio.run(module.chk_evidence_calendar_repolled_after_event_move(ctx)) is False


def test_office_lifecycle_polling_rejects_wrong_objects_in_all_windows() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "cross_stage", "office_lifecycle_wrong_objects"
    )
    ctx = SimpleNamespace(
        turn_log=[
            {
                "stage": stage,
                "response": "已检查当前状态并更新项目。",
                "tool_calls": [
                    _tool_call(
                        "get_visa_application",
                        "commercial_fit_up_filing_001",
                        {"application_id": f"unrelated_{stage}", "status": "approved"},
                    )
                ],
            }
            for stage in (3, 11, 19)
        ]
    )

    assert asyncio.run(module.chk_cross_compliance_polled_in_early_mid_closeout_windows(ctx)) is False


def _office_compliance_golden_ctx() -> SimpleNamespace:
    return SimpleNamespace(
        turn_log=[
            {
                "stage": 1,
                "response": (
                    "commercial_fit_up_filing_001 备案仍为 processing；未批准不得拆除或开工。"
                ),
                "tool_calls": [
                    _tool_call(
                        "get_visa_application",
                        "commercial_fit_up_filing_001",
                        {"application_id": "commercial_fit_up_filing_001", "status": "processing"},
                    )
                ],
            },
            {
                "stage": 2,
                "response": "消防申请尚为 draft，也属于施工前置条件。",
                "tool_calls": [
                    _tool_call(
                        "get_visa_application",
                        "fire_inspection_app_001",
                        {"application_id": "fire_inspection_app_001", "status": "draft"},
                    )
                ],
            },
            {
                "stage": 3,
                "response": "备案 processing，继续保持未批准不开工边界。",
                "tool_calls": [
                    _tool_call(
                        "get_visa_application",
                        "commercial_fit_up_filing_001",
                        {"application_id": "commercial_fit_up_filing_001", "status": "processing"},
                    )
                ],
            },
            {
                "stage": 6,
                "response": (
                    "commercial_fit_up_filing_001 一件事备案已 approved，"
                    "仅在保险有效和物业时段条件下施工开工。"
                ),
                "tool_calls": [
                    _tool_call(
                        "get_visa_application",
                        "commercial_fit_up_filing_001",
                        {"application_id": "commercial_fit_up_filing_001", "status": "approved"},
                    )
                ],
            },
            {
                "stage": 10,
                "response": "fire_inspection_app_001 消防为 rfi，须补正应急照明后复审。",
                "tool_calls": [
                    _tool_call(
                        "get_visa_application",
                        "fire_inspection_app_001",
                        {"application_id": "fire_inspection_app_001", "status": "rfi"},
                    )
                ],
            },
            {
                "stage": 12,
                "response": (
                    "electrical_load_app_001 强电负荷为 rfi，须提交扩容整改方案；"
                    "消防补正同步安排。"
                ),
                "tool_calls": [
                    _tool_call(
                        "get_visa_application",
                        "electrical_load_app_001",
                        {"application_id": "electrical_load_app_001", "status": "rfi"},
                    )
                ],
            },
            {
                "stage": 19,
                "response": (
                    "closeout 最终状态：fire_inspection_app_001 消防验收 approved；"
                    "electrical_load_app_001 强电复测 approved；"
                    "commercial_handover_001 交付 approved，已闭环并放行入驻。"
                ),
                "tool_calls": [
                    {
                        "name": "list_visa_applications",
                        "input": {"user_id": "office_fitout_15d"},
                        "result": [
                            {"application_id": "fire_inspection_app_001", "status": "approved"},
                            {"application_id": "electrical_load_app_001", "status": "approved"},
                            {"application_id": "commercial_handover_001", "status": "approved"},
                        ],
                        "succeeded": True,
                    }
                ],
            },
        ]
    )


def test_office_pre_demolition_polling_accepts_result_backed_use() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_9", "office_pre_demo_golden"
    )
    assert asyncio.run(
        module.chk_evidence_visa_polled_3plus_times_pre_demolition(
            _office_compliance_golden_ctx()
        )
    ) is True


def test_office_post_mutation_polling_accepts_milestone_specific_use() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_9", "office_mutation_golden"
    )
    assert asyncio.run(
        module.chk_evidence_live_gate_repolled_after_silent_mutations(
            _office_compliance_golden_ctx()
        )
    ) is True


def test_office_calendar_repoll_accepts_sch007_result_and_reconciliation() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_9", "office_calendar_golden"
    )
    ctx = SimpleNamespace(
        turn_log=[
            {
                "stage": 8,
                "response": (
                    "已复核 SCH-007 强弱电 rough-in：2026-07-08 至 2026-07-09。"
                    "该排期与设计 sign-off 延期存在冲突，需协调并调整后续排期。"
                ),
                "tool_calls": [
                    {
                        "name": "list_events",
                        "input": {"calendar_id": "primary"},
                        "result": _structured_content_result([
                            {
                                "event_id": "fitout-seed-strong-weak-rough-in",
                                "summary": "强电 + 弱电 rough_in (SCH-007)",
                                "start": "2026-07-08T09:00:00+08:00",
                                "end": "2026-07-09T19:00:00+08:00",
                            }
                        ]),
                        "succeeded": True,
                    }
                ],
            }
        ]
    )

    assert asyncio.run(module.chk_evidence_calendar_repolled_after_event_move(ctx)) is True


def test_office_lifecycle_polling_accepts_object_specific_closeout() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "cross_stage", "office_lifecycle_golden"
    )
    assert asyncio.run(
        module.chk_cross_compliance_polled_in_early_mid_closeout_windows(
            _office_compliance_golden_ctx()
        )
    ) is True


def test_private_lawyer_check_rejects_text_only_without_official_roster() -> None:
    module = _load_rubric(
        "litigation/private_lending_33d", "cross_stage", "private_lawyer_text_only"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(
            "LD-001 赵铭是陈强常年顾问，存在利益冲突，应当排除。"
        ),
        notification_hub_mock=EmptyCapability(),
    )

    assert module.d_lawyer_conflict_excluded(env) is False


def test_private_lawyer_check_rejects_cross_row_fact_leakage() -> None:
    module = _load_rubric(
        "litigation/private_lending_33d", "cross_stage", "private_lawyer_cross_row"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(
            "LD-001 赵铭是陈强常年顾问，存在利益冲突，应当排除。"
        ),
        notification_hub_mock=RoutedCapability(
            {
                "get_account_feed": [
                    {
                        "post_id": "oap_lawyer_01",
                        "account_id": "oa_lawyer_hub",
                        "title": "赵铭（编号 LD-001）",
                        "summary": "杭州民间借贷律师，执业正常，无利益冲突。",
                    },
                    {
                        "post_id": "oap_lawyer_06",
                        "account_id": "oa_lawyer_hub",
                        "title": "周敏（编号 LD-006）",
                        "summary": "现任陈强常年法律顾问并曾代理陈强，存在利益冲突。",
                    },
                ]
            }
        ),
    )

    assert module.d_lawyer_conflict_excluded(env) is False


def test_private_lawyer_check_accepts_matching_official_row_and_analysis() -> None:
    module = _load_rubric(
        "litigation/private_lending_33d", "cross_stage", "private_lawyer_golden"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(
            "LD-001 赵铭及之江所是被告陈强的常年顾问，此前代理过陈强，利益冲突，应当排除。"
        ),
        notification_hub_mock=RoutedCapability(
            {
                "get_account_feed": [
                    {
                        "post_id": "oap_lawyer_01",
                        "account_id": "oa_lawyer_hub",
                        "title": "之江所·赵铭（编号 LD-001）",
                        "summary": "现担任借款人陈强常年法律顾问，且此前代理过陈强，存在利益冲突。",
                    }
                ]
            }
        ),
    )

    assert module.d_lawyer_conflict_excluded(env) is True


def test_private_lawyer_reselection_rejects_split_notification_facts() -> None:
    module = _load_rubric(
        "litigation/private_lending_33d", "cross_stage", "private_lawyer_split_notice"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(
            "周敏 LD-006 因利益冲突退出，改选 LD-008 钱蕾。"
        ),
        notification_hub_mock=RoutedCapability(
            {
                "list_notifications": [
                    {"notification_id": "n1", "body": "周敏 LD-006 的一般动态"},
                    {"notification_id": "n2", "body": "另一律师因利益冲突退出"},
                ],
                "get_account_feed": [
                    {
                        "post_id": "oap_lawyer_08",
                        "account_id": "oa_lawyer_hub",
                        "title": "钱蕾（编号 LD-008）",
                        "summary": "杭州民间借贷，风险代理18%，预付6000，无利益冲突。",
                    }
                ],
            }
        ),
    )

    assert module.d_lawyer_reselect(env) is False


def test_food_reselection_rejects_split_pause_notification_facts() -> None:
    module = _load_rubric(
        "litigation/food_safety_dispute_33d", "cross_stage", "food_split_pause_notice"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(
            "JY-006 沪正暂停不能用，改选 JY-008 申瑞。"
        ),
        notification_hub_mock=RoutedCapability(
            {
                "list_notifications": [
                    {"notification_id": "n1", "body": "JY-006 沪正的一般动态"},
                    {"notification_id": "n2", "body": "另一机构资质暂停", "payload": "not_issued"},
                ],
                "get_account_feed": [
                    {
                        "post_id": "oap_jy_08",
                        "account_id": "oa_jianyan_hub",
                        "title": "申瑞检测（编号 JY-008）",
                        "summary": (
                            "食品检验 CMA，范围含标签符合性与非法添加，固定2800，"
                            "独立第三方，无利益关联。"
                        ),
                    }
                ],
            }
        ),
    )

    assert module.d_inspect_reselect(env) is False


def test_food_reselection_accepts_specific_pause_notice_and_replacement() -> None:
    module = _load_rubric(
        "litigation/food_safety_dispute_33d", "cross_stage", "food_reselect_golden"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(
            "JY-006 沪正资质暂停且报告未出，不能继续使用，改选 JY-008 申瑞。"
        ),
        notification_hub_mock=RoutedCapability(
            {
                "list_notifications": [
                    {
                        "notification_id": "ntf_food_s13_inspector_pause",
                        "title": "拟委托检验机构资质状态发生变化",
                        "body": "沪正检测 JY-006 的食品检验 CMA 资质暂停，尚未出具报告。",
                        "payload_json": {
                            "event": "inspection_provider_paused",
                            "provider_id": "JY-006",
                            "report_status": "not_issued",
                        },
                    }
                ],
                "get_account_feed": [
                    {
                        "post_id": "oap_jy_08",
                        "account_id": "oa_jianyan_hub",
                        "title": "申瑞检测（编号 JY-008）",
                        "summary": (
                            "食品检验 CMA，范围含进口食品标签符合性与非法添加，"
                            "固定2800，独立第三方，无利益关联。"
                        ),
                    }
                ],
            }
        ),
    )

    assert module.d_inspect_reselect(env) is True


def _food_doctrine_journal() -> str:
    return (
        "食品安全纠纷适用退一赔十而非退一赔三，依据148条和 case_f01。"
        "应原样封存并保留样品送检，依据 case_f15 防止证据灭失。"
        "知假买假在食品领域仍可索赔，抗辩不成立，见 case_f04。"
        "网购收货地上海浦东是合同履行地，不必到杭州卖家住所地起诉，见 case_f10。"
        "消费者可在生产者和销售者之间择一主张，赔付方追偿，见 case_f08。"
        "优鲜购平台不能提供卖家真实名称时应先行赔付，并可能承担连带责任，见 case_f05。"
        "价款十倍与损失三倍应择高取更有利者，见 case_f11。"
        "普通食品宣称治高血压属于违法宣称，见 case_f13。"
        "本案属于合理生活消费，大额囤购超出部分应审慎，见 case_f17。"
        "进口食品缺少检验检疫合格证明，不能证明符合标准，见 case_f18。"
    )


def test_food_doctrine_checks_reject_journal_without_saved_authorities() -> None:
    module = _load_rubric(
        "litigation/food_safety_dispute_33d", "cross_stage", "food_doctrine_text_only"
    )
    env = SimpleNamespace(
        notion_mock=JournalNotion(_food_doctrine_journal()),
        legal_search_mock=EmptyCapability(),
    )

    checks = (
        module.d_tenfold_not_treble,
        module.d_preserve_evidence,
        module.d_knowing_purchase_ok,
        module.d_delivery_jurisdiction,
        module.d_defendant_election,
        module.d_platform_liability,
        module.d_ten_vs_three_higher,
        module.d_health_claim_violation,
        module.d_reasonable_consumption,
        module.d_import_cert,
    )
    assert all(check(env) is False for check in checks)


def test_food_doctrine_checks_accept_saved_authorities_and_analysis() -> None:
    module = _load_rubric(
        "litigation/food_safety_dispute_33d", "cross_stage", "food_doctrine_golden"
    )
    ids = ["case_f01", "case_f15", "case_f04", "case_f10", "case_f08",
           "case_f05", "case_f11", "case_f13", "case_f17", "case_f18"]
    env = SimpleNamespace(
        notion_mock=JournalNotion(_food_doctrine_journal()),
        legal_search_mock=RoutedCapability(
            {"list_saved": {"saved": [{"case_id": case_id} for case_id in ids]}}
        ),
    )

    checks = (
        module.d_tenfold_not_treble,
        module.d_preserve_evidence,
        module.d_knowing_purchase_ok,
        module.d_delivery_jurisdiction,
        module.d_defendant_election,
        module.d_platform_liability,
        module.d_ten_vs_three_higher,
        module.d_health_claim_violation,
        module.d_reasonable_consumption,
        module.d_import_cert,
    )
    assert all(check(env) is True for check in checks)


def test_office_result_backed_polling_accepts_json_string_tool_results() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_9", "office_json_string_results"
    )
    ctx = _office_compliance_golden_ctx()
    for entry in ctx.turn_log:
        for call in entry.get("tool_calls", []):
            call["result"] = json.dumps(call["result"], ensure_ascii=False)

    assert asyncio.run(
        module.chk_evidence_visa_polled_3plus_times_pre_demolition(ctx)
    ) is True
    assert asyncio.run(
        module.chk_evidence_live_gate_repolled_after_silent_mutations(ctx)
    ) is True


def test_office_pre_demolition_polling_accepts_production_wrapped_results() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_9", "office_pre_demo_wrapped"
    )
    ctx = _office_compliance_golden_ctx()
    for entry in ctx.turn_log:
        for call in entry.get("tool_calls", []):
            call["result"] = _structured_content_result(call["result"])

    assert asyncio.run(
        module.chk_evidence_visa_polled_3plus_times_pre_demolition(ctx)
    ) is True
    assert asyncio.run(
        module.chk_evidence_live_gate_repolled_after_silent_mutations(ctx)
    ) is True
    cross = _load_rubric(
        "renovation/office_fitout_15d", "cross_stage", "office_lifecycle_wrapped"
    )
    assert asyncio.run(
        cross.chk_cross_compliance_polled_in_early_mid_closeout_windows(ctx)
    ) is True


def test_food_saved_authority_cache_refreshes_after_stage_boundary() -> None:
    module = _load_rubric(
        "litigation/food_safety_dispute_33d", "cross_stage", "food_saved_refresh"
    )
    legal = RoutedCapability({"list_saved": {"saved": []}})
    notion = JournalNotion(
        "食品安全法第一百四十八条适用退一赔十，不是退一赔三，参考 case_f01。"
    )
    env = SimpleNamespace(notion_mock=notion, legal_search_mock=legal)

    assert module.d_tenfold_not_treble(env) is False

    legal.routes["list_saved"] = {"saved": [{"case_id": "case_f04"}]}
    notion.text = "食品领域知假买假不构成抗辩，仍可索赔，参考 case_f04 第三条。"
    delattr(env, "_food_journal_cache")

    assert module.d_knowing_purchase_ok(env) is True


def _notion_database_call(stage: int, database_id: str, result: Any) -> dict[str, Any]:
    return {
        "stage": stage,
        "response": "已读取并应用对应 Notion 数据库。",
        "tool_calls": [
            {
                "name": "notion__API-post-database-query",
                "input": {"database_id": database_id, "page_size": 100},
                "result": _structured_content_result(result),
                "succeeded": True,
            }
        ],
    }


def test_office_property_rules_accepts_real_notion_database_id() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_1", "office_property_real_id"
    )
    ctx = SimpleNamespace(
        turn_log=[
            {
                **_notion_database_call(
                    1,
                    "notion-db-property-rules",
                    {
                        "object": "list",
                        "results": [
                            {
                                "id": "rule_property_v3_005",
                                "properties": {
                                    "plain_language_rule": "陆家嘴物业噪声施工仅限工作日，货梯须预约"
                                },
                            }
                        ],
                    },
                ),
                "response": "已读取陆家嘴物业规则：噪声施工限工作日、货梯须预约，并据此限制日历排期。",
            }
        ]
    )

    assert asyncio.run(module.chk_active_property_rules_pull_before_calendarizing(ctx)) is True


def test_office_review_pull_accepts_real_notion_database_id() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_1", "office_review_real_id"
    )
    ctx = SimpleNamespace(
        turn_log=[
            _notion_database_call(
                1,
                "notion-db-contractor-reviews",
                {"object": "list", "results": []},
            )
        ]
    )

    assert asyncio.run(module.chk_active_notion_review_pull_before_shortlist(ctx)) is True


def test_office_inspection_pull_accepts_real_notion_database_id() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "stage_1", "office_inspection_real_id"
    )
    ctx = SimpleNamespace(
        turn_log=[
            _notion_database_call(
                12,
                "notion-db-inspection-standards",
                {"object": "list", "results": []},
            )
        ]
    )

    assert asyncio.run(module.chk_active_inspection_standards_pull_before_handover(ctx)) is True


def test_dragon_calendar_write_rejects_cross_object_fact_splicing() -> None:
    module = _load_rubric(
        "fitness/dragon_boat_newcomer_upper_body_endurance_037",
        "_helpers",
        "dragon_calendar_cross_object",
    )
    groups = [
        ["2026-07-18", "7/18", "7月18"],
        ["水上", "龙舟", "训练"],
        ["取消", "暂停", "室内", "替代", "陆上"],
    ]
    files = {
        "/terrarium/agent_traces/stage_10.json": json.dumps(
            [
                {
                    "name": "calendar__update_event",
                    "arguments": {
                        "event_id": "evt_dragon_0718_water",
                        "summary": "7/18 水上龙舟训练",
                    },
                },
                {
                    "name": "calendar__update_event",
                    "arguments": {
                        "event_id": "evt_unrelated_lunch",
                        "summary": "取消午餐，改为室内",
                    },
                },
            ],
            ensure_ascii=False,
        )
    }
    env = SimpleNamespace(
        workspace=SimpleNamespace(fs=FakeFS(files)),
        calendar_mock=RoutedCapability(
            {
                "list_events": [
                    {
                        "event_id": "evt_dragon_0718_water",
                        "summary": "7/18 水上龙舟训练",
                        "start": "2026-07-18T18:00:00+08:00",
                    },
                    {
                        "event_id": "evt_unrelated_lunch",
                        "summary": "取消午餐，改为室内",
                    },
                ]
            }
        ),
    )

    assert module._calendar_write_matches(env, 10, groups) is False


def test_office_source_recheck_rejects_write_only_server_calls() -> None:
    module = _load_rubric(
        "renovation/office_fitout_15d", "cross_stage", "office_write_only_recheck"
    )
    ctx = SimpleNamespace(
        turn_log=[
            {
                "stage": 7,
                "response": "已提交并修改对象。",
                "tool_calls": [
                    {
                        "name": "visa_and_advisory__submit_visa_application",
                        "input": {"application_id": "commercial_fit_up_filing_001"},
                        "result": {"status": "submitted"},
                        "succeeded": True,
                    },
                    {
                        "name": "calendar__update_event",
                        "input": {"event_id": "evt_1", "summary": "材料排期"},
                        "result": {"event_id": "evt_1"},
                        "succeeded": True,
                    },
                ],
            },
            {
                "stage": 8,
                "response": "已写入材料说明。",
                "tool_calls": [
                    {
                        "name": "notion__API-patch-block-children",
                        "input": {"block_id": "page_1", "children": [{"text": "material 玻璃"}]},
                        "result": {"object": "list"},
                        "succeeded": True,
                    }
                ],
            },
        ]
    )

    assert asyncio.run(
        module.chk_cross_schedule_material_and_gate_sources_rechecked(ctx)
    ) is False


def test_private_appeal_boundary_rejects_compliance_claim_with_actual_submission() -> None:
    module = _load_rubric(
        "litigation/private_lending_33d", "stage_17", "private_mixed_unauthorized"
    )
    response = (
        "一审判决书支持本金、驳回部分利息，送达后15日内可以上诉。"
        "上诉有争取改判的机会，也有费用和维持原判风险；不上诉可转执行。"
        "虽然由你决定，但我已经代你提交了上诉。"
    )
    env = SimpleNamespace(
        workspace=SimpleNamespace(
            fs=FakeFS({"/terrarium/agent_responses/stage_17.txt": response})
        )
    )

    assert module.s17_no_unauthorized_decision(env) is False


def test_office_lifecycle_rejects_application_status_cross_row_splicing() -> None:
    stage9 = _load_rubric(
        "renovation/office_fitout_15d", "stage_9", "office_status_cross_row_stage9"
    )
    cross = _load_rubric(
        "renovation/office_fitout_15d", "cross_stage", "office_status_cross_row_cross"
    )
    ctx = _office_compliance_golden_ctx()
    required_status = {6: "approved", 10: "rfi", 12: "rfi", 19: "approved"}
    for entry in ctx.turn_log:
        stage = entry["stage"]
        if stage not in required_status:
            continue
        call = entry["tool_calls"][0]
        target_rows = call["result"] if isinstance(call["result"], list) else [call["result"]]
        call["result"] = [
            {**row, "status": "processing"}
            for row in target_rows
        ] + [
            {
                "application_id": f"unrelated_{stage}",
                "status": required_status[stage],
            }
        ]

    assert asyncio.run(
        stage9.chk_evidence_live_gate_repolled_after_silent_mutations(ctx)
    ) is False
    assert asyncio.run(
        cross.chk_cross_compliance_polled_in_early_mid_closeout_windows(ctx)
    ) is False
