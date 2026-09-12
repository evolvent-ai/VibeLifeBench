"""Apply the controller's SQLite transaction contract to vendored mocks."""
from __future__ import annotations

import importlib
from typing import Any, Callable


_BACKENDS = (
    "calendar_mock.backends",
    "job_board_mock.backends",
    "emails_mcp.backends",
    "notification_hub_mock.backends",
    "notion_mock.backends",
)


def _delete_journal_mode(original: Callable[..., Any]) -> Callable[..., Any]:
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        connection = original(*args, **kwargs)
        connection.execute("PRAGMA journal_mode = DELETE;")
        return connection

    return wrapped


for _package_name in _BACKENDS:
    try:
        _package = importlib.import_module(_package_name)
        _module = importlib.import_module(f"{_package_name}.db")
    except ModuleNotFoundError:
        continue
    _wrapped = _delete_journal_mode(_module.get_conn)
    _module.get_conn = _wrapped
    _package.get_conn = _wrapped
