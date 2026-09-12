"""Validated access to immutable Harbor stage sidecars.

Scoring reads only the frozen files under ``stages/stage-NN``.  There is no
network client, service capability, or writable workspace adapter here.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REQUIRED_FILES = ("snapshot.json", "trace.json", "response.txt", "trajectory.json")


class EvidenceError(RuntimeError):
    """Frozen evidence is missing, unreadable, or fails its manifest."""


class HarborEvidence:
    """Read and validate one immutable evidence tree."""

    def __init__(self, root: Path | str = DEFAULT_EVIDENCE_ROOT) -> None:
        self.root = Path(root)
        self._validated: set[int] = set()
        self._cache: dict[tuple[int, str], Any] = {}

    def _stage_dir(self, stage: int) -> Path:
        return self.root / "stages" / f"stage-{int(stage):02d}"

    @staticmethod
    def _read_json(path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise EvidenceError(f"unreadable evidence file {path}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise EvidenceError(f"malformed JSON in {path}: {exc}") from exc

    def validate_stage(self, stage: int) -> Path:
        stage = int(stage)
        stage_dir = self._stage_dir(stage)
        if stage in self._validated:
            return stage_dir
        if not stage_dir.is_dir():
            raise EvidenceError(f"no frozen evidence for stage {stage}: {stage_dir}")
        manifest_path = stage_dir / "manifest.json"
        if not manifest_path.is_file() or manifest_path.is_symlink():
            raise EvidenceError(f"stage {stage} has no manifest")
        manifest = self._read_json(manifest_path)
        if not isinstance(manifest, dict):
            raise EvidenceError(f"stage {stage} manifest is not an object")
        if manifest.get("schema_version") != 1 or manifest.get("kind") != "stage":
            raise EvidenceError(f"stage {stage} manifest type mismatch")
        if manifest.get("virtual_stage") != stage:
            raise EvidenceError(f"stage {stage} manifest number mismatch")
        hashes = manifest.get("hashes")
        if not isinstance(hashes, dict) or not hashes:
            raise EvidenceError(f"stage {stage} manifest has no hashes")
        missing = [name for name in REQUIRED_FILES if name not in hashes]
        if missing:
            raise EvidenceError(f"stage {stage} manifest omits required files: {missing}")
        on_disk = {
            str(path.relative_to(stage_dir))
            for path in stage_dir.rglob("*")
            if path.is_file() and not path.is_symlink() and path.name != "manifest.json"
        }
        declared = set(hashes)
        if on_disk != declared:
            raise EvidenceError(
                f"stage {stage} manifest/disk mismatch: "
                f"undeclared={sorted(on_disk - declared)[:5]} "
                f"missing={sorted(declared - on_disk)[:5]}"
            )
        for relative, expected in hashes.items():
            if not isinstance(expected, str):
                raise EvidenceError(f"stage {stage} has a non-string hash for {relative}")
            target = stage_dir / relative
            if target.is_symlink() or not target.is_file():
                raise EvidenceError(f"stage {stage} hash target is unsafe: {relative}")
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != expected:
                raise EvidenceError(f"stage {stage} hash mismatch: {relative}")
        snapshot = self._read_json(stage_dir / "snapshot.json")
        trace = self._read_json(stage_dir / "trace.json")
        trajectory = self._read_json(stage_dir / "trajectory.json")
        if not isinstance(snapshot, dict) or snapshot.get("stage") != stage:
            raise EvidenceError(f"stage {stage} snapshot number mismatch")
        if "error" in snapshot and not any(key != "error" for key in snapshot):
            raise EvidenceError(f"stage {stage} snapshot captured an error")
        if not isinstance(trace, list):
            raise EvidenceError(f"stage {stage} trace is not a list")
        if not isinstance(trajectory, dict):
            raise EvidenceError(f"stage {stage} trajectory is not an object")
        self._validated.add(stage)
        return stage_dir

    def _load(self, stage: int, filename: str) -> Any:
        key = (int(stage), filename)
        if key not in self._cache:
            stage_dir = self.validate_stage(stage)
            path = stage_dir / filename
            if filename.endswith(".txt"):
                try:
                    value = path.read_text(encoding="utf-8")
                except OSError as exc:
                    raise EvidenceError(f"unreadable evidence file {path}: {exc}") from exc
            else:
                value = self._read_json(path)
            self._cache[key] = value
        return self._cache[key]

    def snapshot(self, stage: int) -> dict[str, Any]:
        value = self._load(stage, "snapshot.json")
        if not isinstance(value, dict):
            raise EvidenceError(f"stage {stage} snapshot is not an object")
        return value

    def trace(self, stage: int) -> list[dict[str, Any]]:
        value = self._load(stage, "trace.json")
        if not isinstance(value, list):
            raise EvidenceError(f"stage {stage} trace is not a list")
        return value

    def response(self, stage: int) -> str:
        value = self._load(stage, "response.txt")
        return value if isinstance(value, str) else str(value)

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
