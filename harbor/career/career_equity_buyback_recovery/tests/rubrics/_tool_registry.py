"""Single source of truth for MCP tool names referenced by the rubrics.

Rubrics match tool calls with *substring* needles through ``stage_calls`` /
``stage_call_matches`` / ``used_tool``, and with *exact* names through
``_call(env, server, tool)``. A bare needle that drifts from the real MCP tool
name — ``"recommend_jobs"`` for ``get_recommended_jobs`` — silently deadens a
check: the filter matches nothing, no error is raised, and the weight is just
lost. This module is the registry every rubric and test must consult, and
``test_tool_name_registry.py`` pins it two ways:

  1. ``TOOLS`` equals the ``@mcp.tool()`` surface actually exported by the mock
     servers (parsed from their source), so a rename in a mock fails the test.
  2. Every tool-name needle in the rubric sources is a substring of a registered
     name, so a needle that drifts fails the test instead of going quiet.

Generated from ``environment/servers/*/tools/*.py``; do not edit by hand without
re-running the registry test.
"""
from __future__ import annotations

TOOLS: dict[str, frozenset[str]] = {
    "banking": frozenset({
        "list_accounts", "get_account", "list_transactions",
        "list_payees", "list_pending_payments", "add_payee", "pay_payee",
        "schedule_recurring", "cancel_recurring", "list_recurring", "transfer",
    }),
    "brokerage": frozenset({
        "get_quote",
        "list_funds", "get_fund_nav", "subscribe_fund", "redeem_fund",
        "list_accounts", "get_portfolio", "get_positions", "get_portfolio_perf",
        "list_orders", "place_order", "cancel_order",
    }),
    "calendar": frozenset({
        "list_calendars",
        "list_events", "get_event", "create_event", "update_event",
        "delete_event", "search_events",
    }),
    "email": frozenset({
        "get_folders", "create_folder", "delete_folder", "get_mailbox_stats",
        "get_unread_count",
        "get_emails", "read_email", "search_emails", "send_email", "reply_email",
        "forward_email", "delete_email", "delete_emails", "move_email",
        "move_emails", "mark_emails",
        "check_connection", "get_email_headers", "download_attachment",
        "export_emails", "import_emails",
        "save_draft", "get_drafts", "update_draft", "delete_draft",
    }),
    "job_board": frozenset({
        "chat_with_recruiter", "list_chats",
        "create_resume", "update_resume", "list_resumes", "get_resume",
        "save_job", "unsave_job", "list_saved_jobs", "apply_job",
        "list_applications", "get_application_status", "subscribe_job_alert",
        "search_jobs", "get_job", "get_company", "get_recommended_jobs",
    }),
    "legal_search": frozenset({
        "search_cases", "get_case", "get_similar_cases", "get_case_citations",
        "save_case", "list_saved", "add_note_to_case",
        "search_statutes", "get_statute", "list_statute_articles", "get_article",
        "list_courts", "get_court",
    }),
    "notion": frozenset({
        "API-post-page", "API-retrieve-a-page", "API-patch-page",
        "API-retrieve-a-page-property",
        "API-get-block-children", "API-patch-block-children",
        "API-retrieve-a-block", "API-update-a-block", "API-delete-a-block",
        "API-create-a-database", "API-retrieve-a-database", "API-update-a-database",
        "API-create-a-comment", "API-retrieve-a-comment",
        "API-get-user", "API-get-users", "API-get-self",
        "API-post-database-query", "API-post-search",
    }),
}


def all_tool_names() -> frozenset[str]:
    """Every registered MCP tool name across all servers."""
    out: set[str] = set()
    for names in TOOLS.values():
        out.update(names)
    return frozenset(out)
