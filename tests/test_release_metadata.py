from __future__ import annotations

import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "1.1.1"


def test_project_readme_and_all_open_tasks_share_release_version() -> None:
    project = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["version"] == EXPECTED_VERSION

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert f"**Benchmark version:** `{EXPECTED_VERSION}`" in readme

    task_files = sorted((REPO_ROOT / "eval_set").glob("*/*/task.toml"))
    assert len(task_files) == 20
    for task_file in task_files:
        metadata = tomllib.loads(task_file.read_text(encoding="utf-8"))["metadata"]
        assert metadata["name"] == task_file.parent.name
        assert metadata["version"] == EXPECTED_VERSION, task_file
