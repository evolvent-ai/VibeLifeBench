"""Shared decorator + JSON serializer for tool layer."""
import functools
import json
import logging
from typing import Any

from ..utils.exceptions import DeliveryMockError

logger = logging.getLogger(__name__)


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def error_response(message: str, code: str) -> str:
    return dumps({"error": message, "code": code})


def handle_errors(fn):
    """Decorator: map DeliveryMockError to a structured error JSON.

    Uses functools.wraps so FastMCP can read the real signature for
    schema generation (NOT the wrapper's ``*args, **kwargs``).
    """
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except DeliveryMockError as e:
            logger.info(f"tool error [{e.code}]: {e.message}")
            return error_response(e.message, e.code)
        except Exception as e:
            logger.exception("unexpected tool error")
            return error_response(f"internal error: {e}", "BAD_ARG")

    return wrapper
