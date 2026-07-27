import functools
import json
import logging
from typing import Any

from ..utils.exceptions import HotelMockError

logger = logging.getLogger(__name__)


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def error_response(message: str, code: str) -> str:
    return dumps({"error": message, "code": code})


def handle_errors(fn):
    """Decorator for tool handlers: map HotelMockError to structured responses.

    Uses functools.wraps so that the wrapper preserves the wrapped function's
    signature (__wrapped__, __signature__, etc.). This is required for FastMCP
    to generate a correct JSON schema from the real tool parameters rather
    than from the wrapper's ``*args, **kwargs``.
    """
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except HotelMockError as e:
            logger.info(f"tool error [{e.code}]: {e.message}")
            return error_response(e.message, e.code)
        except Exception as e:
            logger.exception("unexpected tool error")
            return error_response(f"internal error: {e}", "BAD_ARG")
    return wrapper
