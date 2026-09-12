import re

from ._helpers import *


_STAGE = 5
_BUSY_DATE = '2026-08-14'
_BUSY_START = 13 * 60
_BUSY_END = 15 * 60
_CALENDAR_READ_TOOLS = ('list_events', 'get_event', 'search_events')
_NOTION_WRITE_TOOLS = (
    'api_post_page',
    'api_patch_page',
    'api_patch_block_children',
    'api_update_a_block',
)
_INTERVAL_RE = re.compile(r'(?<!\d)(\d{1,2})\s*[:：]\s*(\d{2})\s*(?:[-–—~～]|to)\s*(\d{1,2})\s*[:：]\s*(\d{2})(?!\d)')


def _rows(value):
    value = _as_obj(value)
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in ('events', 'items', 'results', 'data'):
            rows = value.get(key)
            if isinstance(rows, list):
                return rows
    return []


def _calendar_has_child_rest_interval(value) -> bool:
    for row in _rows(value):
        if not isinstance(row, dict):
            continue
        start_value = row.get('start_dt') or row.get('start') or row.get('start_time') or ''
        end_value = row.get('end_dt') or row.get('end') or row.get('end_time') or ''
        if isinstance(start_value, dict):
            start_value = start_value.get('dateTime') or start_value.get('date') or ''
        if isinstance(end_value, dict):
            end_value = end_value.get('dateTime') or end_value.get('date') or ''
        start = str(start_value)
        end = str(end_value)
        identity = _flat({
            'event_id': row.get('event_id'),
            'summary': row.get('summary'),
            'description': row.get('description'),
        }).lower()
        if (
            start.startswith(f'{_BUSY_DATE}T13:00')
            and end.startswith(f'{_BUSY_DATE}T15:00')
            and any(marker in identity for marker in ('cal_evt_child_nap', 'child', 'nap', 'child rest'))
        ):
            return True
    return False


def _stage_calendar_read_has_busy_interval(env) -> bool:
    for call in _tool_calls(env, _STAGE):
        if call.get('success') is not True or call.get('result') in (None, ''):
            continue
        name = str(call.get('name') or '').lower().replace('-', '_')
        if 'calendar' not in name or not any(tool in name for tool in _CALENDAR_READ_TOOLS):
            continue
        if _calendar_has_child_rest_interval(call.get('result')):
            return True
    return False


def _minutes(hour: str, minute: str) -> int | None:
    hour_i, minute_i = int(hour), int(minute)
    if hour_i > 23 or minute_i > 59:
        return None
    return hour_i * 60 + minute_i


def _conflict_note_is_concrete(value) -> bool:
    text = _flat(value)
    normalized = text.replace('：', ':').replace('—', '-').replace('–', '-').replace('～', '-').replace('~', '-')
    compact = re.sub(r'\s+', '', normalized)
    date_ok = bool(
        re.search(r'(?:2026[-/.]0?8[-/.]14|0?8[-/.]14)', compact)
        or re.search(r'(?:august|aug)14(?:,?2026)?', compact, flags=re.I)
    )
    if not date_ok:
        return False
    if not any(marker in compact for marker in ('child', 'kid')):
        return False
    if not any(marker in compact for marker in ('nap', 'rest', 'sleep')):
        return False
    if not any(marker in compact for marker in ('viewing', 'guided viewing')):
        return False
    if not any(marker in compact for marker in ('nooverlap', 'avoidoverlap', 'avoidsoverlap', 'noconflict')):
        return False

    intervals = []
    for match in _INTERVAL_RE.finditer(normalized):
        start = _minutes(match.group(1), match.group(2))
        end = _minutes(match.group(3), match.group(4))
        if start is None or end is None or start >= end:
            continue
        intervals.append((start, end, match.start(), match.end()))
    if not any(start == _BUSY_START and end == _BUSY_END for start, end, _, _ in intervals):
        return False

    viewing_positions = [match.start() for match in re.finditer(r'viewing|guided viewing', normalized)]
    if not viewing_positions:
        return False
    candidates = [interval for interval in intervals if (interval[0], interval[1]) != (_BUSY_START, _BUSY_END)]
    if not candidates:
        return False
    viewing = min(
        candidates,
        key=lambda interval: min(
            abs(position - interval[2]) if position < interval[2] else abs(position - interval[3])
            for position in viewing_positions
        ),
    )
    viewing_start, viewing_end = viewing[0], viewing[1]
    return viewing_end <= _BUSY_START or viewing_start >= _BUSY_END


def _stage_notion_write_records_safe_interval(env) -> bool:
    for call in _tool_calls(env, _STAGE):
        if call.get('success') is not True or call.get('result') in (None, ''):
            continue
        name = str(call.get('name') or '').lower().replace('-', '_')
        if 'notion' not in name or not any(tool in name for tool in _NOTION_WRITE_TOOLS):
            continue
        if _conflict_note_is_concrete(_notion_write_payload(call)):
            return True
    return False


def r038_check_026_calendar_conflict(env) -> bool:
    return bool(
        _stage_calendar_read_has_busy_interval(env)
        and _calendar_has_child_rest_interval(calendar_events(env))
        and _stage_notion_write_records_safe_interval(env)
        and no_calendar_write(env)
    )


CHECKS = [
    ('r038_check_026_calendar_conflict', r038_check_026_calendar_conflict, 1.25),
]
