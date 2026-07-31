import functools
import json
import logging
from typing import Any

from ..utils.exceptions import ListingPlatformMockError

logger = logging.getLogger(__name__)


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def error_response(message: str, code: str) -> str:
    return dumps({"error": message, "code": code})


def handle_errors(fn):
    """Decorator: map ListingPlatformMockError to structured JSON responses.

    Uses functools.wraps so FastMCP introspects the wrapped function's
    real parameter signature (not the wrapper's ``*args, **kwargs``).
    """
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except ListingPlatformMockError as e:
            logger.info("tool error [%s]: %s", e.code, e.message)
            return error_response(e.message, e.code)
        except Exception as e:  # pragma: no cover — defensive
            logger.exception("unexpected tool error")
            return error_response(f"internal error: {e}", "BAD_ARG")
    return wrapper
