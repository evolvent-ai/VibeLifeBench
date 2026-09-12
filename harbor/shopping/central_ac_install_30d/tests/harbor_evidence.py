"""Validated access to immutable Harbor stage evidence."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REQUIRED_FILES = ("snapshot.json", "trace.json", "response.txt", "trajectory.json")


class EvidenceError(RuntimeError):
    """The frozen sidecar is missing, malformed, or changed."""


class HarborEvidence:
    """Read and validate one immutable stage sidecar at a time."""

    def __init__(self, root: Path | str = DEFAULT_EVIDENCE_ROOT) -> None:
        self.root = Path(root)
        self._validated: set[int] = set()
        self._cache: dict[tuple[int, str], Any] = {}
        self._active_stage = 0

    @property
    def active_stage(self) -> int:
        return self._active_stage

    def set_active_stage(self, stage: int) -> None:
        self._active_stage = int(stage)

    def _stage_dir(self, stage: int) -> Path:
        return self.root / "stages" / f"stage-{int(stage):02d}"

    @staticmethod
    def _json(path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise EvidenceError(f"unreadable evidence file: {path}") from exc
        except json.JSONDecodeError as exc:
            raise EvidenceError(f"malformed JSON evidence: {path}") from exc

    def validate_stage(self, stage: int) -> Path:
        stage = int(stage)
        stage_dir = self._stage_dir(stage)
        if stage in self._validated:
            return stage_dir
        if not stage_dir.is_dir():
            raise EvidenceError(f"missing frozen evidence for stage {stage}")
        manifest_path = stage_dir / "manifest.json"
        manifest = self._json(manifest_path)
        if not isinstance(manifest, dict):
            raise EvidenceError(f"stage {stage} manifest is not an object")
        if manifest.get("schema_version") != 1 or manifest.get("kind") != "stage":
            raise EvidenceError(f"stage {stage} manifest type mismatch")
        if int(manifest.get("virtual_stage", -1)) != stage:
            raise EvidenceError(f"stage {stage} manifest number mismatch")
        hashes = manifest.get("hashes")
        if not isinstance(hashes, dict) or not hashes:
            raise EvidenceError(f"stage {stage} manifest has no hashes")
        actual = {
            str(path.relative_to(stage_dir))
            for path in stage_dir.rglob("*")
            if path.is_file() and not path.is_symlink() and path.name != "manifest.json"
        }
        if actual != set(hashes):
            raise EvidenceError(f"stage {stage} manifest file set mismatch")
        if not set(REQUIRED_FILES).issubset(actual):
            raise EvidenceError(f"stage {stage} is missing a required evidence file")
        for name, expected in hashes.items():
            target = stage_dir / name
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if not isinstance(expected, str) or digest != expected:
                raise EvidenceError(f"stage {stage} hash mismatch: {name}")
        self._validated.add(stage)
        return stage_dir

    def _load(self, stage: int, filename: str) -> Any:
        key = (int(stage), filename)
        if key not in self._cache:
            directory = self.validate_stage(stage)
            path = directory / filename
            if filename.endswith(".txt"):
                try:
                    value = path.read_text(encoding="utf-8")
                except OSError as exc:
                    raise EvidenceError(f"unreadable evidence file: {path}") from exc
            else:
                value = self._json(path)
            self._cache[key] = value
        return self._cache[key]

    def snapshot(self, stage: int) -> dict[str, Any]:
        value = self._load(stage, "snapshot.json")
        if not isinstance(value, dict):
            raise EvidenceError(f"stage {stage} snapshot is not an object")
        if "error" in value and not any(key != "error" for key in value):
            raise EvidenceError(f"stage {stage} snapshot captured an error")
        return value

    def trace(self, stage: int) -> list[dict[str, Any]]:
        value = self._load(stage, "trace.json")
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            raise EvidenceError(f"stage {stage} trace is not a list of objects")
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
        root = self.root / "stages"
        if not root.is_dir():
            raise EvidenceError(f"missing evidence stages directory: {root}")
        result: list[int] = []
        for path in sorted(root.glob("stage-*")):
            try:
                result.append(int(path.name.removeprefix("stage-")))
            except ValueError:
                continue
        return result


def snapshot(env: HarborEvidence, stage: int) -> dict[str, Any]:
    return env.snapshot(stage)


def trace(env: HarborEvidence, stage: int) -> list[dict[str, Any]]:
    return env.trace(stage)


def response(env: HarborEvidence, stage: int) -> str:
    return env.response(stage)
