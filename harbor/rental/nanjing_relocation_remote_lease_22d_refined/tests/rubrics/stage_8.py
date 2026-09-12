"""Stage 8 — read the draft contract email; surface the payee account name."""
from __future__ import annotations
from ._helpers import agent_queried_email, file_has, has_any, stage_corpus, tool_call_arg_has_any

def s8_read_contract_payee(env) -> bool:
    read = agent_queried_email(env, stage=8)
    noted = has_any(stage_corpus(env, 8), ['payee name', 'payee', 'payee account', 'account name', 'account name'])
    durable = file_has(env, 'audit_journal.md', ['payee name', 'email'], minimum=2) or file_has(env, 'decision_log.md', ['collection', 'account name'], minimum=2)
    return read and noted and durable

def s8_contract_emails_compared(env) -> bool:
    searched_contract = tool_call_arg_has_any(env, 'email', 'search_emails', ['contract', 'collection'], stage=8)
    read_some = agent_queried_email(env, stage=8)
    durable = file_has(env, 'audit_journal.md', ['Mingfa', 'Gu Jianguo', 'Venice Water City', 'Li Wei', 'Qiaolin New Estate', 'Liu Jianhua'], minimum=4)
    return searched_contract and read_some and durable
CHECKS = [('s8_read_contract_payee', s8_read_contract_payee, 1.4910394265232976), ('s8_contract_emails_compared', s8_contract_emails_compared, 3.727598566308244)]
