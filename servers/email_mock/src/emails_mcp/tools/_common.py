import functools
import json
import logging
from typing import Any

from ..utils.exceptions import EmailsMockError

logger = logging.getLogger(__name__)


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def error_response(message: str, code: str) -> str:
    return dumps({"error": message, "code": code})


def handle_errors(fn):
    """Map ``EmailsMockError`` to structured JSON error responses.

    ``functools.wraps`` preserves the original signature so FastMCP can
    introspect it for the tool schema.
    """
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except EmailsMockError as e:
            logger.info("tool error [%s]: %s", e.code, e.message)
            return error_response(e.message, e.code)
        except Exception as e:  # pragma: no cover — defensive
            logger.exception("unexpected tool error")
            return error_response(f"internal error: {e}", "BAD_ARG")
    return wrapper
