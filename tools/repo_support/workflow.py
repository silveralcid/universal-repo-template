"""Explicit verification and conflict-aware template adoption."""
from __future__ import annotations
from pathlib import Path
import fnmatch
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from .core import safe_path, load_json, dump_json, state, now, sha
from .validation import config_errors


def verification_plan(root: Path, names=None, changed=None) -> dict:
    problems = config_errors(root)
    if problems:
        raise ValueError('; '.join(problems))
    cfg = load_json(safe_path(root, '.repo/project.json'))
    commands = cfg['commands']
    selected = list(names or [])
    reason = 'explicit command selection' if selected else 'all configured check slots; setup excluded'
    unknown = []
    if changed and not selected:
        areas = load_json(safe_path(root, '.repo/areas.json'))['areas']
        for path in changed:
            safe_path(root, path)
            matches = [area for area in areas if any(fnmatch.fnmatchcase(path, glob) for glob in area['paths'])]
            if not matches:
                unknown.append(path)
            for area in matches:
                selected.extend(area['checks'])
        reason = 'registered path areas (fnmatch; * can cross /)' if not unknown else 'unmapped paths: conservative all-check fallback'
    if not selected or unknown:
        selected = [name for name in commands if name != 'setup']
    selected = list(dict.fromkeys(selected))
    for name in selected:
        if name not in commands:
            raise ValueError(f'Unknown command: {name}')
        if name == 'setup':
            raise ValueError('Setup may install dependencies; inspect and run it separately, not as verification')
    checks = [dict(name=name, status='PLANNED' if commands[name] else 'NOT_CONFIGURED',
                   command=commands[name]) for name in selected]
    return dict(schema_version=1, selection_reason=reason, unmapped_paths=unknown, checks=checks,
                coverage_claim='Selection only. Registered mappings require human review; not proof of complete coverage.')


def execute_verification(root: Path, plan: dict) -> tuple[dict, int, Path]:
    """Only caller's --execute flag invokes this. Config is trusted executable input."""
    run_id = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '-' + uuid.uuid4().hex[:8]
    output = safe_path(root, '.repo-local/runs/' + run_id)
    output.mkdir(parents=True, exist_ok=False)
    receipt = dict(schema_version=1, started_at=now(), source_before=state(root), checks=[],
                   limitation='No security sandbox; argv avoids implicit shell parsing, not malicious executables. Raw logs may contain secrets; never publish unreviewed.')
    failed, incomplete = False, False
    for number, planned in enumerate(plan['checks'], 1):
        record = dict(planned)
        command = record['command']
        if command is None:
            incomplete = True
            receipt['checks'].append(record)
            continue
        argv = list(command['argv'])
        argv = [sys.executable if arg == '{python}' else arg for arg in argv]
        # Explicit executable selection: no interpolation, shell pipelines or automatic installs.
        cwd = safe_path(root, command.get('cwd', '.'))
        logfile = output / f'{number:02d}.log'
        started = time.monotonic()
        record['started_at'] = now()
        record['argv'] = argv
        try:
            with logfile.open('wb') as log:
                process = subprocess.Popen(argv, cwd=cwd, stdout=log, stderr=subprocess.STDOUT,
                                           shell=False, start_new_session=(os.name != 'nt'))
                try:
                    code = process.wait(timeout=command['timeout_seconds'])
                    record.update(exit_code=code, status='PASS' if code == 0 else 'FAIL')
                    failed |= code != 0
                except subprocess.TimeoutExpired:
                    # POSIX stops the process group. Windows can only guarantee direct-child termination.
                    if os.name != 'nt':
                        import signal
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    else:
                        process.kill()
                    process.wait()
                    record.update(status='BLOCKED', reason='TIMEOUT; inspect child processes on Windows', exit_code=None)
                    failed = True
        except OSError as exc:
            record.update(status='BLOCKED', reason=str(exc), exit_code=None)
            failed = True
        record.update(duration_seconds=round(time.monotonic() - started, 3),
                      log_path=logfile.relative_to(root).as_posix(),
                      log_sha256=sha(logfile) if logfile.is_file() else None)
        receipt['checks'].append(record)
    receipt.update(finished_at=now(), source_after=state(root),
                   overall='FAIL_OR_BLOCKED' if failed else 'INCOMPLETE' if incomplete else 'PASS')
    dump_json(output / 'receipt.json', receipt)
    return receipt, 1 if failed else 2 if incomplete else 0, output / 'receipt.json'


def adoption_plan(root: Path, destination: Path) -> dict:
    if destination.is_symlink():
        raise ValueError('Destination must not be a symlink')
    destination = destination.absolute()
    for ancestor in (destination, *destination.parents):
        if ancestor.is_symlink():
            raise ValueError('Destination ancestry contains a symlink')
    destination = destination.resolve()
    if not destination.is_dir():
        raise ValueError('Destination must be an existing directory')
    if destination == root.resolve() or destination.is_relative_to(root.resolve()) or root.resolve().is_relative_to(destination):
        raise ValueError('Source and destination cannot contain one another')
    manifest = load_json(safe_path(root, '.repo/template-manifest.json'))
    files = []
    for rel, expected in manifest['files'].items():
        source = safe_path(root, rel)
        target = safe_path(destination, rel)
        if not source.is_file() or sha(source) != expected:
            raise ValueError(f'Template source modified: {rel}; use a pristine bundle for adoption')
        if target.exists() and not target.is_file():
            status = 'CONFLICT'
        elif target.is_file():
            status = 'SAME' if sha(target) == expected else 'CONFLICT'
        else:
            status = 'ADD'
        files.append(dict(path=rel, status=status, sha256=expected))
    return dict(destination=str(destination), files=files,
                conflicts=sum(x['status'] == 'CONFLICT' for x in files),
                note='Dry-run. Conflicts require manual reconciliation; no automatic overwrite or deletion.')


def apply_adoption(root: Path, plan: dict) -> int:
    if plan['conflicts']:
        raise ValueError('Adoption blocked: conflicts exist; no files copied')
    # Recheck immediately before writes, not just against a stale earlier plan.
    current = adoption_plan(root, Path(plan['destination']))
    if current != plan:
        raise ValueError('Destination changed after plan; rerun the dry-run')
    copied = 0
    for item in current['files']:
        if item['status'] != 'ADD':
            continue
        source = safe_path(root, item['path'])
        target = safe_path(Path(plan['destination']), item['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(source.read_bytes())
        copied += 1
    # Manifest itself is transport bookkeeping, not included in its own hash table.
    target = safe_path(Path(plan['destination']), '.repo/template-manifest.json')
    if not target.exists():
        with target.open('xb') as handle:
            handle.write(safe_path(root, '.repo/template-manifest.json').read_bytes())
    return copied
