"""Validated access to immutable Harbor stage evidence.

The scoring process can read only the files frozen by world-controller.  This
module deliberately has no network client, service capability, or workspace
handle, so a historical check cannot observe the live final world.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REQUIRED_FILES = frozenset(
    {"snapshot.json", "trace.json", "response.txt", "trajectory.json"}
)


class EvidenceError(RuntimeError):
    """Frozen evidence is absent, malformed, or no longer matches its manifest."""


class HarborEvidence:
    """Cached reader over ``<root>/stages/stage-NN``.

    ``stage_limit`` gives stage rubrics a historical view during a final full
    recomputation.  It affects discovery only; explicit access still validates
    the requested stage normally.
    """

    def __init__(
        self,
        root: Path | str = DEFAULT_EVIDENCE_ROOT,
        *,
        stage_limit: int | None = None,
    ) -> None:
        self.root = Path(root)
        self.stage_limit = stage_limit
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
        """Validate the stage manifest, exact file set, and every declared hash."""
        stage_dir = self._stage_dir(stage)
        if stage in self._validated:
            return stage_dir
        if not stage_dir.is_dir() or stage_dir.is_symlink():
            raise EvidenceError(f"no frozen evidence for stage {stage} at {stage_dir}")

        manifest_path = stage_dir / "manifest.json"
        if not manifest_path.is_file() or manifest_path.is_symlink():
            raise EvidenceError(f"stage {stage} has no regular manifest at {manifest_path}")
        manifest = self._read_json(manifest_path)
        if not isinstance(manifest, dict):
            raise EvidenceError(f"stage {stage} manifest is not an object")
        if manifest.get("schema_version") != 1:
            raise EvidenceError(
                f"stage {stage} manifest schema_version="
                f"{manifest.get('schema_version')!r}, expected 1"
            )
        if manifest.get("kind") != "stage":
            raise EvidenceError(
                f"stage {stage} manifest kind={manifest.get('kind')!r}, expected 'stage'"
            )
        if manifest.get("virtual_stage") != stage:
            raise EvidenceError(
                f"stage {stage} manifest declares virtual_stage="
                f"{manifest.get('virtual_stage')!r}"
            )

        hashes = manifest.get("hashes")
        if not isinstance(hashes, dict) or not hashes:
            raise EvidenceError(f"stage {stage} manifest carries no file hashes")
        if any(not isinstance(name, str) or not isinstance(value, str) for name, value in hashes.items()):
            raise EvidenceError(f"stage {stage} manifest contains invalid hash entries")
        missing = REQUIRED_FILES - set(hashes)
        if missing:
            raise EvidenceError(
                f"stage {stage} manifest omits required files: {sorted(missing)}"
            )

        on_disk: dict[str, Path] = {}
        try:
            candidates = list(stage_dir.rglob("*"))
        except OSError as exc:
            raise EvidenceError(f"cannot enumerate stage {stage}: {exc}") from exc
        for path in candidates:
            if path.is_symlink():
                raise EvidenceError(f"stage {stage} contains a symlink: {path}")
            if path.is_file() and path.name != "manifest.json":
                on_disk[str(path.relative_to(stage_dir))] = path
        if set(on_disk) != set(hashes):
            raise EvidenceError(
                f"stage {stage} manifest/disk mismatch: "
                f"undeclared={sorted(set(on_disk) - set(hashes))[:5]} "
                f"missing={sorted(set(hashes) - set(on_disk))[:5]}"
            )

        for name, path in on_disk.items():
            try:
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError as exc:
                raise EvidenceError(f"unreadable evidence file {path}: {exc}") from exc
            if actual != hashes[name]:
                raise EvidenceError(
                    f"stage {stage} file {name} hash mismatch: evidence was modified"
                )

        self._validated.add(stage)
        return stage_dir

    def _load(self, stage: int, filename: str) -> Any:
        key = (stage, filename)
        if key in self._cache:
            return self._cache[key]
        path = self.validate_stage(stage) / filename
        if filename.endswith(".txt"):
            try:
                value = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
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
            raise EvidenceError(
                f"stage {stage} snapshot declares stage={value.get('stage')!r}"
            )
        if "error" in value and not any(key for key in value if key not in {"stage", "error"}):
            raise EvidenceError(
                f"stage {stage} snapshot is a captured error: {value['error']!r}"
            )
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
        if not stages_root.is_dir() or stages_root.is_symlink():
            return []
        found: list[int] = []
        for path in sorted(stages_root.glob("stage-*")):
            if not path.is_dir() or path.is_symlink():
                continue
            try:
                stage = int(path.name.removeprefix("stage-"))
            except ValueError:
                continue
            if self.stage_limit is None or stage <= self.stage_limit:
                found.append(stage)
        return found


def snapshot(env: HarborEvidence, stage: int) -> dict[str, Any]:
    return env.snapshot(stage)


def trace(env: HarborEvidence, stage: int) -> list[dict[str, Any]]:
    return env.trace(stage)


def response(env: HarborEvidence, stage: int) -> str:
    return env.response(stage)
