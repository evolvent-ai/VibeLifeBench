import functools
import json
import logging
from typing import Any

from ..utils.exceptions import CreditCardMockError

logger = logging.getLogger(__name__)


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def error_response(message: str, code: str) -> str:
    return dumps({"error": message, "code": code})


def handle_errors(fn):
    """Decorator: map CreditCardMockError to structured {error, code} JSON.

    `functools.wraps` is required so FastMCP's schema reflection still sees the
    real parameter names.
    """
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except CreditCardMockError as e:
            logger.info(f"tool error [{e.code}]: {e.message}")
            return error_response(e.message, e.code)
        except Exception as e:
            logger.exception("unexpected tool error")
            return error_response(f"internal error: {e}", "BAD_ARG")
    return wrapper
