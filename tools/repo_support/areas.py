"""Create an area authority + agent guide + context route from one bounded input.

A scaffold is DRAFT, never an approved specification or proof of working tests.
"""
from __future__ import annotations
from pathlib import Path
import re
from .core import safe_path, load_json, dump_json, text

ID_PATTERN = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
MARK_START = '<!-- AUTO-REGISTERED-AREAS:START -->'
MARK_END = '<!-- AUTO-REGISTERED-AREAS:END -->'


def _replace_rows(body: str, entries: list[str]) -> str:
    if MARK_START not in body or MARK_END not in body:
        raise ValueError('Missing registered-area markers; do not overwrite an edited owner index')
    before, rest = body.split(MARK_START, 1)
    _, after = rest.split(MARK_END, 1)
    return before + MARK_START + '\n' + '\n'.join(entries) + ('\n' if entries else '') + MARK_END + after


def create_area(root: Path, identifier: str, paths: list[str], checks: list[str] | None = None,
                title: str | None = None, budget: int = 5000) -> dict:
    if not isinstance(identifier, str) or not ID_PATTERN.fullmatch(identifier) or len(identifier) > 80:
        raise ValueError('Area ID must be a lower-kebab-case slug, maximum 80 characters')
    if not paths or not all(isinstance(p, str) and p and not p.startswith('/') and '\\' not in p
                            and '..' not in Path(p).parts and '\x00' not in p for p in paths):
        raise ValueError('Supply at least one safe repository-relative --path pattern')
    if len(paths) != len(set(paths)):
        raise ValueError('Duplicate --path patterns are not allowed')
    if any('[' in p or ']' in p or '\n' in p or '\r' in p or '|' in p for p in paths):
        raise ValueError('Path patterns cannot contain brackets, newlines or table separators')
    if not 1000 <= budget <= 50000:
        raise ValueError('Area context budget must be 1000-50000 estimated tokens')
    title = title or identifier.replace('-', ' ').title()
    if not isinstance(title, str) or not title.strip() or len(title) > 120 or any(c in title for c in '\r\n|[]<>'):
        raise ValueError('Area title must be a single plain-text line (1-120 characters)')
    title = title.strip()
    checks = list(dict.fromkeys(checks or []))
    cfg_path = safe_path(root, '.repo/areas.json')
    cfg = load_json(cfg_path)
    commands = load_json(safe_path(root, '.repo/project.json'))['commands']
    invalid = [c for c in checks if c not in commands or c == 'setup']
    if invalid:
        raise ValueError(f'Unknown/non-verification check slots: {invalid}')
    if any(area['id'] == identifier for area in cfg['areas']):
        raise ValueError(f'Area already registered: {identifier}')
    spec_rel = f'docs/areas/{identifier}/README.md'
    guide_rel = f'docs/agents/areas/{identifier}.md'
    index_rels = ('docs/INDEX.md', 'docs/agents/README.md')
    spec = safe_path(root, spec_rel)
    guide = safe_path(root, guide_rel)
    if spec.exists() or guide.exists():
        raise ValueError('Area document already exists; no files were overwritten')
    routes_path = safe_path(root, 'docs/context/routes.json')
    routes = load_json(routes_path)
    topic = f'area:{identifier}'
    if topic in routes['topics']:
        raise ValueError('Area context route already exists')
    # Preflight all mutable files before any writes.
    existing = [text(safe_path(root, rel)) for rel in index_rels]
    for contents in existing:
        if contents.count(MARK_START) != 1 or contents.count(MARK_END) != 1:
            raise ValueError('Registered-area markers missing or duplicated; no writes performed')
    cfg['areas'].append(dict(id=identifier, title=title, guide=guide_rel, spec=spec_rel,
                             paths=paths, checks=checks))
    cfg['areas'].sort(key=lambda a: a['id'])
    routes['topics'][topic] = dict(required=[
        dict(path=guide_rel, reason=f'{title}: task boundaries, code paths and targeted checks'),
        dict(path=spec_rel, reason=f'{title}: single canonical area specification')],
        optional=[dict(path='docs/agents/documentation.md', reason='Read only when changing area documentation')],
        budget_tokens=budget)
    routes['topics'] = dict(sorted(routes['topics'].items()))
    owner_rows = [f'| {a.get("title", a["id"])} (`{a["id"]}`) | [Canonical area specification](areas/{a["id"]}/README.md) |'
                  for a in cfg['areas'] if a.get('spec')]
    agent_rows = [f'| `{a["id"]}` | [Area guide](areas/{a["id"]}.md) | `area:{a["id"]}` | '
                  + (', '.join(f'`{c}`' for c in a['checks']) or 'NOT CONFIGURED') + ' |'
                  for a in cfg['areas'] if a.get('spec')]
    rewritten = [_replace_rows(existing[0], owner_rows), _replace_rows(existing[1], agent_rows)]
    path_lines = '\n'.join(f'- `{p}`' for p in paths)
    check_line = ', '.join(f'`{c}`' for c in checks) or 'NOT CONFIGURED'
    spec_body = (f'# {title} — area specification\n\n**Status:** DRAFT — scaffold, not an approved product decision.\n\n'
                 f'**Area ID:** `{identifier}`\n\n## Purpose and approved behavior\n\n'
                 'Record confirmed requirements and their source; leave undecided behavior OPEN.\n\n'
                 f'## Owned paths\n\n{path_lines}\n\n## Invariants and contracts\n\n'
                 'Name one owner per fact; link cross-area contracts instead of copying them.\n\n'
                 '## Dependencies, exclusions and open decisions\n\nRecord current evidence and unresolved issues.\n\n'
                 '## Acceptance\n\nDefine visible behavior and targeted verification once implemented.\n')
    guide_body = (f'# {title} — agent area guide\n\n'
                  f'**Single authority:** [Area specification](../../areas/{identifier}/README.md).\n\n'
                  f'**Context route:** `python tools/repo.py context --topic area:{identifier}`\n\n'
                  f'**Owned paths:**\n{path_lines}\n\n**Narrow verification slots:** {check_line}. '
                  'A configured slot still needs to run and pass; an unset slot is NOT CONFIGURED.\n\n'
                  '## Before editing\n\nRead the relevant sections of the area specification, inspect actual code and current tests, '
                  'and check overlaps with other areas. Do not load unrelated areas.\n\n'
                  '## Boundaries and invariants\n\nLink to the exact specification sections when those exist.\n\n'
                  '## Neighboring areas\n\nFollow only the affected contract.\n\n'
                  '## Handoff\n\nReport changed paths, evidence, checks run/not run, current branch and next action.\n')
    # Create the two new documents exclusively; config is updated only once they exist.
    spec.parent.mkdir(parents=True, exist_ok=True)
    guide.parent.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for path, body in ((spec, spec_body), (guide, guide_body)):
            with path.open('x', encoding='utf-8', newline='\n') as handle:
                handle.write(body)
            created.append(path)
        for rel, body in zip(index_rels, rewritten):
            safe_path(root, rel).write_text(body, encoding='utf-8', newline='\n')
        dump_json(cfg_path, cfg)
        dump_json(routes_path, routes)
    except OSError:
        # Never erase pre-existing files; keep an explicit partial-failure signal.
        for path in created:
            path.unlink(missing_ok=True)
        raise
    return dict(id=identifier, title=title, spec=spec_rel, guide=guide_rel,
                context_topic=topic, checks=checks, paths=paths,
                status='DRAFT_NOT_APPROVED_OR_TESTED')


def list_areas(root: Path) -> list[dict]:
    return load_json(safe_path(root, '.repo/areas.json'))['areas']
