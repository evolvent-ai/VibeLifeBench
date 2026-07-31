from __future__ import annotations

import ast
import importlib.util
import inspect
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVAL_ROOT = ROOT / "eval_set"
SERVER_ROOT = ROOT / "servers"

EXPECTED_TASKS = {
    "career/career_equity_buyback_recovery",
    "career/career_espp_refund_recovery",
    "exam_preparation/civil_service_written_to_interview_audit",
    "exam_preparation/pharmacist_western_registration_shift_prep",
    "finance/arm_escrow_shortfall_reset_guard_30d",
    "finance/hsa_medical_bill_liquidity_guard_30d",
    "fitness/broadcast_exam_posture_breathing_32d",
    "fitness/dragon_boat_newcomer_upper_body_endurance_037",
    "litigation/food_safety_dispute_33d",
    "litigation/private_lending_33d",
    "renovation/garage_adu_rental_conversion_25d",
    "renovation/office_fitout_15d",
    "rental/cross_city_remote_viewing_rental",
    "rental/wheelchair_student_accessible_rental",
    "shopping/baby_stroller_safety_standard_30d",
    "shopping/central_ac_install_30d",
    "team_building/factory_visit_safety_day",
    "team_building/pottery_invoice_compliance_day",
    "travel/east_china_bereavement_docs_reissue",
    "travel/galapagos_no_us_transit",
}

REPORT_AUDIT_MATRIX = {
    "career": {"helper_signatures", "tool_schema", "minor_units", "hidden_import_gate"},
    "exam_preparation": {"helper_signatures", "tool_schema", "workspace_contract"},
    "finance": {"helper_signatures", "tool_schema", "compound_checks"},
    "fitness": {"helper_signatures", "tool_schema", "safe_empty_state", "stage_markers"},
    "litigation": {"helper_signatures", "tool_schema", "case_normalization", "email_primary_key"},
    "renovation": {"helper_signatures", "tool_schema", "single_responsibility"},
    "rental": {"helper_signatures", "tool_schema", "wildcard_tools", "scoring_entrypoint"},
    "shopping": {"helper_signatures", "tool_schema", "cart_optimum", "negative_semantics", "anchors"},
    "team_building": {"helper_signatures", "tool_schema", "wildcard_tools", "seed_structure", "workspace_writes"},
    "travel": {"helper_signatures", "tool_schema", "hidden_ids", "stage_visibility", "workspace_precedence", "currency"},
}


def _tasks() -> list[Path]:
    return sorted(path for path in EVAL_ROOT.glob("*/*") if path.is_dir())


def _load_rubric(task: str, module_name: str, alias: str) -> ModuleType:
    task_root = EVAL_ROOT / task
    package_name = f"_report_audit_{alias}_rubrics"
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


def test_report_audit_covers_all_ten_domains_and_twenty_tasks() -> None:
    actual = {path.relative_to(EVAL_ROOT).as_posix() for path in _tasks()}
    assert actual == EXPECTED_TASKS
    assert set(REPORT_AUDIT_MATRIX) == {path.parent.name for path in _tasks()}
    assert all("helper_signatures" in probes for probes in REPORT_AUDIT_MATRIX.values())
    assert all("tool_schema" in probes for probes in REPORT_AUDIT_MATRIX.values())


def _function_contracts(helper_path: Path) -> dict[str, tuple[int, int, bool, set[str], set[str], bool]]:
    tree = ast.parse(helper_path.read_text(encoding="utf-8"))
    result = {}
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        args = node.args
        positional = args.posonlyargs + args.args
        required = len(positional) - len(args.defaults)
        names = {arg.arg for arg in (*positional, *args.kwonlyargs)}
        required_kwonly = {
            arg.arg
            for arg, default in zip(args.kwonlyargs, args.kw_defaults)
            if default is None
        }
        result[node.name] = (
            required,
            len(positional),
            args.vararg is not None,
            required_kwonly,
            names,
            args.kwarg is not None,
        )
    return result


def test_rubric_helper_calls_match_helper_signatures() -> None:
    failures: list[tuple[str, int, str, str]] = []
    for task in _tasks():
        helper_path = task / "rubrics" / "_helpers.py"
        if not helper_path.exists():
            continue
        contracts = _function_contracts(helper_path)
        for path in sorted((task / "rubrics").glob("*.py")):
            if path.name in {"_helpers.py", "__init__.py"}:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for call in ast.walk(tree):
                if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Name):
                    continue
                contract = contracts.get(call.func.id)
                if contract is None:
                    continue
                required, maximum, has_vararg, required_kwonly, names, has_varkw = contract
                positional_count = len(call.args)
                keywords = {kw.arg for kw in call.keywords if kw.arg is not None}
                invalid = (
                    (not has_vararg and positional_count > maximum)
                    or positional_count + len(keywords) < required
                    or not required_kwonly <= keywords
                    or (not has_varkw and bool(keywords - names))
                )
                if invalid:
                    failures.append(
                        (
                            path.relative_to(ROOT).as_posix(),
                            call.lineno,
                            call.func.id,
                            f"positional={positional_count}, keywords={sorted(keywords)}",
                        )
                    )
    assert failures == []


def _mock_tool_schemas() -> dict[str, dict[str, tuple[set[str], bool]]]:
    schemas: dict[str, dict[str, tuple[set[str], bool]]] = {}
    for server in SERVER_ROOT.glob("*_mock"):
        service = server.name.removesuffix("_mock")
        tools: dict[str, tuple[set[str], bool]] = {}
        for path in server.glob("src/**/*.py"):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError):
                continue
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                decorator = next(
                    (
                        item
                        for item in node.decorator_list
                        if isinstance(item, ast.Call)
                        and isinstance(item.func, ast.Attribute)
                        and item.func.attr == "tool"
                    ),
                    None,
                )
                if decorator is None:
                    continue
                tool_name = node.name
                for keyword in decorator.keywords:
                    if (
                        keyword.arg == "name"
                        and isinstance(keyword.value, ast.Constant)
                        and isinstance(keyword.value.value, str)
                    ):
                        tool_name = keyword.value.value
                args = node.args
                names = [arg.arg for arg in (*args.posonlyargs, *args.args)]
                if names and names[0] in {"self", "cls"}:
                    names = names[1:]
                names.extend(arg.arg for arg in args.kwonlyargs)
                tools[tool_name] = (set(names), args.kwarg is not None)
        if tools:
            schemas[service] = tools
    return schemas


def _module_string_constants(tree: ast.Module) -> dict[str, str]:
    result: dict[str, str] = {}
    for node in tree.body:
        target: ast.expr | None = None
        value: ast.expr | None = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target, value = node.targets[0], node.value
        elif isinstance(node, ast.AnnAssign):
            target, value = node.target, node.value
        if (
            isinstance(target, ast.Name)
            and isinstance(value, ast.Constant)
            and isinstance(value.value, str)
        ):
            result[target.id] = value.value
    return result


def test_rubric_backend_calls_use_real_mock_tools_and_arguments() -> None:
    schemas = _mock_tool_schemas()
    failures: list[tuple[str, int, str, str, str]] = []

    def literal(node: ast.expr, constants: dict[str, str]) -> str | None:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Name):
            return constants.get(node.id)
        return None

    for task in _tasks():
        for path in sorted((task / "rubrics").glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            constants = _module_string_constants(tree)
            for call in ast.walk(tree):
                if not isinstance(call, ast.Call):
                    continue
                service = tool = None
                if (
                    isinstance(call.func, ast.Name)
                    and call.func.id
                    in {"_call", "service_call", "_safe_call", "_backend_call", "_call_mock"}
                    and len(call.args) >= 3
                ):
                    service = literal(call.args[1], constants)
                    tool = literal(call.args[2], constants)
                elif (
                    isinstance(call.func, ast.Attribute)
                    and call.func.attr == "call_tool"
                    and call.args
                ):
                    owner = call.func.value
                    if (
                        isinstance(owner, ast.Attribute)
                        and isinstance(owner.value, ast.Name)
                        and owner.value.id == "env"
                        and owner.attr.endswith("_mock")
                    ):
                        service = owner.attr.removesuffix("_mock")
                        tool = literal(call.args[0], constants)
                if not service or not tool or service not in schemas:
                    continue
                if tool not in schemas[service]:
                    failures.append(
                        (path.relative_to(ROOT).as_posix(), call.lineno, service, tool, "missing tool")
                    )
                    continue
                accepted, has_varkw = schemas[service][tool]
                supplied = {kw.arg for kw in call.keywords if kw.arg is not None}
                unexpected = supplied - accepted
                if unexpected and not has_varkw:
                    failures.append(
                        (
                            path.relative_to(ROOT).as_posix(),
                            call.lineno,
                            service,
                            tool,
                            f"unexpected arguments: {sorted(unexpected)}",
                        )
                    )
    assert failures == []


class _TraceFS:
    def __init__(self, rows: list[dict[str, Any]]):
        self.payload = json.dumps(rows).encode("utf-8")

    def exists(self, path: str) -> bool:
        return path == "/terrarium/agent_traces/stage_2.json"

    def read_file(self, path: str) -> bytes:
        assert self.exists(path)
        return self.payload


def test_factory_value_matcher_treats_tool_none_as_any_tool_on_server() -> None:
    helper = _load_rubric(
        "team_building/factory_visit_safety_day", "_helpers", "factory_wildcard"
    )
    env = SimpleNamespace(
        workspace=SimpleNamespace(
            fs=_TraceFS(
                [
                    {
                        "type": "tool_call",
                        "name": "banking__list_transactions",
                        "arguments": {"account_id": "acct_factory_main", "limit": 50},
                    }
                ]
            )
        )
    )

    assert helper.used_tool_with_value(
        env, 2, "banking", None, ["acct_factory_main"]
    ) is True
    assert helper.used_tool_with_value(env, 2, "email", None, ["acct_factory_main"]) is False
    assert helper.used_tool_with_value(env, 2, "banking", None, ["other-account"]) is False


def test_shopping_negative_semantics_and_all_anchor_occurrences_are_active() -> None:
    for task, alias in (
        ("shopping/central_ac_install_30d", "central_ac_semantics"),
        ("shopping/baby_stroller_safety_standard_30d", "stroller_semantics"),
    ):
        helper = _load_rubric(task, "_helpers", alias)
        assert helper._has_unqualified_phrase("可以直接绕过安全检查", "绕过安全检查") is True
        assert helper._has_unqualified_phrase("不要直接绕过安全检查", "绕过安全检查") is False
        text = "目录：THREAD-A\n" + ("占位" * 200) + "\nTHREAD-A 正文：来源、观察、动作、状态"
        windows = helper._thread_anchor_windows(text, "THREAD-A", window=80)
        assert len(windows) == 2
        assert any("正文" in window for window in windows)


def test_event_mutations_reference_existing_sql_files() -> None:
    missing: list[tuple[str, int, str]] = []
    import yaml

    for task in _tasks():
        event_path = task / "event.yaml"
        if not event_path.exists():
            continue
        data = yaml.safe_load(event_path.read_text(encoding="utf-8")) or {}
        for stage, events in (data.get("stages") or {}).items():
            for event in events or []:
                for apply in event.get("apply") or []:
                    relative = apply.get("sql_file")
                    if relative and not (task / relative).is_file():
                        missing.append((task.relative_to(EVAL_ROOT).as_posix(), int(stage), relative))
    assert missing == []


def test_career_has_no_broken_absolute_audit_import_gate() -> None:
    failures = []
    for task in sorted(path for path in (EVAL_ROOT / "career").iterdir() if path.is_dir()):
        source = (task / "task.py").read_text(encoding="utf-8")
        if "from tasks.career" in source or "_has_compliant_audit" in source:
            failures.append(task.name)
    assert failures == []
