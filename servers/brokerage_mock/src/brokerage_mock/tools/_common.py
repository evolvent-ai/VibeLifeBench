"""Shared tool wrappers."""
import functools
import json
import logging
from typing import Any

from ..utils.exceptions import BrokerageMockError

logger = logging.getLogger(__name__)


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def error_response(message: str, code: str) -> str:
    return dumps({"error": message, "code": code})


def handle_errors(fn):
    """Decorator: map BrokerageMockError to structured JSON responses.

    Uses functools.wraps so FastMCP can introspect the wrapped function's
    real signature and generate a correct parameter schema.
    """
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except BrokerageMockError as e:
            logger.info("tool error [%s]: %s", e.code, e.message)
            return error_response(e.message, e.code)
        except Exception as e:
            logger.exception("unexpected tool error")
            return error_response(f"internal error: {e}", "BAD_ARG")
    return wrapper
