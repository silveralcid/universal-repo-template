"""Mechanical validation. Never claims semantic or native-client verification."""
from __future__ import annotations
import re
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlsplit
from .core import safe_path, load_json, text, markdown_files, anchors, links, frontmatter
from .budgets import budget_config_errors

REQUIRED = ['README.md', 'START-HERE.md', 'AGENTS.md', 'CLAUDE.md', 'PLANS.md',
            '.repo/project.json', '.repo/areas.json', 'docs/INDEX.md',
            'docs/context/routes.json', 'docs/project/BRIEF.md',
            'docs/agents/startup.md', 'docs/agents/documentation.md',
            'docs/engineering/VERIFICATION.md', 'docs/agents/definition-of-done.md',
            'tools/tests/test_repo_tool.py', '.repo/context-budgets.json',
            'docs/prompts/README.md', 'docs/areas/README.md']
CORE_SKILLS = ('project-bootstrap', 'implement-task', 'review-change', 'research-scout',
               'docs-steward', 'evidence-reporter', 'work-handoff')


def config_errors(root: Path) -> list[str]:
    errors = []
    cfg = load_json(safe_path(root, '.repo/project.json'))
    if not isinstance(cfg, dict):
        return ['project.json must be a JSON object']
    if cfg.get('schema_version') != 2:
        errors.append('project.json schema_version must be 2; see migration guide')
    for field in ('project_name', 'project_kind', 'integration_branch'):
        if not isinstance(cfg.get(field), str) or not cfg[field].strip():
            errors.append(f'project.json: {field} must be a nonempty string')
    commands = cfg.get('commands')
    if not isinstance(commands, dict) or not commands:
        return errors + ['project.json: commands must be a nonempty object']
    for name, command in commands.items():
        if command is None:
            continue
        if not isinstance(command, dict):
            errors.append(f'Command {name}: use argv/cwd/timeout_seconds object, not a shell string')
            continue
        argv = command.get('argv')
        if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and x and '\x00' not in x for x in argv):
            errors.append(f'Command {name}: argv must be a nonempty string array')
        timeout = command.get('timeout_seconds')
        if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 3600:
            errors.append(f'Command {name}: timeout_seconds must be between 1 and 3600')
        try:
            path = safe_path(root, command.get('cwd', '.'))
            if not path.is_dir():
                errors.append(f'Command {name}: cwd does not exist')
        except ValueError as exc:
            errors.append(f'Command {name}: {exc}')
        if command.get('mutates_external', False) is not False:
            errors.append(f'Command {name}: external mutations are not supported by the verification runner')
    areas = load_json(safe_path(root, '.repo/areas.json'))
    if not isinstance(areas, dict) or areas.get('schema_version') != 1 or not isinstance(areas.get('areas'), list):
        return errors + ['areas.json must have schema_version=1 and an areas array']
    ids = set()
    for area in areas['areas']:
        if not isinstance(area, dict):
            errors.append('Area must be an object')
            continue
        ident = area.get('id')
        if not isinstance(ident, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', ident) or ident in ids:
            errors.append(f'Area ID invalid or duplicate: {ident}')
        ids.add(str(ident))
        for field in ('paths', 'checks'):
            if not isinstance(area.get(field), list) or not all(isinstance(v, str) for v in area[field]):
                errors.append(f'Area {ident}: {field} must be a string array')
        guide = area.get('guide', '')
        try:
            if not safe_path(root, guide).is_file():
                errors.append(f'Area {ident}: missing guide {guide}')
        except ValueError as exc:
            errors.append(str(exc))
        if area.get('spec'):
            try:
                if not safe_path(root, area['spec']).is_file():
                    errors.append(f'Area {ident}: missing canonical spec {area["spec"]}')
            except ValueError as exc:
                errors.append(str(exc))
            routes = load_json(safe_path(root, 'docs/context/routes.json')).get('topics', {})
            route = routes.get('area:' + str(ident))
            if not route or not all(any(entry.get('path') == path for entry in route.get('required', []))
                                    for path in (guide, area['spec'])):
                errors.append(f'Area {ident}: missing or incomplete context route')
        for check in area.get('checks', []):
            if check not in commands or check == 'setup':
                errors.append(f'Area {ident}: unknown/non-verification check {check}')
        for pattern in area.get('paths', []):
            if not pattern or pattern.startswith('/') or '..' in pattern.split('/') or '\\' in pattern:
                errors.append(f'Area {ident}: invalid path pattern {pattern}')
    errors += budget_config_errors(root)
    return errors


def agent_errors(root: Path) -> list[str]:
    errors = []
    if '@AGENTS.md' not in text(safe_path(root, 'CLAUDE.md')):
        errors.append('CLAUDE.md must import @AGENTS.md')
    cfg = tomllib.loads(text(safe_path(root, '.codex/config.toml')))
    if cfg.get('approval_policy') == 'never' or cfg.get('sandbox_mode') == 'danger-full-access':
        errors.append('Unsafe shared Codex approval/sandbox default')
    settings = load_json(safe_path(root, '.claude/settings.json'))
    if not isinstance(settings, dict):
        errors.append('Claude settings must be a JSON object')
    for path in sorted(safe_path(root, '.codex/agents').glob('*.toml')):
        data = tomllib.loads(text(safe_path(root, path.relative_to(root).as_posix())))
        for field in ('name', 'description', 'developer_instructions'):
            if not isinstance(data.get(field), str) or not data[field].strip():
                errors.append(f'Codex {path.name}: missing {field}')
    for name in ('research-scout', 'verification-reviewer'):
        fm = frontmatter(text(safe_path(root, f'.claude/agents/{name}.md')))
        match = re.search(r'^tools:\s*(.+)$', fm, re.M)
        permitted = {'Read', 'Grep', 'Glob', 'LSP', 'WebSearch', 'WebFetch'}
        if not match or any(t.strip() not in permitted for t in match.group(1).split(',')):
            errors.append(f'Claude {name}: research/reviewer tool allowlist must exclude shell, writes and MCP')
        if not safe_path(root, f'.codex/agents/{name}.toml').is_file():
            errors.append(f'Missing Codex {name}')
    for name in CORE_SKILLS:
        canonical = safe_path(root, f'.agents/skills/{name}/SKILL.md')
        loader = safe_path(root, f'.claude/skills/{name}/SKILL.md')
        fm = frontmatter(text(canonical))
        if not re.search(rf'^name:\s*{re.escape(name)}\s*$', fm, re.M) or not re.search(r'^description:\s*\S', fm, re.M):
            errors.append(f'Skill {name}: missing name or description')
        if f'.agents/skills/{name}/SKILL.md' not in text(loader):
            errors.append(f'Claude {name}: broken canonical loader')
    for path in safe_path(root, '.claude/rules').rglob('*.md'):
        path = safe_path(root, path.relative_to(root).as_posix())
        if not re.search(r'^paths:', frontmatter(text(path)), re.M):
            errors.append(f'Claude rule must be path-scoped: {path.name}')
    return errors


def doc_errors(root: Path) -> list[str]:
    errors = []
    for name in REQUIRED:
        if not safe_path(root, name).is_file():
            errors.append(f'Missing required file: {name}')
    if errors:
        return errors
    errors += config_errors(root)
    errors += agent_errors(root)
    routes = load_json(safe_path(root, 'docs/context/routes.json'))
    if routes.get('schema_version') != 1:
        errors.append('Unsupported route schema')
    for topic, route in routes.get('topics', {}).items():
        seen = set()
        for tier in ('required', 'optional'):
            for entry in route.get(tier, []):
                rel = entry.get('path', '')
                try:
                    if not safe_path(root, rel).is_file():
                        errors.append(f'Missing route {topic}: {rel}')
                except ValueError as exc:
                    errors.append(str(exc))
                if rel in seen:
                    errors.append(f'Duplicate route {topic}: {rel}')
                seen.add(rel)
                if not entry.get('reason'):
                    errors.append(f'Route {topic}/{rel} lacks a reason')
    cached = {}
    for path in markdown_files(root):
        for raw in links(text(path)):
            parsed = urlsplit(raw)
            if parsed.scheme or parsed.netloc:
                continue
            rel, fragment = unquote(parsed.path), unquote(parsed.fragment)
            if not rel:
                target = path
            else:
                # Links may legitimately go up to a parent, but cannot escape the root.
                candidate = (root / rel.lstrip('/')) if rel.startswith('/') else (path.parent / rel)
                try:
                    norm = candidate.resolve().relative_to(root.resolve()).as_posix()
                    # Detect symlinks in the original path before normalization.
                    cur = root.resolve()
                    raw_parts = candidate.relative_to(root.resolve()).parts
                    for part in raw_parts:
                        cur /= part
                        if cur.is_symlink():
                            raise ValueError('symlink in link target')
                    target = safe_path(root, norm)
                except (ValueError, OSError):
                    errors.append(f'Unsafe local link: {path.relative_to(root)} -> {raw}')
                    continue
            if not target.exists():
                errors.append(f'Broken local link: {path.relative_to(root)} -> {raw}')
            elif fragment and target.is_file() and target.suffix == '.md':
                if target not in cached:
                    cached[target] = anchors(text(target))
                if fragment not in cached[target]:
                    errors.append(f'Broken fragment: {path.relative_to(root)} -> {raw}')
    return errors
