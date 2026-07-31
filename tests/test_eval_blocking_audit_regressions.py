from __future__ import annotations

from datetime import date
import importlib
from pathlib import Path
import sys


HF_ROOT = Path(__file__).resolve().parents[1]
if str(HF_ROOT) not in sys.path:
    sys.path.insert(0, str(HF_ROOT))


def _optimizer():
    return importlib.import_module("lib.ecommerce_cart_optimizer")


def test_optimizer_finds_true_central_ac_cart() -> None:
    optimizer = _optimizer()
    seed = (
        HF_ROOT
        / "eval_set/shopping/central_ac_install_30d/envs/ecommerce"
        / "central_ac_install_30d/init.sql"
    )

    plans = optimizer.optimal_cart_plans(seed, "bsk_iscac_", date(2026, 6, 22))

    assert len(plans) == 1
    plan = plans[0]
    assert plan.sku_ids == frozenset(
        {"bsk_iscac_a3", "bsk_iscac_b2", "bsk_iscac_c2"}
    )
    assert plan.subtotal_minor == 30800
    assert plan.total_minor == 17104
    assert plan.coupon_codes == frozenset(
        {"SAVE30_iscac", "BIG70_iscac", "PCT12_iscac"}
    )


def test_optimizer_finds_true_stroller_cart() -> None:
    optimizer = _optimizer()
    seed = (
        HF_ROOT
        / "eval_set/shopping/baby_stroller_safety_standard_30d/envs/ecommerce"
        / "baby_stroller_safety_standard_30d/init.sql"
    )

    plans = optimizer.optimal_cart_plans(seed, "bsk_strr_", date(2026, 6, 22))

    assert len(plans) == 1
    plan = plans[0]
    assert plan.sku_ids == frozenset(
        {"bsk_strr_a2", "bsk_strr_b2", "bsk_strr_c2"}
    )
    assert plan.subtotal_minor == 25700
    assert plan.total_minor == 14630
    assert plan.coupon_codes == frozenset(
        {"FULL209_strr", "FULL249_strr", "PCT10_strr"}
    )


def test_optimizer_returns_all_ties_and_excludes_expired_coupon(tmp_path: Path) -> None:
    optimizer = _optimizer()
    seed = tmp_path / "init.sql"
    seed.write_text(
        "\n".join(
            [
                "INSERT INTO products (product_id, title, brand, category, description, rating, rating_count, sales_count, base_price_minor, return_policy) VALUES ('p_a1', 'A one', 'B', 'cat', '', 5, 1, 1, 1000, 'r');",
                "INSERT INTO products (product_id, title, brand, category, description, rating, rating_count, sales_count, base_price_minor, return_policy) VALUES ('p_a2', 'A two', 'B', 'cat', '', 5, 1, 1, 1000, 'r');",
                "INSERT INTO products (product_id, title, brand, category, description, rating, rating_count, sales_count, base_price_minor, return_policy) VALUES ('p_b1', 'B one', 'B', 'cat', '', 5, 1, 1, 2000, 'r');",
                "INSERT INTO skus (sku_id, product_id, attrs_json, price_minor) VALUES ('pool_a1', 'p_a1', '{\"need\": \"n1\"}', 1000);",
                "INSERT INTO skus (sku_id, product_id, attrs_json, price_minor) VALUES ('pool_a2', 'p_a2', '{\"need\": \"n1\"}', 1000);",
                "INSERT INTO skus (sku_id, product_id, attrs_json, price_minor) VALUES ('pool_b1', 'p_b1', '{\"need\": \"n2\"}', 2000);",
                "INSERT INTO stocks (sku_id, quantity) VALUES ('pool_a1', 1);",
                "INSERT INTO stocks (sku_id, quantity) VALUES ('pool_a2', 1);",
                "INSERT INTO stocks (sku_id, quantity) VALUES ('pool_b1', 1);",
                "INSERT INTO coupons (code, kind, value_bp_or_minor, min_spend_minor, valid_from, valid_until, category_restriction, max_uses, used_count, active) VALUES ('LIVE', 'flat_off', 500, 3000, '2026-01-01', '2026-12-31', NULL, 10, 0, 1);",
                "INSERT INTO coupons (code, kind, value_bp_or_minor, min_spend_minor, valid_from, valid_until, category_restriction, max_uses, used_count, active) VALUES ('OLD', 'flat_off', 2500, 3000, '2025-01-01', '2025-12-31', NULL, 10, 0, 1);",
            ]
        ),
        encoding="utf-8",
    )

    plans = optimizer.optimal_cart_plans(seed, "pool_", date(2026, 6, 22))

    assert [plan.sku_ids for plan in plans] == [
        frozenset({"pool_a1", "pool_b1"}),
        frozenset({"pool_a2", "pool_b1"}),
    ]
    assert {plan.total_minor for plan in plans} == {2500}
    assert {plan.coupon_codes for plan in plans} == {frozenset({"LIVE"})}

import importlib.util
import json
import sys
from types import ModuleType, SimpleNamespace
from typing import Any

import yaml


def _load_rubric_module(task_root: Path, module_name: str, alias: str) -> ModuleType:
    package_name = f"_audit_{alias}_rubrics"
    package = ModuleType(package_name)
    package.__path__ = [str(task_root / "rubrics")]  # type: ignore[attr-defined]
    sys.modules[package_name] = package
    qualified = f"{package_name}.{module_name}"
    path = task_root / "rubrics" / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(qualified, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[qualified] = module
    spec.loader.exec_module(module)
    return module


class _EcommerceCap:
    def __init__(self, cart: Any):
        self.cart = cart

    def call_tool(self, tool: str, **kwargs: Any) -> Any:
        assert tool == "get_cart"
        return self.cart


def _cart(
    sku_ids: list[str],
    *,
    subtotal: int,
    total: int,
    coupons: list[str],
    quantities: dict[str, int] | None = None,
) -> dict[str, Any]:
    quantities = quantities or {}
    return {
        "items": [
            {"sku_id": sku, "qty": quantities.get(sku, 1)} for sku in sku_ids
        ],
        "subtotal_minor": subtotal,
        "total_minor": total,
        "applied_coupons": [{"code": code} for code in coupons],
    }


def _shopping_case(name: str, prefix: str, user_id: str):
    task_root = HF_ROOT / "eval_set/shopping" / name
    helper = _load_rubric_module(task_root, "_helpers", f"shopping_{prefix}")
    plans = _optimizer().optimal_cart_plans(
        task_root / f"envs/ecommerce/{name}/init.sql",
        f"bsk_{prefix}_",
        date(2026, 6, 22),
    )
    return task_root, helper, plans, user_id


def test_shopping_helpers_accept_true_optima_and_reject_obsolete_carts() -> None:
    cases = [
        (
            "central_ac_install_30d",
            "iscac",
            "usr_luo_wei",
            _cart(
                ["bsk_iscac_a3", "bsk_iscac_b2", "bsk_iscac_c2"],
                subtotal=30800,
                total=17104,
                coupons=["SAVE30_iscac", "BIG70_iscac", "PCT12_iscac"],
            ),
            _cart(
                ["bsk_iscac_a2", "bsk_iscac_b2", "bsk_iscac_c3"],
                subtotal=31300,
                total=17544,
                coupons=["SAVE30_iscac", "BIG70_iscac", "PCT12_iscac"],
            ),
        ),
        (
            "baby_stroller_safety_standard_30d",
            "strr",
            "usr_yan_ting",
            _cart(
                ["bsk_strr_a2", "bsk_strr_b2", "bsk_strr_c2"],
                subtotal=25700,
                total=14630,
                coupons=["FULL209_strr", "FULL249_strr", "PCT10_strr"],
            ),
            _cart(
                ["bsk_strr_a3", "bsk_strr_b2", "bsk_strr_c3"],
                subtotal=23900,
                total=18510,
                coupons=["FULL209_strr", "PCT10_strr"],
            ),
        ),
    ]
    for name, prefix, user_id, optimal, obsolete in cases:
        _, helper, plans, _ = _shopping_case(name, prefix, user_id)
        assert helper._backend_cart_matches_optimal(
            SimpleNamespace(ecommerce_mock=_EcommerceCap(optimal)), user_id, plans
        ) is True
        assert helper._backend_cart_matches_optimal(
            SimpleNamespace(ecommerce_mock=_EcommerceCap(obsolete)), user_id, plans
        ) is False


def test_shopping_helpers_reject_wrong_quantity_coupon_set_and_backend_failure() -> None:
    _, helper, plans, user_id = _shopping_case(
        "central_ac_install_30d", "iscac", "usr_luo_wei"
    )
    skus = ["bsk_iscac_a3", "bsk_iscac_b2", "bsk_iscac_c2"]
    wrong_qty = _cart(
        skus,
        subtotal=30800,
        total=17104,
        coupons=["SAVE30_iscac", "BIG70_iscac", "PCT12_iscac"],
        quantities={"bsk_iscac_a3": 2},
    )
    wrong_coupons = _cart(
        skus,
        subtotal=30800,
        total=17104,
        coupons=["BIG70_iscac"],
    )
    extra_pool_item = _cart(
        [*skus, "bsk_iscac_a1"],
        subtotal=30800,
        total=17104,
        coupons=["SAVE30_iscac", "BIG70_iscac", "PCT12_iscac"],
    )
    for value in (wrong_qty, wrong_coupons, extra_pool_item, None):
        assert helper._backend_cart_matches_optimal(
            SimpleNamespace(ecommerce_mock=_EcommerceCap(value)), user_id, plans
        ) is False


def test_coupon_visibility_is_complete_in_both_stage8_messages() -> None:
    requirements = {
        "central_ac_install_30d": (
            "SAVE30_iscac",
            "BIG70_iscac",
            "MAX120_iscac",
            "PCT12_iscac",
            "263",
            "301",
            "543",
            "12%",
            "叠加",
        ),
        "baby_stroller_safety_standard_30d": (
            "FULL209_strr",
            "FULL249_strr",
            "PCT10_strr",
            "219",
            "254",
            "10%",
            "叠加",
        ),
    }
    for name, terms in requirements.items():
        task_root = HF_ROOT / "eval_set/shopping" / name
        payload = yaml.safe_load((task_root / "event.yaml").read_text(encoding="utf-8"))
        stage8 = payload["stages"].get(8, payload["stages"].get("8"))
        visible = "\n".join(str(event.get("body") or "") for event in stage8)
        for term in terms:
            assert term in visible, (name, term)


def test_shopping_stage8_sources_do_not_encode_obsolete_contracts() -> None:
    central = (
        HF_ROOT
        / "eval_set/shopping/central_ac_install_30d/rubrics/stage_8.py"
    ).read_text(encoding="utf-8")
    stroller = (
        HF_ROOT
        / "eval_set/shopping/baby_stroller_safety_standard_30d/rubrics/stage_8.py"
    ).read_text(encoding="utf-8")
    assert "subtotal_minor=31300" not in central
    assert "total_minor=24300" not in central
    assert "subtotal_minor=23900" not in stroller
    assert "total_minor=20900" not in stroller

class _TraceFS:
    def __init__(self, traces: dict[int, list[dict[str, Any]]]):
        self.traces = traces

    def read_file(self, path: str) -> bytes:
        for stage, calls in self.traces.items():
            if path.endswith(f"stage_{stage}.json"):
                return json.dumps(calls, ensure_ascii=False).encode("utf-8")
        raise FileNotFoundError(path)


class _FlightCap:
    def __init__(self):
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def call_tool(self, tool: str, **kwargs: Any) -> Any:
        self.calls.append((tool, kwargs))
        if tool == "list_bookings":
            return {"bookings": [{"pnr": "PNR1", "status": "confirmed"}]}
        if tool == "get_booking":
            return {
                "pnr": kwargs["pnr"],
                "status": "confirmed",
                "segments": [{"origin": "AMS", "destination": "UIO"}],
            }
        raise AssertionError(tool)


class _HotelCap:
    def __init__(self):
        self.owners: list[str] = []

    def call_tool(self, tool: str, **kwargs: Any) -> Any:
        if tool == "list_reservations":
            owner = str(kwargs["user_id"])
            self.owners.append(owner)
            ids = ["RES1"] if owner == "linqiao@example.com" else []
            return {"user_id": owner, "count": len(ids), "reservation_ids": ids}
        if tool == "search_hotels":
            city = kwargs["city_or_geo"]
            return [{"hotel_id": "H1", "city": city}] if city == "Puerto Ayora" else []
        if tool == "get_reservation":
            return {
                "reservation_id": kwargs["reservation_id"],
                "hotel_id": "H1",
                "status": "confirmed",
            }
        raise AssertionError(tool)


def _galapagos_backend():
    task_root = HF_ROOT / "eval_set/travel/galapagos_no_us_transit"
    return task_root, _load_rubric_module(task_root, "_backend_checks", "galapagos")


def test_galapagos_flight_lookup_has_no_hidden_owner_filter() -> None:
    _, backend = _galapagos_backend()
    flight = _FlightCap()

    rows = backend.flight_bookings(SimpleNamespace(flight_booking_mock=flight))

    assert rows[0]["segments"] == [{"origin": "AMS", "destination": "UIO"}]
    assert flight.calls[0] == ("list_bookings", {})


def test_galapagos_hotel_lookup_uses_agent_trace_owner() -> None:
    _, backend = _galapagos_backend()
    trace = {
        7: [
            {
                "type": "tool_call",
                "name": "hotel_booking.create_reservation",
                "arguments": {
                    "guest_profile": {
                        "user_id": "linqiao@example.com",
                        "email": "linqiao@example.com",
                    }
                },
            }
        ]
    }
    hotel = _HotelCap()
    env = SimpleNamespace(
        workspace=SimpleNamespace(fs=_TraceFS(trace)), hotel_booking_mock=hotel
    )

    rows = backend.hotel_reservations(env)

    assert hotel.owners == ["linqiao@example.com"]
    assert rows == [
        {
            "reservation_id": "RES1",
            "hotel_id": "H1",
            "status": "confirmed",
            "city": "Puerto Ayora",
        }
    ]


def test_galapagos_hotel_owner_can_come_from_list_trace_and_missing_owner_is_empty() -> None:
    _, backend = _galapagos_backend()
    list_trace = {
        8: [
            {
                "type": "tool_call",
                "name": "hotel_booking.list_reservations",
                "arguments": {"user_id": "linqiao@example.com"},
            }
        ]
    }
    hotel = _HotelCap()
    with_owner = SimpleNamespace(
        workspace=SimpleNamespace(fs=_TraceFS(list_trace)), hotel_booking_mock=hotel
    )
    without_owner = SimpleNamespace(
        workspace=SimpleNamespace(fs=_TraceFS({})), hotel_booking_mock=_HotelCap()
    )

    assert backend.hotel_reservations(with_owner)[0]["reservation_id"] == "RES1"
    assert backend.hotel_reservations(without_owner) == []


def test_galapagos_rubric_source_has_no_private_user_id_contract() -> None:
    task_root, _ = _galapagos_backend()
    source = (task_root / "rubrics/_backend_checks.py").read_text(encoding="utf-8")
    assert 'USER_ID = "user_lin_qiao"' not in source

class _ExistingTraceFS(_TraceFS):
    def exists(self, path: str) -> bool:
        return any(path.endswith(f"stage_{stage}.json") for stage in self.traces)


class _SubscriptionCap:
    def __init__(self, rows: list[dict[str, Any]]):
        self.rows = rows

    def call_tool(self, tool: str, **kwargs: Any) -> Any:
        assert tool == "list_subscriptions"
        return {"subscriptions": self.rows}


def _factory_helper():
    task_root = HF_ROOT / "eval_set/team_building/factory_visit_safety_day"
    return task_root, _load_rubric_module(task_root, "_helpers", "factory")


def _factory_env(
    *,
    target: str = "工厂参访执行前政策更新",
    trace_type: str = "policy_update",
    backend_target: str | None = None,
    backend_type: str = "policy_update",
    status: str = "active",
    include_trace: bool = True,
    trace_success: bool = True,
):
    calls = []
    if include_trace:
        calls.extend(
            [
                {
                    "type": "tool_call",
                    "id": "subscription-call",
                    "name": "notification_hub__create_subscription",
                    "arguments": {"target": target, "type": trace_type},
                },
                {
                    "type": "tool_result",
                    "id": "subscription-call",
                    "name": "notification_hub__create_subscription",
                    "success": trace_success,
                    "result": {"target": target, "type": trace_type},
                },
            ]
        )
    rows = [
        {
            "target": target if backend_target is None else backend_target,
            "type": backend_type,
            "status": status,
        }
    ]
    return SimpleNamespace(
        workspace=SimpleNamespace(fs=_ExistingTraceFS({18: calls})),
        notification_hub_mock=_SubscriptionCap(rows),
    )


def test_factory_accepts_stage18_free_text_policy_subscription_bound_to_backend() -> None:
    _, helper = _factory_helper()
    assert helper.active_subscription_created_at_stage(
        _factory_env(), 18, "policy_update"
    ) is True


def test_factory_rejects_unbound_or_inactive_subscription() -> None:
    _, helper = _factory_helper()
    cases = [
        _factory_env(include_trace=False),
        _factory_env(trace_type="keyword"),
        _factory_env(target="  "),
        _factory_env(backend_target="different target"),
        _factory_env(status="paused"),
        _factory_env(trace_success=False),
    ]
    for env in cases:
        assert helper.active_subscription_created_at_stage(
            env, 18, "policy_update"
        ) is False


def test_factory_rubrics_have_no_private_topic_contract() -> None:
    task_root, _ = _factory_helper()
    source = "\n".join(
        (task_root / path).read_text(encoding="utf-8")
        for path in (
            "rubrics/_helpers.py",
            "rubrics/stage_18.py",
            "rubrics/tool_quality.py",
        )
    )
    assert "factory_visit_preflight_updates" not in source
    assert "工厂参访复盘与SOP整改" not in source


def _east_china_helper():
    task_root = HF_ROOT / "eval_set/travel/east_china_bereavement_docs_reissue"
    return task_root, _load_rubric_module(task_root, "_helpers", "east_china")


def test_east_china_stage7_does_not_require_future_appointment_number(
    monkeypatch,
) -> None:
    _, helper = _east_china_helper()
    captured: list[list[list[str]]] = []
    monkeypatch.setattr(helper, "_active_rail", lambda *args, **kwargs: True)
    monkeypatch.setattr(helper, "_active_hotel", lambda *args, **kwargs: True)

    def calendar_matches(env, groups):
        captured.append(groups)
        assert all(helper.APPT_NO not in group for group in groups)
        return [{"event_id": "plan"}, {"event_id": "buffer"}]

    monkeypatch.setattr(helper, "_calendar_matches", calendar_matches)

    assert helper.check_s7_shanghai_window_plan(object()) is True
    assert captured == [[["上海", "窗口"], [helper.DATE_WINDOW]]]


def test_east_china_stage13_still_requires_appointment_number() -> None:
    task_root, _ = _east_china_helper()
    source = (task_root / "rubrics/_helpers.py").read_text(encoding="utf-8")
    stage7 = source[source.index("def check_s7_") : source.index("def check_s8_")]
    stage13 = source[source.index("def check_s13_") : source.index("def check_s14_")]
    assert "APPT_NO" not in stage7
    assert "APPT_NO" in stage13


def test_stroller_stage8_prompt_does_not_require_each_individually_cheapest_item() -> None:
    path = HF_ROOT / "eval_set/shopping/baby_stroller_safety_standard_30d/event.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    stage8 = payload["stages"].get(8, payload["stages"].get("8"))
    visible = "\n".join(str(event.get("body") or "") for event in stage8)
    assert "每类选中的最便宜款" not in visible
    assert "哪些券" in visible

class _ShadowedWorkspaceFS:
    def read_file(self, path: str) -> bytes:
        files = {
            "/workspace/itinerary.md": b"# Itinerary\n",
            "/terrarium/openclaw/workspace/itinerary.md": (
                "# Itinerary\nagent update\n"
            ).encode("utf-8"),
        }
        if path not in files:
            raise FileNotFoundError(path)
        return files[path]


def test_galapagos_prefers_live_workspace_over_seeded_compatibility_copy() -> None:
    task_root = HF_ROOT / "eval_set/travel/galapagos_no_us_transit"
    helper = _load_rubric_module(task_root, "_helpers", "galapagos_helpers")
    env = SimpleNamespace(workspace=SimpleNamespace(fs=_ShadowedWorkspaceFS()))

    text = helper.read_file(env, "/workspace/itinerary.md")

    assert "agent update" in text


def test_galapagos_hotel_owner_trace_parses_json_and_nested_function_shapes() -> None:
    _, backend = _galapagos_backend()
    owner = "linqiao@example.com"
    trace_shapes = [
        {
            "type": "tool_call",
            "name": "hotel_booking.create_reservation",
            "arguments": json.dumps(
                {"guest_profile": {"user_id": owner, "email": owner}}
            ),
        },
        {
            "type": "tool_call",
            "function": {
                "name": "hotel_booking.create_reservation",
                "arguments": json.dumps(
                    {"guest_profile": {"user_id": owner, "email": owner}}
                ),
            },
        },
    ]
    for idx, call in enumerate(trace_shapes):
        env = SimpleNamespace(
            workspace=SimpleNamespace(fs=_TraceFS({idx: [call]})),
            hotel_booking_mock=_HotelCap(),
        )
        assert backend.hotel_reservations(env)[0]["reservation_id"] == "RES1"

    malformed = {
        "type": "tool_call",
        "name": "hotel_booking.create_reservation",
        "arguments": "{not-json",
    }
    env = SimpleNamespace(
        workspace=SimpleNamespace(fs=_TraceFS({3: [malformed]})),
        hotel_booking_mock=_HotelCap(),
    )
    assert backend.hotel_reservations(env) == []


class _NotionReviewCap:
    def __init__(self, title: str):
        self.title = title

    def call_tool(self, tool: str, **kwargs: Any) -> Any:
        if tool == "API-post-search":
            return {"results": [{"id": "page-review", "title": self.title}]}
        if tool == "API-get-block-children":
            return {
                "results": [
                    {
                        "text": (
                            "预算与发票已核对；供应商评价已归档；"
                            "安全与隐私事件已复盘；未付款项目待确认授权；"
                            "下次 SOP 整改已列出。"
                        )
                    }
                ]
            }
        raise AssertionError(tool)


def test_factory_final_review_accepts_semantic_title_and_rejects_generic_title() -> None:
    _, helper = _factory_helper()
    semantic = SimpleNamespace(notion_mock=_NotionReviewCap("工厂参访最终复盘与下次 SOP"))
    generic = SimpleNamespace(notion_mock=_NotionReviewCap("普通记录"))

    assert helper.final_review_written(semantic) is True
    assert helper.final_review_written(generic) is False


def _pottery_helper():
    task_root = HF_ROOT / "eval_set/team_building/pottery_invoice_compliance_day"
    return task_root, _load_rubric_module(task_root, "_helpers", "pottery")


class _PotteryFS:
    def __init__(
        self,
        seed_root: Path,
        *,
        traces: dict[int, list[dict[str, Any]]] | None = None,
        overrides: dict[str, str] | None = None,
    ):
        self.seed_root = seed_root
        self.traces = traces or {}
        self.overrides = overrides or {}

    def _content(self, path: str) -> bytes:
        for stage, rows in self.traces.items():
            if path.endswith(f"stage_{stage}.json"):
                return json.dumps(rows, ensure_ascii=False).encode("utf-8")
        basename = Path(path).name
        if basename in self.overrides:
            return self.overrides[basename].encode("utf-8")
        source = self.seed_root / basename
        if source.is_file():
            return source.read_bytes()
        raise FileNotFoundError(path)

    def exists(self, path: str) -> bool:
        try:
            self._content(path)
        except FileNotFoundError:
            return False
        return True

    def read_file(self, path: str) -> bytes:
        return self._content(path)


def _pottery_env(
    *,
    traces: dict[int, list[dict[str, Any]]] | None = None,
    overrides: dict[str, str] | None = None,
):
    task_root, helper = _pottery_helper()
    fs = _PotteryFS(task_root / "workspace", traces=traces, overrides=overrides)
    return helper, SimpleNamespace(workspace=SimpleNamespace(fs=fs))


def test_pottery_publisher_seed_passes_its_own_structure_gate() -> None:
    helper, env = _pottery_env()
    assert helper.workspace_is_structured(env) is True


def test_pottery_unrelated_structure_failure_does_not_zero_business_evidence() -> None:
    helper, env = _pottery_env(
        overrides={"team_roster.csv": "group,total_count\nall,27\n"}
    )
    assert helper.workspace_is_structured(env) is False
    assert helper.state_has(env, [["发票"], ["预算"]]) is True


def _paired_workspace_trace(
    *,
    name: str,
    arguments: dict[str, Any],
    success: bool = True,
    include_result: bool = True,
) -> list[dict[str, Any]]:
    rows = [
        {
            "type": "tool_call",
            "id": "workspace-call",
            "name": name,
            "arguments": arguments,
        }
    ]
    if include_result:
        rows.append(
            {
                "type": "tool_result",
                "id": "workspace-call",
                "name": name,
                "success": success,
                "result": {"path": arguments.get("path")},
            }
        )
    return rows


def test_pottery_successful_workspace_write_and_edit_are_targeted_persistence() -> None:
    content = "vendor_name,invoice,status\n釉见,服务类发票,资质已核验且含烧制,候选\n"
    traces = [
        _paired_workspace_trace(
            name="write",
            arguments={
                "path": "/terrarium/openclaw/workspace/vendor_shortlist.csv",
                "content": content,
            },
        ),
        _paired_workspace_trace(
            name="edit",
            arguments={
                "path": "/terrarium/openclaw/workspace/vendor_shortlist.csv",
                "edits": [{"oldText": "旧值", "newText": "服务类 资质 烧制"}],
            },
        ),
    ]
    for rows in traces:
        helper, env = _pottery_env(
            traces={2: rows}, overrides={"vendor_shortlist.csv": content}
        )
        assert helper.stage_has_targeted_write(
            env, "s2_shortlist_has_invoice_fields"
        ) is True


def test_pottery_workspace_persistence_rejects_failed_unpaired_or_unrelated_writes() -> None:
    valid_content = "vendor_name,invoice,status\n釉见,服务类发票,资质已核验且含烧制,候选\n"
    cases = [
        _paired_workspace_trace(
            name="write",
            arguments={
                "path": "/terrarium/openclaw/workspace/vendor_shortlist.csv",
                "content": valid_content,
            },
            success=False,
        ),
        _paired_workspace_trace(
            name="write",
            arguments={
                "path": "/terrarium/openclaw/workspace/vendor_shortlist.csv",
                "content": valid_content,
            },
            include_result=False,
        ),
        _paired_workspace_trace(
            name="write",
            arguments={
                "path": "/terrarium/openclaw/workspace/notes.md",
                "content": valid_content,
            },
        ),
        _paired_workspace_trace(
            name="write",
            arguments={
                "path": "/terrarium/openclaw/workspace/vendor_shortlist.csv",
                "content": "unrelated",
            },
        ),
    ]
    for rows in cases:
        helper, env = _pottery_env(
            traces={2: rows}, overrides={"vendor_shortlist.csv": valid_content}
        )
        assert helper.stage_has_targeted_write(
            env, "s2_shortlist_has_invoice_fields"
        ) is False
