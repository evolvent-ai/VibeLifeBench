from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_DIRS = sorted(path.parent for path in (ROOT / "eval_set").glob("*/*/task.py"))
REMOVED_ARTIFACTS = (
    ROOT / "scripts" / "backend_gate_manifest.py",
    ROOT / "scripts" / "render_backend_gates.py",
    ROOT / "scripts" / "sync_backend_gate_tasks.py",
    ROOT / "docs" / "superpowers" / "plans" / "2026-07-30-backend-first-rubric-gates.md",
    ROOT / "docs" / "superpowers" / "plans" / "2026-07-30-check-level-backend-gates.md",
    ROOT / "docs" / "superpowers" / "plans" / "2026-07-30-check-specific-read-facts-and-demo-audit.md",
    ROOT / "docs" / "superpowers" / "specs" / "2026-07-30-backend-first-rubric-gates-design.md",
    ROOT / "docs" / "superpowers" / "specs" / "2026-07-30-check-level-backend-gates-design.md",
    ROOT / "docs" / "superpowers" / "specs" / "2026-07-30-check-specific-read-facts-and-demo-audit-design.md",
)
FORBIDDEN_NAMES = {
    "_backend_gate_context",
    "_backend_gate_module",
    "BackendGateInfrastructureError",
    "GateContext",
}


def test_release_contains_no_backend_gate_artifacts() -> None:
    assert len(TASK_DIRS) == 20
    assert not list((ROOT / "eval_set").glob("*/*/rubrics/backend_gates.py"))
    assert not (ROOT / "docs" / "superpowers").exists()
    assert all(not path.exists() for path in REMOVED_ARTIFACTS)


def test_task_entrypoints_execute_quality_checks_without_gate_wrapper() -> None:
    failures: list[str] = []
    for task_dir in TASK_DIRS:
        task_file = task_dir / "task.py"
        source = task_file.read_text(encoding="utf-8")
        tree = ast.parse(source)
        names = {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
        }
        attrs = {
            node.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Attribute)
        }
        strings = {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        forbidden = sorted((names | strings) & FORBIDDEN_NAMES)
        if "run_check" in attrs:
            forbidden.append("run_check")
        if "flush_diagnostics" in attrs:
            forbidden.append("flush_diagnostics")
        lowered = source.lower()
        if "backend_gate" in lowered or "backend gate" in lowered:
            forbidden.append("backend_gate")
        if "gated_check" in lowered or "gated check" in lowered:
            forbidden.append("gated_check")
        if forbidden:
            failures.append(f"{task_dir.relative_to(ROOT)}: {sorted(set(forbidden))}")
    assert not failures, "\n".join(failures)
