"""Recruiter chat: send a message (creating a thread on first contact)."""
import logging
import sqlite3
from typing import List

from ..backends.db import next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import BadArgError, ChatNotFoundError
from ..utils.ids import chat_id as make_chat_id, message_id as make_message_id
from ._fetch import fetch_job

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def chat_with_recruiter(self, user_id: str, job_id: str, message: str) -> dict:
        """Send a message to the recruiter for a job.

        Reuses the existing thread for (user, job) if one exists; otherwise
        opens a new thread. The recruiter does not auto-reply — replies arrive
        as out-of-band SQL mutations from the orchestrator.
        """
        if not user_id:
            raise BadArgError("user_id is required")
        if not message:
            raise BadArgError("message is required")
        job = fetch_job(self.conn, job_id)
        ts = now_iso_z()

        chat = self.conn.execute(
            "SELECT * FROM chats WHERE user_id = ? AND job_id = ?",
            (user_id, job_id),
        ).fetchone()
        if chat:
            chat_id = chat["chat_id"]
        else:
            comp = self.conn.execute(
                "SELECT name FROM companies WHERE company_id = ?",
                (job["company_id"],),
            ).fetchone()
            recruiter_name = f"{comp['name']}招聘" if comp else "HR"
            seq = next_counter(self.conn, "chat_seq")
            chat_id = make_chat_id(seq)
            self.conn.execute(
                """
                INSERT INTO chats (chat_id, user_id, job_id, company_id,
                                   recruiter_name, created_at, last_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (chat_id, user_id, job_id, job["company_id"],
                 recruiter_name, ts, ts),
            )

        mseq = next_counter(self.conn, "message_seq")
        msg_id = make_message_id(mseq)
        self.conn.execute(
            """
            INSERT INTO chat_messages (message_id, chat_id, sender, body, sent_at)
            VALUES (?, ?, 'user', ?, ?)
            """,
            (msg_id, chat_id, message, ts),
        )
        self.conn.execute(
            "UPDATE chats SET last_at = ? WHERE chat_id = ?", (ts, chat_id)
        )
        return {
            "chat_id": chat_id,
            "message_id": msg_id,
            "job_id": job_id,
            "sender": "user",
            "body": message,
            "sent_at": ts,
        }

    def list_chats(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            "SELECT * FROM chats WHERE user_id = ? "
            "ORDER BY last_at DESC, chat_id ASC",
            (user_id,),
        ).fetchall()
        out = []
        for c in rows:
            msgs = self.conn.execute(
                "SELECT message_id, sender, body, sent_at FROM chat_messages "
                "WHERE chat_id = ? ORDER BY sent_at ASC, message_id ASC",
                (c["chat_id"],),
            ).fetchall()
            job = self.conn.execute(
                "SELECT title FROM jobs WHERE job_id = ?", (c["job_id"],)
            ).fetchone()
            out.append({
                "chat_id": c["chat_id"],
                "job_id": c["job_id"],
                "job_title": job["title"] if job else None,
                "company_id": c["company_id"],
                "recruiter_name": c["recruiter_name"],
                "created_at": c["created_at"],
                "last_at": c["last_at"],
                "messages": [
                    {
                        "message_id": m["message_id"],
                        "sender": m["sender"],
                        "body": m["body"],
                        "sent_at": m["sent_at"],
                    }
                    for m in msgs
                ],
            })
        return out
