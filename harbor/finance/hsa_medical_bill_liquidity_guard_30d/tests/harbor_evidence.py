"""Harbor-native access to one stage's immutable frozen evidence.

Replaces the former source-path compatibility adapter. The rubrics used to address
three virtual evidence trees through a duck-typed filesystem handle; they now go
through this context, which speaks only Harbor's own vocabulary:

    <evidence_root>/stages/stage-NN/{manifest,snapshot,trace,response,trajectory}

Two properties matter more than convenience:

**Nothing here can reach the live world.** The old adapter also carried per-service
capability objects wired to the running MCP endpoints. No rubric used them, but a
future one could have, and scoring a *historical* stage against the *final* world
silently rewards last-turn back-fill while punishing an agent that correctly
superseded stale values. There is no MCP client in this module — the door is
closed rather than merely unused.

**Damaged evidence raises instead of defaulting.** The previous readers swallowed
every exception and returned ``{}`` / ``[]`` / ``""``. An empty snapshot and a
snapshot that failed to load are indistinguishable to a rubric, so a broken
sidecar read exactly like an agent that did nothing: measured, an empty evidence
tree produced ``reward 0.0`` with 23 swallowed errors and exit 0. Every accessor
here validates first and raises :class:`EvidenceError`; the verifier turns that
into an infrastructure failure rather than a zero score.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))

# Files the world-controller freezes for every published stage.
REQUIRED_FILES = ("snapshot.json", "trace.json", "response.txt", "trajectory.json")


class EvidenceError(RuntimeError):
    """Frozen evidence is missing, unreadable, or fails its own manifest."""


class HarborEvidence:
    """Validated, cached reader over ``<root>/stages/stage-NN``."""

    def __init__(self, root: Path | str = DEFAULT_EVIDENCE_ROOT) -> None:
        self.root = Path(root)
        self._validated: set[int] = set()
        self._cache: dict[tuple[int, str], Any] = {}
        self._active_stage = 23
        self.workspace = _FrozenWorkspace(self)

    def set_active_stage(self, stage: int) -> None:
        self._active_stage = int(stage)

    def _workspace_files(self, stage: int | None = None) -> dict[str, str]:
        data = self.snapshot(self._active_stage if stage is None else int(stage)).get("workspace", {})
        if not isinstance(data, dict):
            return {}
        candidates = data.get("files") if isinstance(data.get("files"), dict) else data
        out: dict[str, str] = {}
        for key, value in candidates.items():
            if isinstance(value, (str, bytes)):
                out[str(key)] = value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value
        return out

    # -- internals ---------------------------------------------------------
    def _stage_dir(self, stage: int) -> Path:
        return self.root / "stages" / f"stage-{stage:02d}"

    def _read_json(self, path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise EvidenceError(f"unreadable evidence file {path}: {exc}") from exc
        except ValueError as exc:
            raise EvidenceError(f"malformed JSON in {path}: {exc}") from exc

    def validate_stage(self, stage: int) -> Path:
        """Verify the manifest, the file set and every hash. Cached per stage."""
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
        if manifest.get("schema_version") != 1:
            raise EvidenceError(
                f"stage {stage} manifest schema_version={manifest.get('schema_version')!r}, expected 1"
            )
        if manifest.get("kind") != "stage":
            raise EvidenceError(
                f"stage {stage} manifest kind={manifest.get('kind')!r}, expected 'stage' "
                "(an event-level manifest means the stage was never published)"
            )
        if int(manifest.get("virtual_stage", -1)) != stage:
            raise EvidenceError(
                f"stage {stage} manifest declares virtual_stage={manifest.get('virtual_stage')!r}"
            )

        hashes = manifest.get("hashes")
        if not isinstance(hashes, dict) or not hashes:
            raise EvidenceError(f"stage {stage} manifest carries no file hashes")

        missing = [name for name in REQUIRED_FILES if name not in hashes]
        if missing:
            raise EvidenceError(f"stage {stage} manifest omits required file(s): {missing}")

        # The manifest must describe exactly what is on disk. A file present but
        # undeclared means the freeze proved nothing about it; a file declared
        # but absent means the freeze was truncated.
        on_disk = {
            str(p.relative_to(stage_dir))
            for p in stage_dir.rglob("*")
            if p.is_file() and p.name != "manifest.json"
        }
        declared = set(hashes)
        if on_disk != declared:
            raise EvidenceError(
                f"stage {stage} manifest/disk mismatch: "
                f"undeclared={sorted(on_disk - declared)[:5]} missing={sorted(declared - on_disk)[:5]}"
            )

        for name, expected in hashes.items():
            target = stage_dir / name
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != expected:
                raise EvidenceError(
                    f"stage {stage} file {name} hash mismatch: frozen evidence was modified"
                )

        self._validated.add(stage)
        return stage_dir

    def _load(self, stage: int, filename: str) -> Any:
        key = (stage, filename)
        if key in self._cache:
            return self._cache[key]
        stage_dir = self.validate_stage(stage)
        path = stage_dir / filename
        value = path.read_text(encoding="utf-8") if filename.endswith(".txt") else self._read_json(path)
        self._cache[key] = value
        return value

    # -- public surface ----------------------------------------------------
    def snapshot(self, stage: int) -> dict[str, Any]:
        value = self._load(stage, "snapshot.json")
        if not isinstance(value, dict):
            raise EvidenceError(f"stage {stage} snapshot is {type(value).__name__}, expected object")
        # The collector records capture failures in-band. Without this check a
        # failed capture reads as "the world was empty" and scores like an idle
        # agent instead of failing the run.
        substantive = {key for key in value if key not in {"error", "stage", "scenario_clock"}}
        if "error" in value and not substantive:
            raise EvidenceError(f"stage {stage} snapshot is a captured error: {value['error']!r}")
        return value

    def trace(self, stage: int) -> list[dict[str, Any]]:
        value = self._load(stage, "trace.json")
        if not isinstance(value, list):
            raise EvidenceError(f"stage {stage} trace is {type(value).__name__}, expected list")
        return value

    def response(self, stage: int) -> str:
        value = self._load(stage, "response.txt")
        return value if isinstance(value, str) else str(value)

    def trajectory(self, stage: int) -> dict[str, Any]:
        value = self._load(stage, "trajectory.json")
        if not isinstance(value, dict):
            raise EvidenceError(f"stage {stage} trajectory is {type(value).__name__}, expected object")
        return value

    def published_stages(self) -> list[int]:
        stages_root = self.root / "stages"
        if not stages_root.is_dir():
            return []
        found = []
        for path in sorted(stages_root.glob("stage-*")):
            try:
                found.append(int(path.name.removeprefix("stage-")))
            except ValueError:
                continue
        return found


class _FrozenFS:
    """Read-only workspace projection captured in the frozen stage snapshot."""

    def __init__(self, evidence: HarborEvidence) -> None:
        self.evidence = evidence

    @staticmethod
    def _key(path: str) -> str:
        raw = str(path).rstrip("/")
        if raw == "/workspace":
            return "/workspace"
        return raw if raw.startswith("/workspace/") else "/workspace/" + raw.lstrip("/")

    def _files(self) -> dict[str, str]:
        return self.evidence._workspace_files()

    def read_file(self, path: str) -> bytes:
        key = self._key(path)
        files = self._files()
        value = files.get(key, files.get(key.removeprefix("/workspace/")))
        if value is None:
            raise FileNotFoundError(path)
        return value.encode("utf-8")

    def exists(self, path: str) -> bool:
        key = self._key(path)
        files = self._files()
        return key in files or key.removeprefix("/workspace/") in files

    def list_dir(self, path: str) -> list[str]:
        prefix = self._key(path).rstrip("/") + "/"
        return sorted({key[len(prefix):].split("/", 1)[0] for key in self._files() if key.startswith(prefix)})


class _FrozenWorkspace:
    def __init__(self, evidence: HarborEvidence) -> None:
        self.fs = _FrozenFS(evidence)


def snapshot(env: HarborEvidence, stage: int) -> dict[str, Any]:
    return env.snapshot(stage)


def trace(env: HarborEvidence, stage: int) -> list[dict[str, Any]]:
    return env.trace(stage)


def response(env: HarborEvidence, stage: int) -> str:
    return env.response(stage)
