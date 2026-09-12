"""Validated access to immutable Harbor stage evidence."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


DEFAULT_EVIDENCE_ROOT = Path(
    os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence")
)
REQUIRED_FILES = ("snapshot.json", "trace.json", "response.txt", "trajectory.json")


class EvidenceError(RuntimeError):
    """Frozen evidence is missing, malformed, or inconsistent with its manifest."""


class HarborEvidence:
    """Read and cache the world-controller's immutable per-stage evidence."""

    def __init__(self, root: Path | str = DEFAULT_EVIDENCE_ROOT) -> None:
        self.root = Path(root)
        self._validated: set[int] = set()
        self._cache: dict[tuple[int, str], Any] = {}
        self._rubric_stage: int | None = None

    def _stage_dir(self, stage: int) -> Path:
        if isinstance(stage, bool) or not isinstance(stage, int) or stage < 0:
            raise EvidenceError(f"invalid virtual stage: {stage!r}")
        return self.root / "stages" / f"stage-{stage:02d}"

    @staticmethod
    def _read_json(path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise EvidenceError(f"unreadable evidence file {path}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise EvidenceError(f"malformed JSON in {path}: {exc}") from exc

    def validate_stage(self, stage: int) -> Path:
        """Validate the manifest, declared file set, and every recorded hash."""
        stage_dir = self._stage_dir(stage)
        if stage in self._validated:
            return stage_dir
        if not stage_dir.is_dir():
            raise EvidenceError(f"no frozen evidence for stage {stage} at {stage_dir}")

        manifest_path = stage_dir / "manifest.json"
        manifest = self._read_json(manifest_path)
        if not isinstance(manifest, dict):
            raise EvidenceError(f"stage {stage} manifest is not an object")
        if manifest.get("schema_version") != 1:
            raise EvidenceError(f"stage {stage} has an unsupported manifest schema")
        if manifest.get("kind") != "stage":
            raise EvidenceError(f"stage {stage} manifest is not stage evidence")
        if manifest.get("virtual_stage") != stage:
            raise EvidenceError(f"stage {stage} manifest declares a different stage")

        hashes = manifest.get("hashes")
        if not isinstance(hashes, dict) or not hashes:
            raise EvidenceError(f"stage {stage} manifest has no file hashes")
        missing = sorted(set(REQUIRED_FILES) - set(hashes))
        if missing:
            raise EvidenceError(f"stage {stage} manifest omits required files: {missing}")

        on_disk = {
            str(path.relative_to(stage_dir))
            for path in stage_dir.rglob("*")
            if path.is_file() and not path.is_symlink() and path.name != "manifest.json"
        }
        if on_disk != set(hashes):
            raise EvidenceError(
                f"stage {stage} manifest file set differs from disk: "
                f"undeclared={sorted(on_disk - set(hashes))[:5]}, "
                f"missing={sorted(set(hashes) - on_disk)[:5]}"
            )

        for relative, expected in hashes.items():
            if not isinstance(relative, str) or not isinstance(expected, str):
                raise EvidenceError(f"stage {stage} manifest contains an invalid hash entry")
            target = stage_dir / relative
            try:
                actual = hashlib.sha256(target.read_bytes()).hexdigest()
            except OSError as exc:
                raise EvidenceError(f"unreadable evidence file {target}: {exc}") from exc
            if actual != expected:
                raise EvidenceError(f"stage {stage} file {relative} failed hash validation")

        self._validated.add(stage)
        return stage_dir

    def _load(self, stage: int, filename: str) -> Any:
        key = (stage, filename)
        if key in self._cache:
            return self._cache[key]
        path = self.validate_stage(stage) / filename
        if filename.endswith(".txt"):
            try:
                value: Any = path.read_text(encoding="utf-8")
            except OSError as exc:
                raise EvidenceError(f"unreadable evidence file {path}: {exc}") from exc
        else:
            value = self._read_json(path)
        self._cache[key] = value
        return value

    def snapshot(self, stage: int) -> dict[str, Any]:
        value = self._load(stage, "snapshot.json")
        if not isinstance(value, dict):
            raise EvidenceError(f"stage {stage} snapshot is not an object")
        if value.get("stage") != stage:
            raise EvidenceError(f"stage {stage} snapshot declares a different stage")
        if "error" in value and not any(key != "error" for key in value):
            raise EvidenceError(f"stage {stage} snapshot records a capture error")
        return value

    def trace(self, stage: int) -> list[dict[str, Any]]:
        value = self._load(stage, "trace.json")
        if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
            raise EvidenceError(f"stage {stage} trace must be a list of objects")
        return value

    def response(self, stage: int) -> str:
        value = self._load(stage, "response.txt")
        if not isinstance(value, str):
            raise EvidenceError(f"stage {stage} response is not text")
        return value

    def trajectory(self, stage: int) -> dict[str, Any]:
        value = self._load(stage, "trajectory.json")
        if not isinstance(value, dict):
            raise EvidenceError(f"stage {stage} trajectory is not an object")
        return value

    def published_stages(self) -> list[int]:
        stages_root = self.root / "stages"
        if not stages_root.is_dir():
            return []
        stages: list[int] = []
        for path in stages_root.glob("stage-*"):
            if not path.is_dir() or path.is_symlink():
                continue
            suffix = path.name.removeprefix("stage-")
            if suffix.isdigit():
                stages.append(int(suffix))
        return sorted(stages)


def snapshot(env: HarborEvidence, stage: int) -> dict[str, Any]:
    return env.snapshot(stage)


def trace(env: HarborEvidence, stage: int) -> list[dict[str, Any]]:
    return env.trace(stage)


def response(env: HarborEvidence, stage: int) -> str:
    return env.response(stage)
