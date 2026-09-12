from __future__ import annotations
import json
from ._helpers import TRACE_DIR, STAGE_COUNT, _workspace_fs


def _records(env):
    rows=[]
    fs=_workspace_fs(env)
    if fs is None:
        return rows
    for stage in range(STAGE_COUNT):
        path=f'{TRACE_DIR}/stage_{stage}.json'
        try:
            raw=fs.read_file(path).decode('utf-8',errors='replace')
        except (FileNotFoundError,KeyError):
            continue
        except Exception as error:
            raise RuntimeError(f'trace read failed for stage_{stage}: {type(error).__name__}: {error}') from error
        try:
            data=json.loads(raw or '[]')
        except json.JSONDecodeError as error:
            raise RuntimeError(f'trace parse failed for stage_{stage}: {error}') from error
        if not isinstance(data,list):
            raise RuntimeError(f'trace contract failed for stage_{stage}: expected list')
        rows.extend(item for item in data if isinstance(item,dict))
    return rows


def _business_payload(value):
    if value in (None,'',[],{}):
        return False
    if isinstance(value,dict) and set(value) <= {'ok','echo'}:
        return False
    return True


def successful_tool_result(env) -> bool:
    rows=_records(env)
    successful=[r for r in rows if r.get('success') is True and _business_payload(r.get('result'))]
    return len(successful) >= 12


def no_missing_or_failed_tool_result(env) -> bool:
    rows=_records(env)
    return bool(rows) and all(r.get('success') is True and not r.get('error') and r.get('result') not in (None,'') for r in rows)


def cross_service_evidence(env) -> bool:
    core={'listing_platform','maps','calendar','email','notion','review_platform','banking'}
    servers=set()
    for row in _records(env):
        if row.get('success') is not True or not _business_payload(row.get('result')):
            continue
        name=str(row.get('name') or '').lower().replace('-','_')
        servers.update(server for server in core if server in name)
    return len(servers) >= 6

CHECKS=[
 ('tool_quality_successful_results',successful_tool_result,3.0),
 ('tool_quality_no_missing_or_failed_results',no_missing_or_failed_tool_result,3.0),
 ('tool_quality_cross_service_evidence',cross_service_evidence,2.0),
]
