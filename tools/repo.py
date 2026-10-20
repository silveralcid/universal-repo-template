#!/usr/bin/env python3
"""Agent repository helper. Python 3.11+; standard library; no automatic networking."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

if sys.version_info < (3, 11):
    raise SystemExit('Python 3.11+ is required (standard-library TOML validation). Markdown remains usable without Python.')

from repo_support.core import VERSION, safe_path, load_json, dump_json, text, markdown_files, state, git
from repo_support.validation import doc_errors, agent_errors, config_errors
from repo_support.knowledge import context, save_snapshot, compare_snapshot, new_record, inventory, search_records, BUCKETS
from repo_support.workflow import verification_plan, execute_verification, adoption_plan, apply_adoption
ROOT = Path(__file__).resolve().parent.parent


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=VERSION)
    sub = parser.add_subparsers(dest='action', required=True)
    init = sub.add_parser('init', help='Set local metadata; no Git initialization or package installation')
    init.add_argument('--name', required=True)
    init.add_argument('--kind', default='unspecified')
    init.add_argument('--branch', default='auto')
    init.add_argument('--force', action='store_true')
    doctor = sub.add_parser('doctor', help='Inspect local readiness; no network or AI session')
    doctor.add_argument('--strict', action='store_true')
    check = sub.add_parser('check', help='Validate template structure; optionally run template helper tests')
    check.add_argument('--tests', action='store_true')
    docs = sub.add_parser('docs')
    docs.add_argument('mode', choices=('check', 'budget'))
    agents = sub.add_parser('agents')
    agents.add_argument('mode', choices=('check',))
    agents.add_argument('--cli', action='store_true', help='Run only installed client --version commands')
    branch = sub.add_parser('branch')
    branch.add_argument('mode', choices=('check',))
    branch.add_argument('--strict', action='store_true')
    ctx = sub.add_parser('context', help='List task-relevant paths without dumping their bodies')
    ctx.add_argument('mode', nargs='?', choices=('list', 'diff'))
    ctx.add_argument('--topic', default='implementation')
    ctx.add_argument('--include-optional', action='store_true')
    ctx.add_argument('--format', choices=('text', 'json'), default='text')
    ctx.add_argument('--snapshot', help='Write new snapshot under .repo-local/; diff reads this path')
    new = sub.add_parser('new', help='Create blank dated record, never fabricated evidence')
    new.add_argument('kind', choices=tuple(BUCKETS))
    new.add_argument('--slug', required=True)
    new.add_argument('--bucket')
    cat = sub.add_parser('catalog', help='Derived index of sanitized documentation records')
    cat.add_argument('mode', choices=('build', 'check'), default='build', nargs='?')
    cat.add_argument('--write', action='store_true', help='Write ignored .repo-local/catalog.json')
    search = sub.add_parser('search', help='Search authored research/evidence/decision records only')
    search.add_argument('query')
    search.add_argument('--kind')
    search.add_argument('--limit', type=int, default=20)
    verify = sub.add_parser('verify', help='Plan or explicitly execute configured application checks')
    verify.add_argument('mode', choices=('plan', 'run'))
    verify.add_argument('--name', action='append', help='Specific command name; repeat for several')
    verify.add_argument('--path', action='append', help='Changed path for registered area selection')
    verify.add_argument('--execute', action='store_true', help='Required before any configured command executes')
    adopt = sub.add_parser('adopt', help='Dry-run additive adoption; conflicting files are never overwritten')
    adopt.add_argument('--into', required=True)
    adopt.add_argument('--apply', action='store_true')
    sub.add_parser('hygiene', help='Check tracked path names for common sensitive files; not a secret scanner')
    return parser.parse_args()


def report_errors(errors, label):
    for error in errors:
        print('FAIL:', error)
    print(f'{label}: {"FAIL" if errors else "PASS"}')
    return 1 if errors else 0


def main():
    args = parse_args()
    try:
        if args.action == 'init':
            cfg = load_json(safe_path(ROOT, '.repo/project.json'))
            if cfg['project_name'] != 'REPLACE_ME' and not args.force:
                raise ValueError('Already initialized; --force replaces metadata only')
            if not args.name.strip() or any(c in args.branch for c in '\n\r\t '):
                raise ValueError('Provide a name and a branch without whitespace')
            cfg.update(project_name=args.name.strip(), project_kind=args.kind, integration_branch=args.branch)
            dump_json(safe_path(ROOT, '.repo/project.json'), cfg)
            print('Metadata initialized. Follow START-HERE.md; application setup is not installed.')
        elif args.action == 'doctor':
            cfg = load_json(safe_path(ROOT, '.repo/project.json'))
            result = dict(template_version=VERSION, python=sys.version.split()[0], git=state(ROOT, cfg),
                          project_name=cfg['project_name'],
                          unset_commands=[k for k, v in cfg['commands'].items() if v is None],
                          native_clients={name: 'ON_PATH_NOT_SMOKE_TESTED' if shutil.which(name) else 'NOT_ON_PATH'
                                          for name in ('codex', 'claude')},
                          application_readiness='NOT_PROVEN; fill brief and run stack checks',
                          template_errors=config_errors(ROOT))
            emit(result)
            return 2 if args.strict and (result['template_errors'] or cfg['project_name'] == 'REPLACE_ME'
                                          or result['unset_commands']) else 0
        elif args.action == 'check' or args.action == 'docs' and args.mode == 'check':
            result = report_errors(doc_errors(ROOT), 'Template static checks')
            print('Checks: common local links/fragments, routes, config structure, provider adapters. Not native discovery, semantics, runtime tests or CI proof.')
            if result:
                return result
            if args.action == 'check' and args.tests:
                return subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tools/tests', '-v'], cwd=ROOT, check=False).returncode
        elif args.action == 'docs':
            counts = sorted(((len(text(p)) + 3) // 4, p.relative_to(ROOT).as_posix()) for p in markdown_files(ROOT))
            emit(dict(largest=list(reversed(counts[-15:])), total_estimated_tokens=sum(n for n, _ in counts),
                      note='chars/4 estimate, not tokenization; scan restricted to docs and agent roots'))
        elif args.action == 'agents':
            code = report_errors(agent_errors(ROOT), 'Agent static configuration checks')
            for binary in ('codex', 'claude'):
                path = shutil.which(binary)
                if args.cli and path:
                    try:
                        result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=10, check=False)
                        print(f'{binary}: {"VERSION_OK" if result.returncode == 0 else "VERSION_FAILED"}; {(result.stdout or result.stderr).strip()[:300]}')
                        code = max(code, int(result.returncode != 0))
                    except (OSError, subprocess.TimeoutExpired):
                        print(f'{binary}: VERSION_FAILED')
                        code = 1
                else:
                    print(f'{binary}: {"VERSION_NOT_RUN" if path else "NOT_ON_PATH"}')
            print('Native discovery/permissions: NOT_TESTED. Follow docs/agents/agent-setup-validation.md.')
            return code
        elif args.action == 'branch':
            status = state(ROOT)
            emit(status)
            print('No fetch, PR lookup or remote freshness claim. Dirty working files are not changed.')
            return 2 if args.strict and (not status['head'] or not status['branch'] or not status['integration_branch']
                                         or 'ahead' not in status or 'behind' not in status
                                         or status['branch'] == status['integration_branch']
                                         or status['working_tree'] != 'CLEAN' or status.get('behind', 0)) else 0
        elif args.action == 'context':
            if args.mode == 'list':
                emit(sorted(load_json(safe_path(ROOT, 'docs/context/routes.json'))['topics']))
            elif args.mode == 'diff':
                if not args.snapshot:
                    raise ValueError('context diff requires --snapshot')
                emit(compare_snapshot(ROOT, args.snapshot))
            else:
                pack = context(ROOT, args.topic, args.include_optional)
                if args.format == 'json':
                    emit(pack)
                else:
                    print(f'Topic {pack["topic"]}: ~{pack["estimated_tokens"]} tokens (chars/4); budget {pack["budget_tokens"]}')
                    for item in pack['files']:
                        print(f'{item["tier"]}: {item["path"]} — {item["reason"]}')
                    print('Read only relevant sections. No document bodies were concatenated.')
                if args.snapshot:
                    save_snapshot(ROOT, pack, args.snapshot)
                    print('Saved content-hash snapshot:', args.snapshot)
        elif args.action == 'new':
            path = new_record(ROOT, args.kind, args.slug, args.bucket)
            print('Created blank record:', path.relative_to(ROOT))
            print('Not evidence of execution, approval, or completion. Fill truthfully.')
        elif args.action == 'catalog':
            data = inventory(ROOT)
            path = safe_path(ROOT, '.repo-local/catalog.json')
            if args.mode == 'check':
                if not path.exists():
                    print('NOT_BUILT: run catalog build --write')
                    return 2
                if load_json(path) != data:
                    print('STALE: run catalog build --write')
                    return 1
                print('Catalog matches current record files; no semantic validity claim.')
            elif args.write:
                dump_json(path, data)
                print(f'Indexed {len(data["records"])} records in ignored .repo-local/catalog.json')
            else:
                emit(data)
        elif args.action == 'search':
            if not 1 <= args.limit <= 100:
                raise ValueError('limit must be 1-100')
            emit(search_records(ROOT, args.query, args.kind, args.limit))
        elif args.action == 'verify':
            plan = verification_plan(ROOT, args.name, args.path)
            if args.mode == 'plan':
                emit(plan)
            elif not args.execute:
                emit(plan)
                print('NOT_EXECUTED: add --execute after inspecting configured argv. No checks ran.')
                return 2
            else:
                receipt, code, path = execute_verification(ROOT, plan)
                # Do not print raw command output: it may contain private data.
                emit(dict(overall=receipt['overall'], checks=[{'name': r['name'], 'status': r['status']}
                                                              for r in receipt['checks']],
                          local_receipt=path.relative_to(ROOT).as_posix()))
                return code
        elif args.action == 'adopt':
            plan = adoption_plan(ROOT, Path(args.into))
            emit(plan)
            if args.apply:
                print('Copied missing files:', apply_adoption(ROOT, plan))
            return 1 if plan['conflicts'] else 0
        elif args.action == 'hygiene':
            tracked = git(ROOT, 'ls-files', '-z')
            if tracked is None:
                print('NOT_AVAILABLE: Git checkout required. No secret scan performed.')
                return 2
            suspects = []
            for name in tracked.split('\0'):
                if not name:
                    continue
                base = Path(name).name
                if (base.startswith('.env') and base != '.env.example') or base in {'auth.json', 'id_rsa', 'id_ed25519'} or name.startswith(('secrets/', '.repo-local/')):
                    suspects.append(name)
            emit(dict(suspicious_tracked_paths=suspects,
                      limitation='Filename-only heuristic. Does not inspect contents/history or replace a secret scanner.'))
            return 1 if suspects else 0
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('ERROR:', str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
