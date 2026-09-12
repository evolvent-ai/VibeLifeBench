"""Serve one frozen stage snapshot through the MCP vocabulary the rubrics speak.

The rubrics address the world as ``env.<server>_mock.call_tool(tool, **kwargs)``
and ``env.workspace.fs``. That vocabulary is correct and stays; what was missing
was an implementation backed by frozen evidence rather than by a live service.

This module is that implementation. It answers every call from
``<evidence_root>/stages/stage-NN/snapshot.json`` — the same bytes the
world-controller froze and hashed at the stage boundary — so scoring a historical
stage observes that stage's world and nothing later.

**Why an index and not a passthrough.** ``snapshot.json`` is organised by
business area (``banking``/``email``/...), while the rubrics ask by tool name.
:class:`SnapshotEnv` owns that translation in one place. A tool the capture layer
never recorded raises :class:`~harbor_evidence.EvidenceError` instead of
returning ``None``: a helper that reads ``None`` degrades to an empty list and
the check scores zero, which is indistinguishable from an agent that did nothing.
Measured on this task before the rewire: every one of the 38 checks read empty
and the whole 100.0-weight pool was unearnable, with no error raised anywhere.
Missing capture is infrastructure failure and must be loud.

**No live door.** There is no MCP client and no live filesystem here, exactly as
in :mod:`harbor_evidence`. ``environment/evidence-collector/harbor_env.py`` is
the capture-side counterpart and must never be imported from ``tests/``.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from harbor_evidence import DEFAULT_EVIDENCE_ROOT, EvidenceError, HarborEvidence


class _Capability:
    """One server's read surface, answered from the frozen snapshot."""

    def __init__(self, env: "SnapshotEnv", server: str) -> None:
        self._env = env
        self.server = server

    def call_tool(self, name: str, **kwargs: Any) -> Any:
        return self._env.dispatch(self.server, name, kwargs)


class _Fs:
    """Read-only view of the workspace as frozen for this stage.

    Keys in the captured map are Harbor-native absolute paths (``/workspace/x.md``).
    """

    def __init__(self, files: dict[str, str]) -> None:
        self._files = files

    def exists(self, path: str) -> bool:
        return str(path) in self._files

    def read_file(self, path: str) -> bytes:
        key = str(path)
        if key not in self._files:
            raise FileNotFoundError(path)
        return self._files[key].encode("utf-8")

    def list_dir(self, path: str) -> list[str]:
        prefix = str(path).rstrip("/") + "/"
        names = {
            key[len(prefix):].split("/", 1)[0]
            for key in self._files
            if key.startswith(prefix)
        }
        return sorted(names)

    def write_file(self, path: str, data: bytes) -> None:
        raise PermissionError("frozen evidence is read-only")


class _Workspace:
    def __init__(self, files: dict[str, str]) -> None:
        self.fs = _Fs(files)


class SnapshotEnv:
    """``env`` for one frozen stage: MCP-shaped reads plus a workspace view.

    ``stage`` is the virtual stage whose snapshot answers capability calls. The
    per-stage response and trace are addressed separately by stage index, so a
    task-level rubric can bind to the last published stage for backend reads
    while still inspecting any earlier stage's trace.
    """

    SERVERS = ("banking", "brokerage", "calendar", "email", "job_board", "legal_search", "notion")

    def __init__(self, stage: int, evidence: HarborEvidence | None = None,
                 root: Path | str = DEFAULT_EVIDENCE_ROOT) -> None:
        self.stage = int(stage)
        self.evidence = evidence if evidence is not None else HarborEvidence(root)
        self._snapshot = self.evidence.snapshot(self.stage)
        self.workspace = _Workspace(self._workspace_files())
        for server in self.SERVERS:
            setattr(self, f"{server}_mock", _Capability(self, server))

    # -- workspace ---------------------------------------------------------
    def _workspace_files(self) -> dict[str, str]:
        raw = self._snapshot.get("workspace")
        if not isinstance(raw, dict):
            return {}
        return {str(k): str(v) for k, v in raw.items() if isinstance(v, str)}

    # -- per-stage agent artefacts ----------------------------------------
    def response(self, stage: int) -> str:
        return self.evidence.response(stage)

    def trace(self, stage: int) -> list[dict[str, Any]]:
        return self.evidence.trace(stage)

    # -- snapshot shape ----------------------------------------------------
    def _table(self, payload: Any, where: str) -> dict:
        """Index one level of the snapshot, refusing to invent an empty table.

        Every level this navigates is written by the capture layer as an object.
        Anything else means what is filed there is not a value — most often the
        *text* of a failed tool call, because MCP reports a tool-level failure by
        returning ``CallToolResult(isError=True)`` rather than by raising, and a
        decoder that ignores that flag yields the message as a bare ``str``.

        This used to coerce such a payload to ``{}``, which was the last step of
        the silent-zero chain: an unreadable server became an empty one, every
        check reading it scored 0, and the run reported ``status: ok``. Measured
        then, with one server failing at capture: reward 0.3950, ``verifier_ok``
        1.0 — a dead backend billed to the agent.
        """
        if isinstance(payload, dict):
            return payload
        raise EvidenceError(
            f"stage {self.stage}: {where} is {type(payload).__name__}, expected an object — "
            f"the capture recorded something that is not a value, so it cannot be scored"
        )

    # -- capability dispatch ----------------------------------------------
    def dispatch(self, server: str, tool: str, kwargs: dict[str, Any]) -> Any:
        section = self._snapshot.get(server)
        if section is None:
            raise EvidenceError(
                f"stage {self.stage} snapshot has no '{server}' section: "
                f"the capture layer never recorded it, so {server}.{tool} is unscoreable"
            )
        handler = getattr(self, f"_{server}", None)
        if handler is None:
            raise EvidenceError(f"no dispatch for server {server!r}")
        payload = handler(self._table(section, server), tool, kwargs)
        # Three outcomes, matching the capture side's split. ``None`` is an
        # answer — the snapshot holds no row under that id, which is what an
        # unwritten record looks like and what the helpers correctly read as
        # empty. A container is data. A scalar is neither: no healthy capture
        # files a string where an MCP envelope belongs, so returning one would
        # hand the helpers something they degrade to empty without ever knowing
        # the read had failed.
        if payload is not None and not isinstance(payload, (dict, list)):
            raise EvidenceError(
                f"stage {self.stage}: {server}.{tool} is recorded as "
                f"{type(payload).__name__}, expected an MCP envelope — "
                f"{payload!r:.120}"
            )
        return payload

    # -- per-server dispatch ----------------------------------------------
    def _banking(self, section: dict, tool: str, kw: dict) -> Any:
        if tool == "list_transactions":
            account_id = str(kw.get("account_id") or "")
            book = self._table(section.get("transactions"), "banking.transactions")
            if account_id in book:
                return book[account_id]
            raise EvidenceError(
                f"stage {self.stage}: no captured transactions for account {account_id!r}"
            )
        if tool == "get_account":
            account_id = str(kw.get("account_id") or "")
            book = self._table(section.get("accounts"), "banking.accounts")
            return book.get(account_id)
        raise EvidenceError(f"stage {self.stage}: banking.{tool} was never captured")

    def _brokerage(self, section: dict, tool: str, kw: dict) -> Any:
        if tool == "get_positions":
            account_id = str(kw.get("account_id") or "")
            book = self._table(section.get("positions"), "brokerage.positions")
            if account_id in book:
                return book[account_id]
            raise EvidenceError(
                f"stage {self.stage}: no captured positions for account {account_id!r}"
            )
        if tool == "get_quote":
            symbol = str(kw.get("symbol") or "")
            book = self._table(section.get("quotes"), "brokerage.quotes")
            return book.get(symbol)
        raise EvidenceError(f"stage {self.stage}: brokerage.{tool} was never captured")

    def _calendar(self, section: dict, tool: str, kw: dict) -> Any:
        if tool == "list_calendars":
            return section.get("calendars")
        if tool == "list_events":
            calendar_id = str(kw.get("calendar_id") or "")
            book = self._table(section.get("events_by_calendar"), "calendar.events_by_calendar")
            if calendar_id in book:
                return book[calendar_id]
            # A calendar the agent created and the capture did not track is a
            # capture gap, not an empty calendar.
            raise EvidenceError(
                f"stage {self.stage}: no captured events for calendar {calendar_id!r}"
            )
        if tool == "get_event":
            event_id = str(kw.get("event_id") or "")
            return self._table(section.get("event_details"), "calendar.event_details").get(event_id)
        raise EvidenceError(f"stage {self.stage}: calendar.{tool} was never captured")

    def _email(self, section: dict, tool: str, kw: dict) -> Any:
        if tool == "get_emails":
            folder = str(kw.get("folder") or "INBOX")
            book = self._table(section.get("folders"), "email.folders")
            if folder in book:
                return self._table(book[folder], f"email.folders[{folder}]").get("listing")
            raise EvidenceError(f"stage {self.stage}: email folder {folder!r} was never captured")
        if tool == "get_drafts":
            return section.get("drafts")
        if tool in ("read_email", "get_email_headers"):
            email_id = str(kw.get("email_id") or "")
            detail = self._table(section.get("details"), "email.details").get(email_id)
            # Both tools are served from the merged per-message record: the
            # capture layer already joins read_email with get_email_headers,
            # because the mock's read_email projection omits the threading
            # headers that sent-reply matching depends on.
            return detail
        raise EvidenceError(f"stage {self.stage}: email.{tool} was never captured")

    def _job_board(self, section: dict, tool: str, kw: dict) -> Any:
        if tool == "list_applications":
            book = self._table(section.get("applications_by_user"), "job_board.applications_by_user")
            user_id = str(kw.get("user_id") or "")
            # Alternate spellings of the same person are probed by the helpers;
            # an unknown user is legitimately empty, not a capture gap.
            return book.get(user_id, {"applications": []})
        if tool == "get_job":
            job_id = str(kw.get("job_id") or "")
            return self._table(section.get("jobs"), "job_board.jobs").get(job_id)
        if tool == "search_jobs":
            return section.get("search")
        raise EvidenceError(f"stage {self.stage}: job_board.{tool} was never captured")

    def _legal_search(self, section: dict, tool: str, kw: dict) -> Any:
        if tool == "get_case":
            book = self._table(section.get("cases"), "legal_search.cases")
            return book.get(str(kw.get("case_id") or ""))
        if tool == "get_article":
            book = self._table(section.get("articles"), "legal_search.articles")
            return book.get(str(kw.get("article_id") or ""))
        if tool == "get_statute":
            book = self._table(section.get("statutes"), "legal_search.statutes")
            return book.get(str(kw.get("statute_id") or ""))
        if tool == "list_saved":
            book = self._table(section.get("saved_by_user"), "legal_search.saved_by_user")
            return book.get(str(kw.get("user_id") or ""), {"saved": []})
        if tool == "search_cases":
            return section.get("search")
        if tool == "search_statutes":
            return section.get("statute_search")
        raise EvidenceError(f"stage {self.stage}: legal_search.{tool} was never captured")

    def _notion(self, section: dict, tool: str, kw: dict) -> Any:
        if tool == "API-post-search":
            # The capture records one unfiltered page search; the helpers call it
            # once per query term and union the results, so returning the same
            # full page set for every query preserves that union exactly.
            return section.get("pages")
        if tool == "API-get-block-children":
            block_id = str(kw.get("block_id") or "")
            blocks = self._table(section.get("page_blocks"), "notion.page_blocks")
            if block_id in blocks:
                return blocks[block_id]
            children = self._table(section.get("row_children"), "notion.row_children")
            return children.get(block_id, {"results": []})
        if tool == "API-post-database-query":
            book = self._table(section.get("database_rows"), "notion.database_rows")
            return book.get(str(kw.get("database_id") or ""))
        raise EvidenceError(f"stage {self.stage}: notion.{tool} was never captured")


def load_json(path: Path | str) -> Any:
    """Read a JSON document, raising EvidenceError on damage (test helper)."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise EvidenceError(f"unreadable {path}: {exc}") from exc
