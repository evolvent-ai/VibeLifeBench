"""Strict read-only access to immutable Harbor stage evidence."""
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
    """Frozen evidence is absent, malformed, or no longer matches its manifest."""


class HarborEvidence:
    """Validated reader over ``<root>/stages/stage-NN``."""

    def __init__(self, root: Path | str = DEFAULT_EVIDENCE_ROOT) -> None:
        self.root = Path(root)
        self.scoring_stage: int | None = None
        self._validated: set[int] = set()
        self._cache: dict[tuple[int, str], Any] = {}

    def _stage_dir(self, stage: int) -> Path:
        if isinstance(stage, bool) or not isinstance(stage, int) or stage < 0:
            raise EvidenceError(f"invalid stage number: {stage!r}")
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
            str(path.relative_to(stage_dir)): path
            for path in stage_dir.rglob("*")
            if path.is_file() and not path.is_symlink() and path.name != "manifest.json"
        }
        if set(on_disk) != set(hashes):
            raise EvidenceError(f"stage {stage} manifest file set mismatch")
        for name, path in on_disk.items():
            expected = hashes[name]
            if not isinstance(expected, str):
                raise EvidenceError(f"stage {stage} hash for {name} is not text")
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != expected:
                raise EvidenceError(f"stage {stage} hash mismatch: {name}")
        self._validated.add(stage)
        return stage_dir

    def _load(self, stage: int, filename: str) -> Any:
        key = (stage, filename)
        if key not in self._cache:
            path = self.validate_stage(stage) / filename
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
        if value.get("stage") != stage:
            raise EvidenceError(f"stage {stage} snapshot number mismatch")
        if value.get("error") and set(value) <= {"stage", "error"}:
            raise EvidenceError(f"stage {stage} snapshot captured an error: {value['error']}")
        return value

    def trace(self, stage: int) -> list[dict[str, Any]]:
        value = self._load(stage, "trace.json")
        if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
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
        stages_root = self.root / "stages"
        if not stages_root.is_dir():
            return []
        found: list[int] = []
        for path in stages_root.glob("stage-*"):
            if not path.is_dir():
                continue
            try:
                found.append(int(path.name.removeprefix("stage-")))
            except ValueError:
                continue
        return sorted(found)


def snapshot(env: HarborEvidence, stage: int) -> dict[str, Any]:
    return env.snapshot(stage)


def trace(env: HarborEvidence, stage: int) -> list[dict[str, Any]]:
    return env.trace(stage)


def response(env: HarborEvidence, stage: int) -> str:
    return env.response(stage)
