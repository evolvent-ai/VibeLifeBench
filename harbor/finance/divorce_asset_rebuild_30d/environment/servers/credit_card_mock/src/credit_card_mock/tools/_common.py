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
            # Not BAD_ARG: an unexpected exception here is a server-side fault
            # (e.g. sqlite3.OperationalError "database is locked"), not a
            # problem with the caller's arguments. Reporting it as BAD_ARG tells
            # the agent to fix its input for a condition a retry would clear.
            logger.exception("unexpected tool error")
            return error_response(f"internal error: {e}", "INTERNAL")
    return wrapper
