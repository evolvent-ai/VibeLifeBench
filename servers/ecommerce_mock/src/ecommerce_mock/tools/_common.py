"""Tool-layer helpers: JSON serialization and error envelope wrapping.

Mirrors hotel_booking_mock/tools/_common.py — kept tiny so business
logic stays in services/.
"""
import functools
import json
import logging
from typing import Any

from ..utils.exceptions import EcommerceMockError

logger = logging.getLogger(__name__)


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def error_response(message: str, code: str) -> str:
    return dumps({"error": message, "code": code})


def handle_errors(fn):
    """Decorator that maps EcommerceMockError to structured responses.

    Uses functools.wraps so FastMCP can introspect the wrapped function's
    real signature (otherwise it generates a schema from `*args/**kwargs`).
    """
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except EcommerceMockError as exc:
            logger.info("tool error [%s]: %s", exc.code, exc.message)
            return error_response(exc.message, exc.code)
        except Exception as exc:  # noqa: BLE001
            logger.exception("unexpected tool error")
            return error_response(f"internal error: {exc}", "BAD_ARG")

    return wrapper
