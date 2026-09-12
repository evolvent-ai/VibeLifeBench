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
        self._active_stage = 20
        self.workspace = _FrozenWorkspace(self)
        self.fs = self.workspace.fs
        self.filesystem = self.fs
        self.container_workspace = "/workspace"
        self._services = {
            name: _FrozenService(self, name)
            for name in ("calendar", "email", "hotel_booking", "maps", "notion",
                         "visa_and_advisory", "weather")
        }

    def set_active_stage(self, stage: int) -> None:
        selected = int(stage)
        if selected < 0:
            raise ValueError(f"active stage must be non-negative, got {selected}")
        self._active_stage = selected

    def __getattr__(self, name: str) -> Any:
        if name in self._services:
            return self._services[name]
        if name == "emails":
            return self._services["email"]
        if name == "google_calendar":
            return self._services["calendar"]
        raise AttributeError(name)

    @property
    def snapshots(self) -> dict[str, dict[str, str]]:
        return {f"T{stage}": self._workspace_files(stage) for stage in self.published_stages()}

    @property
    def turn_log(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for stage in self.published_stages():
            if stage > self._active_stage:
                continue
            calls = []
            for call in self.trace(stage):
                if not isinstance(call, dict):
                    continue
                normalized = dict(call)
                args = normalized.get("input", normalized.get("arguments", {}))
                normalized["input"] = args if isinstance(args, dict) else {}
                normalized["arguments"] = normalized["input"]
                normalized["stage"] = stage
                success = normalized.get("succeeded", normalized.get("success"))
                if success is not None:
                    normalized["succeeded"] = bool(success)
                calls.append(normalized)
            rows.append({"stage": stage, "response": self.response(stage), "tool_calls": calls})
        return rows

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


class _FrozenService:
    """Read-only projection of one captured service namespace."""

    def __init__(self, evidence: HarborEvidence, service: str) -> None:
        self.evidence = evidence
        self.service = service

    async def call_tool(self, tool: str, **kwargs: Any) -> Any:
        snapshot = self.evidence.snapshot(self.evidence._active_stage)
        section = snapshot.get(self.service, {})
        if not isinstance(section, dict):
            return None
        if self.service == "email":
            folder = str(kwargs.get("folder") or "").lower()
            if tool == "get_emails":
                if folder in {"sent", "sent items", "inbox.sent"}:
                    return (section.get("sent") or {}).get("listing")
                return (section.get("inbox") or {}).get("listing")
            if tool in {"read_email", "get_email_headers"}:
                wanted = str(kwargs.get("email_id") or "")
                for box in (section.get("inbox"), section.get("sent")):
                    for row in (box or {}).get("details") or []:
                        if isinstance(row, dict) and str(row.get("email_id") or row.get("id")) == wanted:
                            return row
                return None
            return section.get(tool)
        if self.service == "calendar" and tool in {"list_events", "search_events"}:
            events = section.get("events")
            if tool == "search_events":
                query = str(kwargs.get("query") or "").lower()
                rows = events if isinstance(events, list) else (events or {}).get("events", [])
                return [row for row in rows if query in json.dumps(row, ensure_ascii=False).lower()]
            return events
        if self.service == "notion":
            aliases = {
                "query_database": "API-post-database-query",
                "get_page": "API-retrieve-a-page",
                "search": "API-post-search",
            }
            key = aliases.get(tool, tool)
            return section.get(key) or section.get(tool)
        if self.service == "visa_and_advisory":
            if tool == "list_visa_applications":
                apps = section.get("applications") or section.get("visa_applications") or section.get("list_visa_applications")
                return apps
            if tool == "get_visa_application":
                app_id = str(kwargs.get("application_id") or "")
                apps = section.get("application_details") or section.get("applications") or {}
                if isinstance(apps, dict):
                    return apps.get(app_id)
                return next((row for row in apps if isinstance(row, dict) and str(row.get("application_id")) == app_id), None)
        if self.service == "hotel_booking":
            if tool == "list_reservations":
                return section.get("reservations") or section.get(tool)
            if tool == "get_reservation":
                reservation_id = str(kwargs.get("reservation_id") or "")
                details = section.get("reservation_details") or {}
                if isinstance(details, dict):
                    return details.get(reservation_id)
                return None
        return section.get(tool)


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

    async def read_file(self, path: str) -> str:
        key = self._key(path)
        files = self._files()
        value = files.get(key, files.get(key.removeprefix("/workspace/")))
        if value is None:
            raise FileNotFoundError(path)
        return value

    async def exists(self, path: str) -> bool:
        key = self._key(path)
        files = self._files()
        return key in files or key.removeprefix("/workspace/") in files

    async def list_dir(self, path: str) -> list[str]:
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
