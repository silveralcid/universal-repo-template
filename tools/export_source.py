#!/usr/bin/env python3
"""Export reviewed UTF-8 source with minimized ZIP metadata, not anonymity."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import zipfile

MANIFEST = '.repo/template-manifest.json'
STAMP = (1980, 1, 1, 0, 0, 0)
ROOT_NAME = 'project-starter'
MAX_FILE = 2 * 1024 * 1024
MAX_TOTAL = 20 * 1024 * 1024
PRIVATE_PARTS = {'.git', '.repo-local', '__pycache__', '.ssh', '.aws',
                 '.vscode', '.idea', 'node_modules', '.venv', 'venv',
                 'dist', 'build', '.DS_Store', '__MACOSX'}
EMAIL = re.compile(r'\b[A-Z0-9._%+\-]+@([A-Z0-9.\-]+\.[A-Z]{2,})\b', re.I)
SECRET = re.compile(
    r'-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----|'
    r'\bgh[pousr]_[A-Za-z0-9]{20,}\b|'
    r'\bgithub_pat_[A-Za-z0-9_]{20,}\b|'
    r'\bAKIA[A-Z0-9]{16}\b|'
    r'\bxox[baprs]-[A-Za-z0-9-]{15,}\b|'
    r'\bsk-[A-Za-z0-9_-]{24,}\b')
PERSONAL_PATH = re.compile(
    r'(?:/Users/|/home/|[A-Za-z]:[\\/]Users[\\/])[A-Za-z0-9_.-]+[\\/]')


GITHUB_REPO_LINK = re.compile(
    r'(?:https?://(?:www\.)?github\.com/|git@github\.com:|'
    r'https?://raw\.githubusercontent\.com/|https?://api\.github\.com/repos/)'
    r'(?P<owner>[A-Za-z0-9-]+)/(?P<repo>[A-Za-z0-9_.-]+)', re.I)


def checked_path(root: Path, relative: str) -> Path:
    """Reject ambiguous paths and symlinks before reading any bytes."""
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError('Invalid package path')
    parts = relative.split('/')
    if any(part in {'', '.', '..'} or part in PRIVATE_PARTS for part in parts):
        raise ValueError('Unsafe or private package path')
    if ':' in relative or any(ord(c) < 32 or ord(c) == 127 for c in relative):
        raise ValueError('Unsafe package filename')
    if PurePosixPath(relative).is_absolute():
        raise ValueError('Absolute package path')
    if any(part.startswith('.env') and part != '.env.example' for part in parts):
        raise ValueError('Private environment file')
    if Path(relative).suffix.lower() in {'.pem', '.key', '.p12', '.pfx', '.pyc', '.zip', '.log'}:
        raise ValueError('Private or generated file type')
    current = root
    for part in parts:
        current /= part
        if current.is_symlink():
            raise ValueError('Symlink in package path')
    if not current.is_file() or not current.resolve().is_relative_to(root):
        raise ValueError('Missing or escaped package file')
    if current.stat().st_size > MAX_FILE:
        raise ValueError('Package file exceeds size limit')
    return current


def load_payload(root: Path) -> dict[str, bytes]:
    root = root.resolve(strict=True)
    manifest_bytes = checked_path(root, MANIFEST).read_bytes()
    manifest = json.loads(manifest_bytes)
    entries = manifest.get('files')
    if manifest.get('algorithm') != 'sha256' or not isinstance(entries, dict) or not entries:
        raise ValueError('Expected a nonempty SHA-256 package manifest')
    if MANIFEST in entries:
        raise ValueError('Manifest cannot hash itself')
    payload = {MANIFEST: manifest_bytes}
    folded = {MANIFEST.casefold()}
    for relative, expected in sorted(entries.items()):
        if not isinstance(expected, str) or not re.fullmatch(r'[a-f0-9]{64}', expected):
            raise ValueError('Invalid manifest checksum')
        if relative.casefold() in folded:
            raise ValueError('Duplicate case-insensitive package path')
        folded.add(relative.casefold())
        data = checked_path(root, relative).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('Package manifest does not match reviewed files')
        data.decode('utf-8')
        if b'\0' in data:
            raise ValueError('Binary data is not permitted in this source package')
        payload[relative] = data
    if sum(map(len, payload.values())) > MAX_TOTAL:
        raise ValueError('Package exceeds total size limit')
    return payload


def unreviewed_tracked_count(root: Path, included: set[str]) -> int:
    """Count Git-tracked files omitted from the reviewed package, without printing their paths."""
    result = subprocess.run(['git', 'ls-files', '--cached', '-z'], cwd=root,
                            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tracked = {part.decode('utf-8') for part in result.stdout.split(b'\0') if part}
    return len(tracked - included)


def repo_identity(value: str) -> tuple[str, str]:
    if not re.fullmatch(r'[A-Za-z0-9-]+/[A-Za-z0-9_.-]+', value):
        raise ValueError('Expected a repository identity in owner/name form')
    return tuple(part.casefold() for part in value.split('/', 1))


def findings(payload: dict[str, bytes], terms: tuple[str, ...] = (),
             repository: str | None = None) -> list[str]:
    """Return locations and categories only, never matched private values."""
    issues = []
    owner, current = repo_identity(repository) if repository else ('', '')
    for relative, data in sorted(payload.items()):
        text = data.decode('utf-8')
        combined = (relative + '\n' + text).casefold()
        if any(term.casefold() in combined for term in terms if term.strip()):
            issues.append(f'{relative}: private denylist match')
        for number, line in enumerate(text.splitlines(), 1):
            if owner and any(match.group('owner').casefold() == owner
                             and match.group('repo').removesuffix('.git').casefold() != current
                             for match in GITHUB_REPO_LINK.finditer(line)):
                issues.append(f'{relative}:{number}: link to another repository under the same owner')
            if SECRET.search(line):
                issues.append(f'{relative}:{number}: credential-like content')
            if PERSONAL_PATH.search(line):
                issues.append(f'{relative}:{number}: personal filesystem path')
            for match in EMAIL.finditer(line):
                if match.group(0).casefold() == 'git@github.com' and line[match.end():].startswith(':'):
                    continue  # Git SSH remote syntax, not an email address.
                domain = match.group(1).casefold()
                allowed = domain.endswith(('.invalid', '.example')) or domain in {
                    'example.com', 'example.org', 'example.net'}
                if not allowed:
                    issues.append(f'{relative}:{number}: non-example email address')
    return sorted(set(issues))


def export(payload: dict[str, bytes], output: Path) -> None:
    """Write a new archive only. Source files and existing outputs stay intact."""
    with output.open('xb') as handle:
        with zipfile.ZipFile(handle, 'w', compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as archive:
            archive.comment = b''
            for relative, data in sorted(payload.items()):
                info = zipfile.ZipInfo(f'{ROOT_NAME}/{relative}', STAMP)
                info.create_system = 0
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.extra = b''
                info.comment = b''
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, data, compresslevel=9)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New ZIP path; omit for a read-only check')
    parser.add_argument('--denylist-file', type=Path, help='Private terms file outside the source root')
    parser.add_argument('--repository', default=os.environ.get('GITHUB_REPOSITORY'),
                        help='owner/name to detect links to a different repository under the same owner')
    parser.add_argument('--check-tracked', action='store_true',
                        help='Require all Git-tracked files to be listed in the reviewed manifest')
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        terms: tuple[str, ...] = ()
        if args.denylist_file:
            denylist = args.denylist_file.resolve(strict=True)
            if denylist.is_relative_to(root):
                raise ValueError('The private denylist must be outside the source root')
            terms = tuple(line.strip() for line in denylist.read_text(encoding='utf-8').splitlines()
                          if line.strip() and not line.lstrip().startswith('#'))
        payload = load_payload(root)
        if args.check_tracked:
            omitted = unreviewed_tracked_count(root, set(payload))
            if omitted:
                print(f'BLOCKED: {omitted} Git-tracked files omitted from the reviewed manifest.',
                      file=sys.stderr)
                return 2
        issues = findings(payload, terms, args.repository)
        if issues:
            for issue in issues:
                print('BLOCKED:', issue, file=sys.stderr)
            return 2
        if args.output:
            output = args.output.absolute()
            if output.resolve().is_relative_to(root):
                raise ValueError('Write the archive outside the source root')
            export(payload, output)
        print(f'PASS: {len(payload)} reviewed source files; no configured scan matches.')
        print('LIMIT: identifier and metadata checks do not establish anonymity or scan Git history.')
        return 0
    except (OSError, ValueError, TypeError, UnicodeError, subprocess.CalledProcessError) as exc:
        print(f'BLOCKED: {type(exc).__name__}. Check input paths, manifest, and file contents.',
              file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
