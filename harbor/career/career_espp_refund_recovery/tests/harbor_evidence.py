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
        self._active_stage = 0
        self.workspace = _FrozenWorkspace(self)

    def set_active_stage(self, stage: int) -> None:
        self._active_stage = int(stage)

    def _service(self, server: str) -> dict[str, Any]:
        value = self.snapshot(self._active_stage).get(server, {})
        return value if isinstance(value, dict) else {}

    @staticmethod
    def _rows(value: Any, *keys: str) -> list[dict[str, Any]]:
        if isinstance(value, list):
            return [row for row in value if isinstance(row, dict)]
        if isinstance(value, dict):
            for key in keys:
                candidate = value.get(key)
                if isinstance(candidate, list):
                    return [row for row in candidate if isinstance(row, dict)]
        return []

    @staticmethod
    def _row_id(row: dict[str, Any]) -> str:
        for key in ("id", "email_id", "message_id", "application_id", "tx_id", "event_id"):
            if row.get(key) is not None:
                return str(row[key])
        return ""

    def call_tool(self, server: str, tool: str, **kwargs: Any) -> Any:
        """Read a captured tool-shaped projection without a network client."""
        data = self._service(server)
        if server == "job_board":
            if tool == "list_applications":
                return data.get("applications", [])
            if tool == "get_application_status":
                details = data.get("application_details", {})
                return details.get(str(kwargs.get("application_id"))) if isinstance(details, dict) else None
            if tool == "list_resumes":
                return data.get("resumes", [])
            if tool == "list_saved_jobs":
                return data.get("saved_jobs", [])
            if tool == "list_chats":
                return data.get("chats", [])
            if tool == "get_job":
                jobs = data.get("jobs", {})
                return jobs.get(str(kwargs.get("job_id"))) if isinstance(jobs, dict) else None
            if tool == "search_jobs":
                return {"jobs": list(data.get("jobs", {}).values())} if isinstance(data.get("jobs"), dict) else data.get("jobs", [])
        elif server == "banking":
            if tool == "list_transactions":
                return data.get("transactions", data.get("transaction_list", []))
            if tool == "get_account":
                accounts = data.get("accounts", {})
                if isinstance(accounts, dict):
                    return accounts.get(str(kwargs.get("account_id")))
                return next((row for row in self._rows(accounts) if str(row.get("account_id")) == str(kwargs.get("account_id"))), None)
        elif server == "brokerage":
            if tool == "get_positions":
                return data.get("positions", [])
            if tool == "get_quote":
                quotes = data.get("quotes", {})
                if isinstance(quotes, dict):
                    return quotes.get(str(kwargs.get("symbol")))
                return next((row for row in self._rows(quotes) if str(row.get("symbol")) == str(kwargs.get("symbol"))), None)
        elif server == "calendar":
            if tool == "list_calendars":
                # The collector freezes the requested calendar's events rather
                # than a separate calendar listing. Reconstruct the small
                # listing needed by the rubric helpers from those event rows.
                ids = sorted({
                    str(row.get("calendar_id"))
                    for row in data.get("events", [])
                    if isinstance(row, dict) and row.get("calendar_id")
                })
                return [{"calendar_id": calendar_id} for calendar_id in ids]
            if tool == "list_events":
                return data.get("events", [])
            if tool == "get_event":
                event_id = str(kwargs.get("event_id") or "")
                return next(
                    (row for row in data.get("events", [])
                     if isinstance(row, dict) and str(row.get("event_id") or "") == event_id),
                    None,
                )
        elif server == "email":
            folder = str(kwargs.get("folder") or "")
            if tool == "get_emails":
                section = data.get("inbox" if folder.lower() == "inbox" else "sent", {})
                if isinstance(section, dict) and "listing" in section:
                    return section["listing"]
                return section
            if tool == "get_drafts":
                return data.get("drafts", [])
            if tool in {"read_email", "get_email_headers"}:
                needle = str(kwargs.get("email_id"))
                for section_name in ("inbox", "sent"):
                    section = data.get(section_name, {})
                    details = section.get("details", []) if isinstance(section, dict) else []
                    for row in details:
                        if isinstance(row, dict) and self._row_id(row) == needle:
                            return row
        elif server == "legal_search":
            if tool == "list_saved":
                return data.get("saved_cases", [])
            for collection, tool_name, key in (("cases", "get_case", "case_id"), ("statutes", "get_statute", "statute_id"), ("articles", "get_article", "article_id")):
                if tool == tool_name:
                    values = data.get(collection, {})
                    return values.get(str(kwargs.get(key))) if isinstance(values, dict) else None
        elif server == "notion":
            if tool == "API-post-search":
                return data.get("databases" if (kwargs.get("filter") or {}).get("value") == "database" else "pages", {})
            if tool == "API-get-block-children":
                block_id = str(kwargs.get("block_id"))
                return (data.get("page_blocks", {}) or {}).get(block_id) or (data.get("row_children", {}) or {}).get(block_id)
            if tool == "API-post-database-query":
                return (data.get("database_rows", {}) or {}).get(str(kwargs.get("database_id")))
        return None

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
        if "error" in value and not any(k for k in value if k != "error"):
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
    def __init__(self, evidence: HarborEvidence) -> None:
        self.evidence = evidence

    def _files(self) -> dict[str, str]:
        value = self.evidence._service("workspace").copy()
        return {str(k): str(v) for k, v in value.items()}

    @staticmethod
    def _key(path: str) -> str:
        raw = str(path).rstrip("/")
        if raw == "/workspace":
            return "/workspace"
        if raw.startswith("/workspace/"):
            return raw
        return "/workspace/" + raw.lstrip("/")

    def read_file(self, path: str) -> bytes:
        files = self._files()
        key = self._key(path)
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
        files = self._files()
        return sorted({key[len(prefix):].split("/", 1)[0] for key in files if key.startswith(prefix)})


class _FrozenWorkspace:
    def __init__(self, evidence: HarborEvidence) -> None:
        self.fs = _FrozenFS(evidence)


def snapshot(env: HarborEvidence, stage: int) -> dict[str, Any]:
    return env.snapshot(stage)


def trace(env: HarborEvidence, stage: int) -> list[dict[str, Any]]:
    return env.trace(stage)


def response(env: HarborEvidence, stage: int) -> str:
    return env.response(stage)
