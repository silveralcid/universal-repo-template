"""Selective context, local knowledge indexing and blank record scaffolding."""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import json
import re
from .core import safe_path, load_json, dump_json, text, sha, now, state, markdown_files

BUCKETS = {
    'research': ('research', 'exploratory', ('inbox', 'exploratory', 'candidates', 'validated', 'archive'), 'research-note.md'),
    'experiment': ('experiments', 'proposed', ('proposed', 'active', 'completed'), 'experiment-record.md'),
    'evidence': ('evidence', 'tests', ('tests', 'benchmarks', 'manual-qa', 'reproductions', 'audits', 'agent-evals'), 'evidence-record.md'),
    'handoff': ('handoffs', 'active', ('active', 'completed'), 'handoff.md'),
    'plan': ('plans', 'active', ('active', 'completed'), 'execution-plan.md'),
    'incident': ('incidents', 'reports', ('reports',), 'incident-report.md'),
    'task': ('tasks', 'ready', ('inbox', 'ready', 'completed'), 'ready-packet.md'),
    'decision': ('decisions', None, (None,), 'decision.md'),
    'adr': ('adr', None, (None,), 'adr.md'),
}


def context(root: Path, topic: str, optional=False) -> dict:
    routes = load_json(safe_path(root, 'docs/context/routes.json')).get('topics', {})
    if topic not in routes:
        raise ValueError('Unknown topic; available: ' + ', '.join(sorted(routes)))
    route = routes[topic]
    entries = [{'path': 'AGENTS.md', 'reason': 'Shared entrypoint', 'tier': 'always'}]
    for tier in ('required', 'optional') if optional else ('required',):
        entries.extend(dict(item, tier=tier) for item in route.get(tier, []))
    unique = {}
    for entry in entries:
        unique.setdefault(entry['path'], entry)
    result = []
    for entry in unique.values():
        path = safe_path(root, entry['path'])
        if not path.is_file():
            raise ValueError('Missing context target: ' + entry['path'])
        result.append(dict(entry, sha256=sha(path), estimated_tokens=(len(text(path)) + 3) // 4))
    return dict(schema_version=1, topic=topic, files=result,
                estimated_tokens=sum(x['estimated_tokens'] for x in result),
                estimate_method='characters / 4; not a tokenizer', budget_tokens=route.get('budget_tokens'))


def save_snapshot(root: Path, data: dict, relative: str):
    if not relative.startswith('.repo-local/'):
        raise ValueError('Context snapshots must be stored under ignored .repo-local/')
    output = safe_path(root, relative)
    dump_json(output, dict(data, observed_at=now(), source=state(root)), exclusive=True)
    return output


def compare_snapshot(root: Path, relative: str) -> dict:
    previous = load_json(safe_path(root, relative))
    changed, missing, same = [], [], []
    for item in previous['files']:
        path = safe_path(root, item['path'])
        if not path.is_file():
            missing.append(item['path'])
        elif sha(path) != item['sha256']:
            changed.append(item['path'])
        else:
            same.append(item['path'])
    # Routes can add relevant owners even if all previously read files are unchanged.
    route = load_json(safe_path(root, 'docs/context/routes.json'))['topics'].get(previous['topic'], {})
    old_paths = {x['path'] for x in previous['files']}
    tiers = ('required', 'optional') if any(x.get('tier') == 'optional' for x in previous['files']) else ('required',)
    new_paths = {'AGENTS.md'} | {x['path'] for tier in tiers for x in route.get(tier, [])}
    return dict(changed=changed, missing=missing, unchanged=same,
                newly_routed=sorted(new_paths - old_paths), no_longer_routed=sorted(old_paths - new_paths),
                limitation='File-content drift only. Inspect affected sections; no semantic-alignment claim.')


def new_record(root: Path, kind: str, slug: str, bucket=None) -> Path:
    if kind not in BUCKETS:
        raise ValueError('Unknown record kind')
    folder, default, choices, template = BUCKETS[kind]
    bucket = default if bucket is None else bucket
    if bucket not in choices:
        raise ValueError(f'Invalid bucket for {kind}: {bucket}; choices: {choices}')
    slug = slug.strip().lower().replace(' ', '-')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or len(slug) > 100:
        raise ValueError('Slug: 1-100 lowercase letters/numbers with single hyphens')
    today = datetime.now(timezone.utc).date().isoformat()
    rel = '/'.join(x for x in ('docs', folder, bucket, f'{today}-{slug}.md') if x)
    output = safe_path(root, rel)
    if kind == 'evidence':
        template = {'tests': 'test-report.md', 'benchmarks': 'benchmark-report.md',
                    'agent-evals': 'agent-eval.md'}.get(bucket, template)
    body = text(safe_path(root, 'docs/templates/' + template))
    body = body.replace('<date>', today)
    for key in ('<topic>', '<question>', '<hypothesis>', '<area>', '<task>', '<skill-or-role>', '<title>'):
        body = body.replace(key, slug.replace('-', ' '))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(body)
    return output


def inventory(root: Path) -> dict:
    """A derived index of authored records. No authority inference or external calls."""
    groups = {'research', 'experiments', 'evidence', 'handoffs', 'plans', 'tasks', 'decisions', 'adr', 'incidents'}
    result = []
    for path in markdown_files(root):
        rel = path.relative_to(root).as_posix()
        parts = rel.split('/')
        if len(parts) < 3 or parts[0] != 'docs' or parts[1] not in groups:
            continue
        if path.name in {'README.md', 'INDEX.md', 'ARTIFACTS.md'}:
            continue
        body = text(path)
        title = re.search(r'^#\s+(.+)$', body, re.M)
        tags = re.search(r'^\*\*Tags:\*\*\s*(.*)$', body, re.M)
        result.append(dict(path=rel, kind=parts[1], bucket=parts[2] if len(parts) > 3 else '',
                           title=title.group(1) if title else path.stem,
                           tags=tags.group(1) if tags else '', sha256=sha(path),
                           authority='NOT_INFERRED'))
    return dict(schema_version=1, records=result,
                note='Derived navigation only; folder maturity never approves product scope.')


def search_records(root: Path, query: str, kind=None, limit=20):
    terms = query.casefold().split()
    if not terms:
        raise ValueError('Provide a nonempty search query')
    scored = []
    for record in inventory(root)['records']:
        if kind and record['kind'] != kind:
            continue
        data = text(safe_path(root, record['path']))
        hay = ' '.join((record['path'], record['title'], record['tags'], data)).casefold()
        if not all(term in hay for term in terms):
            continue
        matching = [f'{i}: {line[:220]}' for i, line in enumerate(data.splitlines(), 1)
                    if any(term in line.casefold() for term in terms)][:3]
        score = sum(hay.count(term) for term in terms)
        scored.append((score, dict(record, matches=matching)))
    scored.sort(key=lambda x: (-x[0], x[1]['path']))
    return [record for _, record in scored[:limit]]
