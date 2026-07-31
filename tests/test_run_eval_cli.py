from __future__ import annotations

import sys
import tomllib
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts import run_eval


def _write_config(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    models_json: Path,
) -> dict:
    repo_root = tmp_path / "repo"
    repo_root.mkdir(exist_ok=True)
    task_dir = repo_root / "eval_set" / "travel" / "example_task"
    task_dir.mkdir(parents=True)
    config_path = repo_root / "outputs" / "job.toml"
    config_path.parent.mkdir()

    monkeypatch.setattr(run_eval, "REPO_ROOT", repo_root)
    run_eval.write_config(
        config_path,
        "job",
        repo_root / "outputs" / "job",
        {"example_task": task_dir},
        "provider/model",
        models_json,
        attempts=1,
        concurrent=1,
        timeout_sec=60,
        think="high",
    )
    return tomllib.loads(config_path.read_text(encoding="utf-8"))


def test_write_config_accepts_relative_models_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir(exist_ok=True)
    monkeypatch.chdir(repo_root)

    data = _write_config(monkeypatch, tmp_path, Path("models.json.example"))

    assert data["agents"][0]["kwargs"]["models_config_path"] == "models.json.example"


def test_write_config_makes_repo_absolute_models_path_relative(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    models_json = tmp_path / "repo" / "configs" / "models.json"

    data = _write_config(monkeypatch, tmp_path, models_json)

    assert data["agents"][0]["kwargs"]["models_config_path"] == "configs/models.json"


def test_write_config_preserves_external_absolute_models_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    models_json = (tmp_path / "external" / "models.json").resolve()

    data = _write_config(monkeypatch, tmp_path, models_json)

    assert data["agents"][0]["kwargs"]["models_config_path"] == str(models_json)


def test_main_resolves_user_models_path_before_preflight(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir(exist_ok=True)
    models_json = repo_root / "models.json.example"
    models_json.write_text("{}", encoding="utf-8")
    task_dir = repo_root / "eval_set" / "travel" / "example_task"
    task_dir.mkdir(parents=True)
    captured: dict[str, Path] = {}

    monkeypatch.chdir(repo_root)
    monkeypatch.setattr(run_eval, "REPO_ROOT", repo_root)
    monkeypatch.setattr(run_eval, "discover_tasks", lambda: {"example_task": task_dir})
    monkeypatch.setattr(
        run_eval,
        "preflight",
        lambda path, tasks: captured.setdefault("preflight", path),
    )
    monkeypatch.setattr(
        run_eval,
        "write_config",
        lambda path, job_name, job_dir, tasks, model, path_arg, *rest: captured.setdefault(
            "write_config", path_arg
        ),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_eval.py",
            "--model",
            "provider/model",
            "--models-json",
            "models.json.example",
            "--job-name",
            "test-relative-path",
            "--dry-run",
        ],
    )

    assert run_eval.main() == 0
    assert captured == {
        "preflight": models_json.resolve(),
        "write_config": models_json.resolve(),
    }
