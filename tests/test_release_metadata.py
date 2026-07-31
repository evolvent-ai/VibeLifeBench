from __future__ import annotations

import json
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "1.0.0"


def test_project_readme_and_all_open_tasks_share_release_version() -> None:
    project = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["version"] == EXPECTED_VERSION

    lock = (REPO_ROOT / "uv.lock").read_text(encoding="utf-8")
    assert f'name = "vibelifebench"\nversion = "{EXPECTED_VERSION}"' in lock

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert f"**Benchmark version:** `{EXPECTED_VERSION}`" in readme
    assert "1.1.0" not in readme
    assert "1.1.1" not in readme

    task_files = sorted((REPO_ROOT / "eval_set").glob("*/*/task.toml"))
    assert len(task_files) == 20
    for task_file in task_files:
        metadata = tomllib.loads(task_file.read_text(encoding="utf-8"))["metadata"]
        assert metadata["name"] == task_file.parent.name
        assert metadata["version"] == EXPECTED_VERSION, task_file


def test_changelog_starts_with_v1_release() -> None:
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [1.0.0] - 2026-07-31" in changelog
    assert "## [1.1.1]" not in changelog


def test_gpt55_example_uses_conservative_context_window() -> None:
    config = json.loads((REPO_ROOT / "models.json.example").read_text(encoding="utf-8"))
    models = config["providers"]["openai"]["models"]
    model = next(item for item in models if item["id"] == "gpt-5.5")
    assert 300_000 <= model["contextWindow"] <= 320_000
    assert model["params"]["reasoning_effort"] == "xhigh"
