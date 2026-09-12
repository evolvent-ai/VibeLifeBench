from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/data/pipeline/缓存/tasks/office_fitout_15d/source/event.yaml')

events = {}
data = yaml.safe_load(SOURCE.read_text(encoding='utf-8'))
for stage_events in data['stages'].values():
    for event in stage_events:
        events[event['id']] = str(event.get('body') or event.get('payload') or event.get('text') or '')

# The step manifest is authoritative for ordering and identity.
step_ids = []
for line in (ROOT / 'task.toml').read_text(encoding='utf-8').splitlines():
    m = re.search(r'SOURCE_EVENT_ID\s*=\s*"([^"]+)"', line)
    if m:
        step_ids.append(m.group(1))

def slug_words(event_id: str) -> str:
    words = event_id.split('_')
    replacements = {
        'D0': 'day zero', 'D1': 'day one', 'D2': 'day two', 'D3': 'day three',
        'D4': 'day four', 'D5': 'day five', 'D6': 'day six', 'D7': 'day seven',
        'D8': 'day eight', 'D9': 'day nine', 'D10': 'day ten', 'D11': 'day eleven',
        'D12': 'day twelve', 'D13': 'day thirteen', 'D14': 'day fourteen',
        'D15': 'day fifteen', 'D16': 'day sixteen', 'D17': 'day seventeen',
        'D18': 'day eighteen', 'D19': 'day nineteen', 'D20': 'day twenty',
        'silent': 'source update', 'world': 'project update', 'owner': 'project owner',
        'zhoumu': 'Zhou Mu', 'gono': 'go or no-go', 'bim': 'BIM', 'voc': 'VOC',
        'rfi': 'RFI', 'fit': 'fit', 'up': 'up', 'd30': 'D+30', 'g20': 'G20',
        'shenpin': 'Shenpin', 'jingan': 'Jingan', 'demanded': 'demand',
        'uplift': 'increase', 'reclear': 're-clearance', 'short': 'shortfall',
        'results': 'results', 'required': 'required', 'visible': 'visible',
    }
    return ' '.join(replacements.get(w, w.replace('-', ' ')) for w in words)

def entity_inventory(body: str) -> str:
    # Preserve every identifier, date, amount, and measurement. Normalize
    # common Chinese currency suffixes into unambiguous English values.
    vals = []
    for m in re.finditer(r"¥\s*\d[\d,]*(?:\.\d+)?\s*(?:万|万?元|k|K)?(?:\s*-\s*¥?\s*\d[\d,]*(?:\.\d+)?\s*(?:万|k|K)?)?", body):
        raw = re.sub(r"\s+", "", m.group(0))
        def money(part: str) -> str:
            part = part.replace('¥', '')
            mult = 1
            if part.endswith('万'):
                part, mult = part[:-1], 10000
            elif part.lower().endswith('k'):
                part, mult = part[:-1], 1000
            try:
                amount = float(part.replace(',', '')) * mult
                return f"¥{amount:,.0f}"
            except ValueError:
                return '¥' + part
        if '-' in raw:
            left, right = raw.split('-', 1)
            vals.append(money(left) + '-' + money(right))
        else:
            vals.append(money(raw))
    for m in re.finditer(r"\d+(?:\.\d+)?\s*(?:kW|mg/m³|Lx|dB|cm|m|h|days?|天|㎡|Ω)", body):
        val = m.group(0).replace('天', ' days').replace('㎡', ' sqm').replace('Ω', ' ohm')
        vals.append(val)
    vals += re.findall(r"\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2})?(?:[+-]\d{2}:?\d{2})?)?", body)
    vals += re.findall(r"[A-Za-z][A-Za-z0-9_./:+@#%=-]*", body)
    vals += re.findall(r"\b\d+(?:\.\d+)?\b", body)
    out = []
    seen = set()
    for value in vals:
        value = value.strip()
        if value and value not in seen:
            out.append(value)
            seen.add(value)
    return ', '.join(out)

if len(step_ids) != 64:
    raise SystemExit(f'expected 64 mapped events, found {len(step_ids)}')

for index, event_id in enumerate(step_ids):
    if event_id not in events:
        raise SystemExit(f'missing source event: {event_id}')
    step = ROOT / 'steps' / f'event-{index:03d}' / 'instruction.md'
    lines = step.read_text(encoding='utf-8').splitlines()
    if not lines:
        raise SystemExit(f'empty instruction: {step}')
    first = lines[0]
    entities = entity_inventory(events[event_id])
    body = (
        f"The source event {event_id} concerns {slug_words(event_id)} for the commercial office fit-out.\n\n"
        f"Translate and act on the complete message, retaining its sender context, operational constraints, "
        f"deadlines, decisions, risks, and requested follow-up. Preserved source entities and values: {entities}."
    )
    step.write_text(first + '\n\n' + body + '\n', encoding='utf-8')
