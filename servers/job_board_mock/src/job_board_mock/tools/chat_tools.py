from mcp.server.fastmcp import FastMCP

from ..services.chat_service import ChatService
from ._common import dumps, handle_errors


def register_chat_tools(mcp: FastMCP, chat_service: ChatService) -> None:

    @mcp.tool()
    @handle_errors
    async def chat_with_recruiter(user_id: str, job_id: str, message: str) -> str:
        """Send a message to the recruiter for a job. Reuses the existing thread for this user+job or opens a new one. The recruiter does not auto-reply (replies arrive out-of-band). Errors JOB_NOT_FOUND if the job is unknown."""
        return dumps(
            chat_service.chat_with_recruiter(
                user_id=user_id, job_id=job_id, message=message
            )
        )

    @mcp.tool()
    @handle_errors
    async def list_chats(user_id: str) -> str:
        """List a user's recruiter chat threads (most recently active first), each with its full message history in chronological order."""
        return dumps(chat_service.list_chats(user_id))
