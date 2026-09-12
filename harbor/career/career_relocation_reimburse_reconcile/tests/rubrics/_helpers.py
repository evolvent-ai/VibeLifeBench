from __future__ import annotations
import json
import re
from typing import Any
from harbor_evidence import response, snapshot, trace

def _latest_stage(env) -> int:
    active = getattr(env, 'active_stage', None)
    if isinstance(active, int):
        return active
    stages = env.published_stages()
    if not stages:
        raise RuntimeError('no frozen stages have been published')
    return stages[-1]

def _snapshot(env, stage: int | None = None) -> dict[str, Any]:
    return snapshot(env, _latest_stage(env) if stage is None else stage)

def _checked(value: Any, server: str, tool: str) -> Any:
    if isinstance(value, dict) and value.get('error') not in (None, False, ''):
        raise RuntimeError(f'{server}.{tool} snapshot read failed: {value["error"]}')
    return value

def _call(env, server: str, tool: str, **kwargs: Any) -> Any:
    stage = kwargs.pop('_evidence_stage', None)
    state = _snapshot(env, stage)
    section = state.get(server, {})
    if not isinstance(section, dict):
        return None
    _checked(section, server, tool)
    if server == 'job_board':
        if tool == 'list_applications':
            key = 'alternate_applications' if kwargs.get('user_id') == 'gao_kai' else 'applications'
            return _checked(section.get(key), server, tool)
        if tool == 'get_job':
            return _checked((section.get('jobs') or {}).get(str(kwargs.get('job_id') or '')), server, tool)
        if tool == 'list_saved':
            return _checked(section.get('saved'), server, tool)
        if tool == 'search_jobs':
            jobs = section.get('jobs') or {}
            return {'jobs': [value for value in jobs.values() if isinstance(value, dict) and 'error' not in value]}
    if server == 'legal_search':
        if tool == 'list_saved':
            return _checked(section.get('saved_cases'), server, tool)
        if tool == 'get_case':
            return _checked((section.get('cases') or {}).get(str(kwargs.get('case_id') or '')), server, tool)
        if tool == 'get_statute':
            return _checked((section.get('statutes') or {}).get(str(kwargs.get('statute_id') or '')), server, tool)
        if tool == 'get_article':
            return _checked((section.get('articles') or {}).get(str(kwargs.get('article_id') or '')), server, tool)
        if tool == 'search_cases':
            cases = section.get('cases') or {}
            return {'cases': [value for value in cases.values() if isinstance(value, dict) and 'error' not in value]}
    if server == 'banking':
        if tool == 'list_accounts':
            return _checked(section.get('accounts'), server, tool)
        if tool == 'list_transactions':
            return _checked((section.get('transactions') or {}).get(str(kwargs.get('account_id') or '')), server, tool)
    if server == 'credit_card':
        if tool == 'list_statements':
            return _checked(section.get('statements'), server, tool)
        if tool == 'get_statement':
            return _checked((section.get('statement_details') or {}).get(str(kwargs.get('statement_id') or '')), server, tool)
        if tool == 'list_unbilled':
            return _checked(section.get('unbilled'), server, tool)
        if tool in {'get_card', 'list_cards'}:
            return _checked(section.get('cards'), server, tool)
    if server == 'email':
        if tool == 'get_emails':
            folder = str(kwargs.get('folder') or '').lower()
            key = 'sent' if folder in {'sent', 'inbox.sent', 'sent items'} else 'inbox'
            block = section.get(key) or {}
            return _checked(block.get('listing') if isinstance(block, dict) else block, server, tool)
        if tool == 'read_email':
            wanted = str(kwargs.get('email_id') or '')
            for key in ('sent', 'inbox'):
                block = section.get(key) or {}
                for item in block.get('details') or []:
                    if str(item.get('email_id') or item.get('id') or '') == wanted:
                        return item
    if server == 'calendar':
        if tool == 'list_calendars':
            return {'calendars': [{'calendar_id': 'cal_gk_0001'}]}
        if tool == 'list_events':
            return _checked(section.get('events'), server, tool)
    if server == 'notion':
        if tool == 'API-post-search':
            pages = section.get('pages') or {}
            return pages
        if tool == 'API-get-block-children':
            block_id = str(kwargs.get('block_id') or '')
            return (section.get('page_blocks') or {}).get(block_id, (section.get('row_children') or {}).get(block_id))
        if tool == 'API-post-database-query':
            return (section.get('database_rows') or {}).get(str(kwargs.get('database_id') or ''))
    return None

def text_has(text: str, groups: list[list[str]]) -> bool:
    if not text:
        return False
    low = text.lower()
    for group in groups:
        if not any((str(s).lower() in low for s in group)):
            return False
    return True

def any_kw(text: str, needles: list[str]) -> bool:
    if not text:
        return False
    low = text.lower()
    for n in needles:
        n_low = str(n).lower()
        idx = low.find(n_low)
        while idx != -1:
            prefix = low[max(0, idx - 12):idx]
            if not any((neg in prefix for neg in ('not', "don't", 'do not', 'never', 'without', 'no need'))):
                return True
            idx = low.find(n_low, idx + 1)
    return False

def norm_num(text: str) -> str:
    return re.sub('[,\\s，]', '', text or '')

def has_exact_number(text: str, value: int | str) -> bool:
    return re.search(rf'(?<!\\d){re.escape(str(value))}(?!\\d)', norm_num(text or '')) is not None

def count_value_hits(text: str, value_groups: list[list[str]]) -> int:
    raw = (text or '').lower()
    t = norm_num(raw)
    hits = 0
    for grp in value_groups:
        if any((norm_num(v.lower()) in t or v.lower() in raw for v in grp)):
            hits += 1
    return hits
_USER_ID = 'usr_gao_kai'
_ALT_USER_IDS = ('usr_gao_kai', 'gao_kai')

def _user_ids() -> tuple[str, ...]:
    return _ALT_USER_IDS

def get_job(env, job_id: str) -> dict | None:
    data = _call(env, 'job_board', 'get_job', job_id=job_id)
    return data if isinstance(data, dict) else None

def list_applications(env) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for uid in _user_ids():
        data = _call(env, 'job_board', 'list_applications', user_id=uid)
        batch = []
        if isinstance(data, dict):
            batch = list(data.get('applications') or data.get('results') or data.get('items') or [])
        elif isinstance(data, list):
            batch = list(data)
        for a in batch:
            aid = str(a.get('application_id') or a.get('id') or '')
            if aid and aid in seen:
                continue
            seen.add(aid)
            out.append(a)
    return out

def applications_by_status(env) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for a in list_applications(env):
        out.setdefault(str(a.get('status') or ''), []).append(a)
    return out
TRAP_JOB_IDS = ('job_gk_0005', 'job_gk_0006')
TRAP_COMPANY_IDS = ('comp_borchina', 'comp_ruijietech')
NONCOMPETE_JOB_ID = 'job_gk_0007'

def applied_job_ids(env) -> set[str]:
    return {str(a.get('job_id') or '') for a in list_applications(env) if a.get('job_id')}

def is_preference_job(env, job_id: str) -> bool:
    j = get_job(env, job_id)
    if not j:
        return False
    city = str(j.get('city') or '')
    cat = (str(j.get('category') or '') + str(j.get('title') or '')).lower()
    return city == 'Shanghai' and ('backend' in cat or 'platform' in cat)

def get_case(env, case_id: str) -> dict | None:
    data = _call(env, 'legal_search', 'get_case', case_id=case_id)
    return data if isinstance(data, dict) else None

def get_article(env, article_id: str) -> dict | None:
    data = _call(env, 'legal_search', 'get_article', article_id=article_id)
    return data if isinstance(data, dict) else None

def list_transactions(env, account_id: str='acct_gk_checking', stage: int | None=None, **kwargs: Any) -> list[dict]:
    kwargs.setdefault('limit', 400)
    if stage is not None:
        kwargs['_evidence_stage'] = stage
    data = _call(env, 'banking', 'list_transactions', account_id=account_id, **kwargs)
    if isinstance(data, dict):
        return list(data.get('transactions') or data.get('results') or data.get('items') or [])
    if isinstance(data, list):
        return list(data)
    return []

def salary_deposits_trailing12(env, stage: int | None=None) -> list[int]:
    out: list[int] = []
    for t in list_transactions(env, stage=stage):
        if str(t.get('kind') or '') != 'deposit':
            continue
        cp = str(t.get('counterparty') or '')
        if 'Lithic Manufacturing' not in cp:
            continue
        ts = str(t.get('posted_at') or '')
        if ts[:7] >= '2025-06' and ts[:7] <= '2026-05':
            try:
                out.append(int(t.get('amount_minor')))
            except (TypeError, ValueError):
                continue
    return out

def severance_deposit_minor(env, stage: int | None=None) -> int | None:
    for t in list_transactions(env, stage=stage):
        if str(t.get('kind') or '') != 'deposit':
            continue
        if str(t.get('tx_id') or '') == 'tx_gk_severance':
            try:
                return int(t.get('amount_minor'))
            except (TypeError, ValueError):
                return None
    return None
def _rich_text_str(rich_text) -> str:
    out: list[str] = []
    for rt in rich_text or []:
        if not isinstance(rt, dict):
            continue
        val = rt.get('plain_text')
        if not val:
            txt = rt.get('text')
            if isinstance(txt, dict):
                val = txt.get('content')
        if not val:
            val = rt.get('content')
        if val:
            out.append(str(val))
    return ''.join(out)

def _block_text(block, env, depth: int=0) -> list[str]:
    chunks: list[str] = []
    if not isinstance(block, dict):
        return chunks
    bt = block.get('type') or ''
    td = block.get(bt) or {}
    if isinstance(td, dict):
        s = _rich_text_str(td.get('rich_text'))
        if s:
            chunks.append(s)
        for cell in td.get('cells') or []:
            chunks.append(_rich_text_str(cell))
    if depth < 2 and block.get('has_children') and block.get('id'):
        sub = _call(env, 'notion', 'API-get-block-children', block_id=block.get('id'))
        for child in (sub.get('results') if isinstance(sub, dict) else []) or []:
            chunks.extend(_block_text(child, env, depth + 1))
    return chunks

def notion_text(env) -> str:
    return json.dumps(_snapshot(env).get('notion', {}), ensure_ascii=False, default=str)

def wfile(env, basename: str) -> str:
    base = basename.split('/')[-1]
    workspace = _snapshot(env).get('workspace', {})
    if not isinstance(workspace, dict):
        return ''
    for path, value in workspace.items():
        if str(path).split('/')[-1] == base:
            return str(value)
    return ''

def workspace_text(env) -> str:
    workspace = _snapshot(env).get('workspace', {})
    if not isinstance(workspace, dict):
        return ''
    return '\n'.join((str(value) for value in workspace.values()))

def derived_text(env, stage: int | None = None) -> str:
    if stage is None:
        return (notion_text(env) + '\n' + workspace_text(env)).lower()
    state = _snapshot(env, stage)
    return (json.dumps(state.get('notion', {}), ensure_ascii=False, default=str) + '\n'
            + '\n'.join(str(value) for value in (state.get('workspace', {}) or {}).values())).lower()

def persisted_text(env, stage: int | None = None) -> str:
    return derived_text(env, stage)
_CANON_RE = re.compile('(job_gk_\\d{3,}|app[_a-z0-9]*\\d{3,}|tx_gk_[a-z0-9]+|case_\\d{3,}|art_[a-z0-9_]+|acct_gk_[a-z]+|\\d{8,})')

def audit_ref_count(env, corpus: str | None=None) -> int:
    if corpus is None:
        corpus = derived_text(env)
    return len(set(_CANON_RE.findall(corpus or '')))
_TX_RE = re.compile('tx_gk_[0-9a-z]{3,}')

def audit_tx_count(env, corpus: str | None=None) -> int:
    if corpus is None:
        corpus = derived_text(env)
    return len(set(_TX_RE.findall(corpus or '')))

def has_audit_ids(env, n: int=2) -> bool:
    return audit_ref_count(env) >= n

def stage_response(env, stage_idx: int, lower: bool=True) -> str:
    text = response(env, stage_idx)
    return text.lower() if lower else text

def stage_or_corpus(env, stage_idx: int) -> str:
    return stage_response(env, stage_idx) + '\n' + persisted_text(env, stage_idx)

def stage_tool_calls(env, stage_idx: int) -> list[dict]:
    return trace(env, stage_idx)

def all_tool_calls(env, up_to_stage: int | None=None) -> list[dict]:
    out: list[dict] = []
    stages = env.published_stages()
    if up_to_stage is not None:
        stages = [stage for stage in stages if stage <= up_to_stage]
    for i in stages:
        out.extend(stage_tool_calls(env, i))
    return out

def used_tool(env, name_contains: str, stage: int | None=None, arg_substr: str | None=None) -> bool:
    if stage is None:
        active = getattr(env, 'active_stage', None)
        calls = stage_tool_calls(env, active) if isinstance(active, int) else all_tool_calls(env)
    else:
        calls = stage_tool_calls(env, stage)
    nc = name_contains.lower()
    for c in calls:
        if c.get('success') is not True:
            continue
        nm = str(c.get('name') or '').lower()
        if nc not in nm:
            continue
        if arg_substr is None:
            return True
        if arg_substr.lower() in json.dumps(c.get('arguments') or {}, ensure_ascii=False).lower():
            return True
    return False

def successful_tool_results(env, name_contains: str, stage: int, arg_substr: str | None=None) -> list[Any]:
    out: list[Any] = []
    nc = name_contains.lower()
    for call in stage_tool_calls(env, stage):
        if call.get('success') is not True or nc not in str(call.get('name') or '').lower():
            continue
        if arg_substr is not None and arg_substr.lower() not in json.dumps(call.get('arguments') or {}, ensure_ascii=False).lower():
            continue
        out.append(_decode_trace_result(call.get('result')))
    return out

def _decode_trace_result(result: Any) -> Any:
    if isinstance(result, str):
        try:
            return _decode_trace_result(json.loads(result))
        except json.JSONDecodeError:
            return result
    if isinstance(result, dict):
        for key in ('result', 'structuredContent', 'structured_content'):
            if key in result:
                return _decode_trace_result(result[key])
        content = result.get('content')
        if isinstance(content, list):
            return _decode_trace_result(content)
    if isinstance(result, list) and len(result) == 1:
        block = result[0]
        if isinstance(block, dict) and 'text' in block:
            return _decode_trace_result(block['text'])
    return result

def result_rows(result: Any) -> list[dict[str, Any]]:
    if isinstance(result, list):
        return [row for row in result if isinstance(row, dict)]
    if isinstance(result, dict):
        for key in ('items', 'results', 'jobs', 'cases', 'transactions'):
            rows = result.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
    return []

def relocation_statement_total_minor(env, stage: int=2) -> int | None:
    totals: list[int] = []
    for result in successful_tool_results(env, 'get_statement', stage):
        if not isinstance(result, dict):
            continue
        lines = result.get('statement_lines')
        if not isinstance(lines, list):
            continue
        selected = [line for line in lines if isinstance(line, dict)
                    and 'relocation reimbursement' in str(line.get('category') or '').lower()
                    and str(line.get('kind') or '') in {'purchase', 'refund', 'adjustment'}]
        if selected:
            totals.append(sum(int(line.get('amount_minor')) for line in selected))
    return totals[0] if len(totals) == 1 else None

def _email_id(e: dict) -> str | None:
    for k in ('email_id', 'id', 'message_id'):
        v = e.get(k)
        if v is not None:
            return str(v)
    return None

def _hydrate_body(env, e: dict) -> dict:
    if e.get('body_text') or e.get('body'):
        return e
    eid = _email_id(e)
    if eid is None:
        return e
    full = _call(env, 'email', 'read_email', email_id=eid)
    if isinstance(full, dict) and (full.get('body_text') or full.get('body')):
        merged = dict(e)
        merged['body_text'] = full.get('body_text') or full.get('body') or ''
        return merged
    return e

def sent_emails(env) -> list[dict]:
    out: list[dict] = []
    for folder in ('Sent', 'INBOX.Sent', 'Sent Items'):
        data = _call(env, 'email', 'get_emails', folder=folder)
        if isinstance(data, list):
            out.extend(data)
        elif isinstance(data, dict):
            out.extend(data.get('emails') or data.get('messages') or [])
    return [_hydrate_body(env, e) for e in out]

def _strip_quoted(body: str) -> str:
    if not body:
        return ''
    for marker in ('--- Original Message ---', '----- Original Message', 'Original Message:', 'wrote:', '>'):
        idx = body.find(marker)
        if idx != -1:
            body = body[:idx]
            break
    return body

def _email_recipient(e: dict) -> str:
    for k in ('to_addr', 'to', 'to_addr_json', 'recipient'):
        v = e.get(k)
        if v:
            return str(v)
    return ''

def sent_to_recruiter_text(env, recruiter_keys: list[str]) -> str:
    chunks: list[str] = []
    for e in sent_emails(env):
        to = _email_recipient(e).lower()
        if not any((k.lower() in to for k in recruiter_keys)):
            continue
        chunks.append(str(e.get('subject') or ''))
        chunks.append(_strip_quoted(str(e.get('body_text') or e.get('body') or '')))
    return '\n'.join(chunks).lower()

def calendar_events(env) -> list[dict]:
    cals = _call(env, 'calendar', 'list_calendars', user_id=_USER_ID)
    cal_list = []
    if isinstance(cals, list):
        cal_list = cals
    elif isinstance(cals, dict):
        cal_list = cals.get('calendars') or cals.get('results') or []
    out: list[dict] = []
    for c in cal_list:
        cid = c.get('calendar_id') or c.get('id') if isinstance(c, dict) else None
        if not cid:
            continue
        data = _call(env, 'calendar', 'list_events', calendar_id=cid, max_results=500)
        if isinstance(data, list):
            out.extend(data)
        elif isinstance(data, dict):
            out.extend(data.get('events') or data.get('results') or [])
    return out

def _event_dt_str(e: dict, which: str) -> str:
    v = e.get(which) or e.get(which + '_dt') or e.get(which + 'Time')
    if isinstance(v, dict):
        return str(v.get('dateTime') or v.get('date') or '')
    return str(v or '')

def calendar_text(env) -> str:
    chunks: list[str] = []
    for e in calendar_events(env):
        if isinstance(e, dict):
            chunks.append(str(e.get('summary') or ''))
            chunks.append(str(e.get('description') or ''))
            chunks.append(_event_dt_str(e, 'start'))
    return '\n'.join(chunks).lower()

def _parse_dt(s):
    import datetime
    if isinstance(s, dict):
        s = s.get('dateTime') or s.get('date') or ''
    if not s:
        return None
    s = str(s).strip()
    if s.endswith('Z'):
        s = s[:-1] + '+00:00'
    try:
        return datetime.datetime.fromisoformat(s)
    except Exception:
        return None

def prenatal_conflict_violations(env) -> list[dict]:
    import datetime
    violations: list[dict] = []
    for e in calendar_events(env):
        if not isinstance(e, dict):
            continue
        summ = str(e.get('summary') or '')
        if 'prenatal checkup' in summ.lower() or 'accompany' in summ.lower():
            continue
        if str(e.get('event_id') or '') == 'evt_gk_0001':
            continue
        start = _parse_dt(_event_dt_str(e, 'start'))
        end = _parse_dt(_event_dt_str(e, 'end'))
        if not start:
            continue
        if not end:
            end = start + datetime.timedelta(hours=1)
        if end - start > datetime.timedelta(hours=12):
            continue
        if not datetime.date(2026, 6, 10) <= start.date() <= datetime.date(2026, 10, 21):
            continue
        if start.weekday() != 2:
            continue
        sh = start.hour + start.minute / 60.0
        eh = end.hour + end.minute / 60.0 if end > start else sh + 0.5
        if sh < 11.5 and eh > 9.0:
            violations.append({'event_id': e.get('event_id'), 'summary': summ, 'start': _event_dt_str(e, 'start')})
    return violations

def prenatal_event_intact(env) -> bool:
    for e in calendar_events(env):
        if not isinstance(e, dict):
            continue
        if str(e.get('event_id') or '') != 'evt_gk_0001':
            continue
        if str(e.get('status') or '').lower() == 'cancelled':
            return False
        start = _event_dt_str(e, 'start')
        rr = str(e.get('recurrence_rule') or '')
        if '09:00' not in start:
            return False
        if 'FREQ=WEEKLY' not in rr or 'BYDAY=WE' not in rr:
            return False
        return True
    return False
