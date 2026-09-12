"""Validated, read-only access to Harbor's immutable stage evidence."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REQUIRED_FILES = ("snapshot.json", "trace.json", "response.txt", "trajectory.json")


class EvidenceError(RuntimeError):
    """Frozen evidence is missing, unreadable, or fails integrity checks."""


class HarborEvidence:
    """A cached reader over ``stages/stage-NN`` with no live capabilities."""

    def __init__(self, root: Path | str = DEFAULT_EVIDENCE_ROOT) -> None:
        self.root = Path(root)
        self._validated: set[int] = set()
        self._cache: dict[tuple[int, str], Any] = {}
        self.current_stage: int | None = None

    def _stage_dir(self, stage: int) -> Path:
        if not isinstance(stage, int) or stage < 0:
            raise EvidenceError(f"invalid stage {stage!r}")
        return self.root / "stages" / f"stage-{stage:02d}"

    @staticmethod
    def _read_json(path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise EvidenceError(f"unreadable evidence file {path}: {exc}") from exc
        except ValueError as exc:
            raise EvidenceError(f"malformed JSON in {path}: {exc}") from exc

    def validate_stage(self, stage: int) -> Path:
        stage_dir = self._stage_dir(stage)
        if stage in self._validated:
            return stage_dir
        if not stage_dir.is_dir():
            raise EvidenceError(f"no frozen evidence for stage {stage} at {stage_dir}")
        manifest_path = stage_dir / "manifest.json"
        if not manifest_path.is_file():
            raise EvidenceError(f"stage {stage} has no manifest at {manifest_path}")
        manifest = self._read_json(manifest_path)
        if not isinstance(manifest, dict):
            raise EvidenceError(f"stage {stage} manifest is not an object")
        if manifest.get("schema_version") != 1 or manifest.get("kind") != "stage":
            raise EvidenceError(f"stage {stage} manifest type mismatch")
        if int(manifest.get("virtual_stage", -1)) != stage:
            raise EvidenceError(f"stage {stage} manifest number mismatch")
        hashes = manifest.get("hashes")
        if not isinstance(hashes, dict) or not hashes:
            raise EvidenceError(f"stage {stage} manifest carries no file hashes")
        declared = set(hashes)
        on_disk = {
            str(path.relative_to(stage_dir))
            for path in stage_dir.rglob("*")
            if path.is_file() and not path.is_symlink() and path.name != "manifest.json"
        }
        if on_disk != declared:
            raise EvidenceError(
                f"stage {stage} manifest/disk mismatch: "
                f"undeclared={sorted(on_disk - declared)[:5]} "
                f"missing={sorted(declared - on_disk)[:5]}"
            )
        missing = [name for name in REQUIRED_FILES if name not in hashes]
        if missing:
            raise EvidenceError(f"stage {stage} manifest omits required file(s): {missing}")
        for name, expected in hashes.items():
            target = stage_dir / name
            if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                raise EvidenceError(f"stage {stage} hash mismatch: {name}")
        self._validated.add(stage)
        return stage_dir

    def _load(self, stage: int, filename: str) -> Any:
        key = (stage, filename)
        if key in self._cache:
            return self._cache[key]
        path = self.validate_stage(stage) / filename
        try:
            value = path.read_text(encoding="utf-8") if filename.endswith(".txt") else self._read_json(path)
        except OSError as exc:
            raise EvidenceError(f"unreadable evidence file {path}: {exc}") from exc
        self._cache[key] = value
        return value

    def snapshot(self, stage: int) -> dict[str, Any]:
        value = self._load(stage, "snapshot.json")
        if not isinstance(value, dict):
            raise EvidenceError(f"stage {stage} snapshot is not an object")
        if value.get("stage") != stage:
            raise EvidenceError(f"stage {stage} snapshot number mismatch")
        if "error" in value and not any(key != "error" for key in value):
            raise EvidenceError(f"stage {stage} snapshot captured an error: {value['error']!r}")
        return value

    def trace(self, stage: int) -> list[dict[str, Any]]:
        value = self._load(stage, "trace.json")
        if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
            raise EvidenceError(f"stage {stage} trace is not an object list")
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
        result: list[int] = []
        for path in sorted(stages_root.glob("stage-*")):
            try:
                result.append(int(path.name.removeprefix("stage-")))
            except ValueError:
                continue
        return result

    def active_stage(self) -> int:
        if self.current_stage is not None:
            return self.current_stage
        stages = self.published_stages()
        if not stages:
            raise EvidenceError("no published stages available")
        return max(stages)


def snapshot(env: HarborEvidence, stage: int) -> dict[str, Any]:
    return env.snapshot(stage)


def trace(env: HarborEvidence, stage: int) -> list[dict[str, Any]]:
    return env.trace(stage)


def response(env: HarborEvidence, stage: int) -> str:
    return env.response(stage)
