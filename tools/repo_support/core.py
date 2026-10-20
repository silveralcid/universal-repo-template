"""Bounded file access, configuration and read-only Git helpers."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import subprocess
from datetime import datetime, timezone

VERSION = '4.0.0'
ROOT_DOCS = ('README.md', 'START-HERE.md', 'AGENTS.md', 'CLAUDE.md', 'PLANS.md',
             'CONTRIBUTING.md', 'SECURITY.md', 'CHANGELOG.md')
DOC_ROOTS = ('docs', '.agents', '.claude', '.codex', '.repo')
PRUNE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'artifacts',
         '.repo-local', '.context-out', 'build', 'dist', '.cache'}
MAX_TEXT_BYTES = 2_000_000


def safe_path(root: Path, relative: str) -> Path:
    """Resolve an in-repository path; refuse escapes and symlink traversal."""
    if not isinstance(relative, str) or not relative or '\x00' in relative:
        raise ValueError('Path must be a nonempty string')
    if '\\' in relative or PureWindowsPath(relative).drive or Path(relative).is_absolute():
        raise ValueError(f'Use a repository-relative forward-slash path: {relative!r}')
    if '..' in Path(relative).parts:
        raise ValueError(f'Parent traversal is not allowed: {relative!r}')
    root = root.resolve()
    candidate = root / relative
    current = root
    for part in Path(relative).parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f'Symlink path is not supported: {relative}')
    if not candidate.resolve().is_relative_to(root):
        raise ValueError(f'Path leaves repository: {relative}')
    return candidate


def text(path: Path) -> str:
    if path.stat().st_size > MAX_TEXT_BYTES:
        raise ValueError(f'Text file exceeds {MAX_TEXT_BYTES} byte inspection limit: {path.name}')
    return path.read_text(encoding='utf-8-sig')


def load_json(path: Path):
    return json.loads(text(path))


def dump_json(path: Path, data, *, exclusive=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x' if exclusive else 'w', encoding='utf-8', newline='\n') as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(65536), b''):
            digest.update(chunk)
    return digest.hexdigest()


def git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=10, check=False,
                                env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'})
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def state(root: Path, cfg=None):
    cfg = cfg or load_json(safe_path(root, '.repo/project.json'))
    base = cfg.get('integration_branch', 'auto')
    source = 'configured'
    if base in (None, '', 'auto'):
        remote = git(root, 'symbolic-ref', '--quiet', '--short', 'refs/remotes/origin/HEAD')
        base = remote[7:] if remote and remote.startswith('origin/') else None
        source = 'cached origin/HEAD' if base else 'unresolved'
    status = git(root, 'status', '--porcelain=v1', '--untracked-files=normal')
    result = dict(head=git(root, 'rev-parse', '--verify', 'HEAD'),
                  branch=git(root, 'branch', '--show-current'), integration_branch=base,
                  integration_source=source,
                  working_tree='UNKNOWN' if status is None else 'DIRTY' if status else 'CLEAN',
                  status_sha256=hashlib.sha256(status.encode()).hexdigest() if status is not None else None,
                  remote_freshness='NOT_VERIFIED', pr_state='NOT_VERIFIED')
    if base:
        counts = git(root, 'rev-list', '--left-right', '--count', f'HEAD...refs/remotes/origin/{base}')
        if counts and re.fullmatch(r'\d+\s+\d+', counts):
            result['ahead'], result['behind'] = map(int, counts.split())
    return result


def markdown_files(root: Path):
    """Only documentation and agent roots; never scan application/vendor trees."""
    found = []
    for name in ROOT_DOCS:
        path = safe_path(root, name)
        if path.is_file():
            found.append(path)
    for name in DOC_ROOTS:
        folder = safe_path(root, name)
        if not folder.is_dir():
            continue
        for here, dirs, files in os.walk(folder, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in PRUNE and not (Path(here) / d).is_symlink())
            for filename in sorted(files):
                path = Path(here) / filename
                if filename.endswith('.md') and not path.is_symlink():
                    found.append(path)
    return sorted(set(found))


def strip_fences(data: str) -> str:
    lines, marker, length = [], None, 0
    for line in data.splitlines():
        match = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
        if match:
            run, rest = match.groups()
            if marker is None:
                marker, length = run[0], len(run)
                lines.append('')
                continue
            if run[0] == marker and len(run) >= length and not rest.strip():
                marker = None
                lines.append('')
                continue
        lines.append(line if marker is None else '')
    return '\n'.join(lines)


def slugify_heading(value: str) -> str:
    value = re.sub(r'<[^>]*>', '', value)
    value = value.lower().replace('`', '').replace('*', '').replace('~', '')
    return re.sub(r'[^\w\-\s]', '', value, flags=re.UNICODE).strip().replace(' ', '-')


def anchors(data: str) -> set[str]:
    """Common GitHub ATX headings + explicit HTML ids; not a complete renderer."""
    clean = strip_fences(data)
    result = set(re.findall(r'<(?:a|span|div|h[1-6])\b[^>]*\bid=[\"\']([^\"\']+)', clean))
    seen = {}
    for line in clean.splitlines():
        match = re.match(r'^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$', line)
        if not match:
            continue
        key = slugify_heading(match.group(1))
        count = seen.get(key, 0)
        seen[key] = count + 1
        result.add(f'{key}-{count}' if count else key)
    return result


def links(data: str):
    """Common inline and reference links, including images, outside fenced code."""
    clean = strip_fences(data)
    for match in re.finditer(r'!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+[\"\'][^\n]*?[\"\'])?\)', clean):
        yield match.group(1).strip('<>')
    for match in re.finditer(r'^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)', clean, re.M):
        yield match.group(1).strip('<>')


def frontmatter(data: str) -> str:
    if not data.startswith('---\n') or '\n---' not in data[4:]:
        raise ValueError('Expected YAML frontmatter delimited by ---')
    return data.split('---', 2)[1]
