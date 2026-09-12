"""Validated access to Harbor's immutable stage evidence."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REQUIRED_FILES = ("snapshot.json", "trace.json", "response.txt", "trajectory.json")


class EvidenceError(RuntimeError):
    """Frozen evidence is missing, malformed, or has been modified."""


class HarborEvidence:
    """Read and validate one or more immutable virtual-stage directories."""

    def __init__(self, root: Path | str = DEFAULT_EVIDENCE_ROOT) -> None:
        self.root = Path(root)
        self._validated: set[int] = set()
        self._cache: dict[tuple[int, str], Any] = {}
        self.current_stage: int | None = None

    def set_stage(self, stage: int) -> None:
        self.current_stage = int(stage)

    def _stage_dir(self, stage: int) -> Path:
        return self.root / "stages" / f"stage-{int(stage):02d}"

    def _read_json(self, path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise EvidenceError(f"unreadable evidence file {path}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise EvidenceError(f"malformed JSON in {path}: {exc}") from exc

    def validate_stage(self, stage: int) -> Path:
        stage = int(stage)
        if stage in self._validated:
            return self._stage_dir(stage)
        stage_dir = self._stage_dir(stage)
        if not stage_dir.is_dir():
            raise EvidenceError(f"no frozen evidence for stage {stage}: {stage_dir}")
        manifest_path = stage_dir / "manifest.json"
        if not manifest_path.is_file():
            raise EvidenceError(f"stage {stage} has no manifest")
        manifest = self._read_json(manifest_path)
        if not isinstance(manifest, dict):
            raise EvidenceError(f"stage {stage} manifest is not an object")
        if manifest.get("schema_version") != 1 or manifest.get("kind") != "stage":
            raise EvidenceError(f"stage {stage} manifest type mismatch")
        if int(manifest.get("virtual_stage", -1)) != stage:
            raise EvidenceError(f"stage {stage} manifest number mismatch")
        hashes = manifest.get("hashes")
        if not isinstance(hashes, dict) or not hashes:
            raise EvidenceError(f"stage {stage} manifest has no hashes")
        missing = [name for name in REQUIRED_FILES if name not in hashes]
        if missing:
            raise EvidenceError(f"stage {stage} manifest omits required files: {missing}")
        actual = {
            str(path.relative_to(stage_dir))
            for path in stage_dir.rglob("*")
            if path.is_file() and not path.is_symlink() and path.name != "manifest.json"
        }
        declared = set(hashes)
        if actual != declared:
            raise EvidenceError(
                f"stage {stage} manifest/disk mismatch: "
                f"undeclared={sorted(actual - declared)[:5]} missing={sorted(declared - actual)[:5]}"
            )
        for relative, expected in hashes.items():
            target = stage_dir / relative
            if not isinstance(expected, str) or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                raise EvidenceError(f"stage {stage} hash mismatch: {relative}")
        self._validated.add(stage)
        return stage_dir

    def _load(self, stage: int, filename: str) -> Any:
        key = (int(stage), filename)
        if key in self._cache:
            return self._cache[key]
        stage_dir = self.validate_stage(stage)
        path = stage_dir / filename
        if not path.is_file() or path.is_symlink():
            raise EvidenceError(f"stage {stage} missing {filename}")
        try:
            value = path.read_text(encoding="utf-8") if filename.endswith(".txt") else self._read_json(path)
        except OSError as exc:
            raise EvidenceError(f"unreadable evidence file {path}: {exc}") from exc
        self._cache[key] = value
        return value

    def _context_stage(self) -> int:
        if self.current_stage is not None:
            return self.current_stage
        stages = self.published_stages()
        if stages:
            return stages[-1]
        raise EvidenceError("no current or published stage selected")

    def snapshot(self, stage: int) -> dict[str, Any]:
        value = self._load(stage, "snapshot.json")
        if not isinstance(value, dict):
            raise EvidenceError(f"stage {stage} snapshot is not an object")
        if "error" in value and not any(key for key in value if key != "error"):
            raise EvidenceError(f"stage {stage} snapshot is a captured error: {value['error']!r}")
        return value

    def trace(self, stage: int) -> list[dict[str, Any]]:
        value = self._load(stage, "trace.json")
        if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
            raise EvidenceError(f"stage {stage} trace is not a list of objects")
        return value

    def response(self, stage: int) -> str:
        value = self._load(stage, "response.txt")
        return value if isinstance(value, str) else str(value)

    def trajectory(self, stage: int) -> dict[str, Any]:
        value = self._load(stage, "trajectory.json")
        if not isinstance(value, dict):
            raise EvidenceError(f"stage {stage} trajectory is not an object")
        return value

    def workspace_file(self, basename: str, stage: int | None = None) -> str:
        stage = self._context_stage() if stage is None else int(stage)
        stage_dir = self.validate_stage(stage)
        name = Path(str(basename)).name
        path = stage_dir / "workspace" / name
        if not path.exists():
            return ""
        if not path.is_file() or path.is_symlink():
            raise EvidenceError(f"invalid workspace evidence path: {path}")
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            raise EvidenceError(f"unreadable workspace evidence {path}: {exc}") from exc

    def published_stages(self) -> list[int]:
        stages_root = self.root / "stages"
        if not stages_root.is_dir():
            return []
        result = []
        for path in sorted(stages_root.glob("stage-*")):
            try:
                result.append(int(path.name.removeprefix("stage-")))
            except ValueError:
                continue
        return result
