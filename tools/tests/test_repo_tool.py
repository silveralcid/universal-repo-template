"""Infrastructure tests. Synthetic fixtures never copy or execute application code."""
from __future__ import annotations
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from repo_support import core, validation, knowledge, workflow


class TemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = ROOT

    def test_pristine_static_checks(self):
        self.assertEqual(validation.doc_errors(self.root), [])

    def test_all_context_routes_resolve(self):
        for topic in core.load_json(self.root / 'docs/context/routes.json')['topics']:
            packet = knowledge.context(self.root, topic, True)
            self.assertTrue(packet['files'])
            self.assertEqual(len(packet['files']), len({x['path'] for x in packet['files']}))

    def test_seven_canonical_skills_and_loaders(self):
        self.assertEqual(len(validation.CORE_SKILLS), 7)
        self.assertEqual(validation.agent_errors(self.root), [])

    def test_template_checks_do_not_require_an_application_layout(self):
        for name in ('package.json', 'pyproject.toml', 'Cargo.toml', 'src', 'apps', 'packages'):
            self.assertNotIn(name, validation.REQUIRED)
        # These tests must keep working once real project code and commands exist.
        self.assertEqual(core.load_json(self.root / '.repo/project.json')['schema_version'], 2)

    def test_ready_path_and_honesty_contract(self):
        entry = core.text(self.root / 'START-HERE.md')
        self.assertIn('Do not stop after planning', entry)
        self.assertIn('NOT CONFIGURED', core.text(self.root / 'docs/agents/definition-of-done.md'))
        self.assertIn('not a delivered user feature', core.text(self.root / 'docs/agents/definition-of-done.md'))

    def test_security_specialists_do_not_have_shell_or_writes(self):
        for name in ('research-scout', 'verification-reviewer'):
            fm = core.frontmatter(core.text(self.root / f'.claude/agents/{name}.md'))
            self.assertNotIn('Bash', fm)
            self.assertNotIn('Write', fm)
            self.assertNotIn('mcp__', fm)

    def test_root_agents_remains_compact(self):
        self.assertLess(len(core.text(self.root / 'AGENTS.md')), 6500)
        self.assertLess(len(core.text(self.root / 'CLAUDE.md')), 1500)

    def test_common_markdown_fragment_parser(self):
        source = '# A heading\n## Repeat\n## Repeat\n<a id="stable-id"></a>\n```md\n# Ignore\n```\n'
        self.assertEqual(core.anchors(source), {'a-heading', 'repeat', 'repeat-1', 'stable-id'})

    def test_reference_and_inline_links_outside_fences(self):
        source = '[a](docs/a.md#one)\n![img](img.png)\n[b]: docs/b.md\n```\n[x](bad)\n```'
        self.assertEqual(list(core.links(source)), ['docs/a.md#one', 'img.png', 'docs/b.md'])

    def test_fence_lengths_are_respected(self):
        source = '````\n```\n[hidden](missing.md)\n````\n[shown](README.md)'
        self.assertEqual(list(core.links(source)), ['README.md'])


    def test_ci_invokes_current_nonempty_infrastructure_suite(self):
        content = core.text(self.root / '.github/workflows/repo-health.yml')
        self.assertIn('python3 tools/repo.py check --tests', content)
        self.assertNotIn('discover -s tests', content)
        self.assertIn('contents: read', content)
        self.assertIn('persist-credentials: false', content)
        self.assertIn('timeout-minutes:', content)
        self.assertNotIn('pull_request_target:', content)
        self.assertNotIn('secrets.', content)
        self.assertRegex(content, r'uses: actions/checkout@[a-f0-9]{40}')


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.root = self.base / 'project'
        self.root.mkdir()
        # Copy only the helper under test. Do not clone the user's application,
        # dependencies, private docs, configured commands, data or build outputs.
        helper_files = [ROOT / 'tools/repo.py', ROOT / 'tools/tests/test_repo_tool.py']
        helper_files += sorted((ROOT / 'tools/repo_support').glob('*.py'))
        for source in helper_files:
            target = self.root / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        for name in validation.REQUIRED:
            if not (self.root / name).exists():
                self.write(name, '# Synthetic test fixture\n')
        self.write('README.md', '# Fixture template\nPython 3.11; infrastructure tests in tools/tests.\n')
        self.write('CLAUDE.md', '@AGENTS.md\n')
        self.write('.gitignore', '__pycache__/\n*.pyc\n.repo-local/\n.env\n')
        core.dump_json(self.root / '.repo/project.json', {
            'schema_version': 2, 'project_name': 'REPLACE_ME', 'project_kind': 'unspecified',
            'integration_branch': 'auto', 'release_branch': None,
            'commands': {name: None for name in
                         ('setup', 'format_check', 'lint', 'typecheck', 'test', 'build', 'smoke', 'security')}})
        core.dump_json(self.root / '.repo/areas.json', {'schema_version': 1, 'areas': []})
        self.write('.codex/config.toml', '[agents]\nmax_concurrent_threads_per_session = 3\n')
        self.write('.claude/settings.json', '{}\n')
        for name in ('research-scout', 'verification-reviewer'):
            self.write('.codex/agents/' + name + '.toml',
                       'name = "' + name + '"\ndescription = "Fixture"\ndeveloper_instructions = "Fixture"\n')
            self.write('.claude/agents/' + name + '.md',
                       '---\nname: ' + name + '\ndescription: Fixture\ntools: Read, Grep, Glob\n---\n')
        self.write('.claude/rules/documentation.md', '---\npaths: ["docs/**"]\n---\n# Fixture rule\n')
        for name in validation.CORE_SKILLS:
            self.write('.agents/skills/' + name + '/SKILL.md',
                       '---\nname: ' + name + '\ndescription: Synthetic fixture\n---\n# Fixture\n')
            self.write('.claude/skills/' + name + '/SKILL.md',
                       '[Canonical](../../../.agents/skills/' + name + '/SKILL.md)\n')
        self.write('docs/agents/delivery.md', '# Synthetic delivery fixture\n')
        core.dump_json(self.root / 'docs/context/routes.json', {
            'schema_version': 1, 'topics': {'implementation': {
                'required': [{'path': name, 'reason': 'Synthetic dependency'} for name in (
                    'docs/agents/delivery.md', 'docs/agents/definition-of-done.md',
                    'docs/engineering/VERIFICATION.md')], 'optional': [], 'budget_tokens': 1000}}})
        template_names = {entry[3] for entry in knowledge.BUCKETS.values()}
        template_names.update(('test-report.md', 'benchmark-report.md', 'agent-eval.md'))
        for name in template_names:
            self.write('docs/templates/' + name, '# <topic>\n**Date:** <date>\n**Status:** NOT RUN\n')

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, data):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding='utf-8')
        return path

    def command(self, argv, name='test', timeout=10):
        path = self.root / '.repo/project.json'
        cfg = core.load_json(path)
        cfg['commands'][name] = {'argv': argv, 'cwd': '.', 'timeout_seconds': timeout, 'mutates_external': False}
        core.dump_json(path, cfg)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(self.root/'tools/repo.py'), *args], cwd=self.root,
                              text=True, capture_output=True, timeout=25, check=False)

    def manifest(self):
        files = {}
        for path in sorted(self.root.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and '.repo-local' not in path.parts:
                rel = path.relative_to(self.root).as_posix()
                if rel != '.repo/template-manifest.json':
                    files[rel] = core.sha(path)
        core.dump_json(self.root / '.repo/template-manifest.json', {'template_version':'4.0.0','files':files})

    def test_path_traversal_and_windows_absolute_refused(self):
        for path in ('../outside', '/outside', 'C:/outside', r'C:\outside', 'docs/../../x', ''):
            with self.subTest(path=path), self.assertRaises(ValueError):
                core.safe_path(self.root, path)

    def test_symlink_targets_refused(self):
        link = self.root / 'docs/link'
        try:
            link.symlink_to(self.base, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable to test account')
        with self.assertRaises(ValueError):
            core.safe_path(self.root, 'docs/link/private.md')

    def test_scanner_does_not_read_dependencies_or_raw_artifacts(self):
        self.write('node_modules/p/README.md', '[bad](MISSING)')
        self.write('artifacts/report.md', '[bad](MISSING)')
        self.write('.repo-local/private.md', '[bad](MISSING)')
        self.assertEqual(validation.doc_errors(self.root), [])

    def test_broken_file_target_detected(self):
        self.write('docs/bad.md', '[missing](does-not-exist.md)')
        self.assertTrue(any('Broken local link' in x for x in validation.doc_errors(self.root)))

    def test_broken_fragment_detected(self):
        self.write('docs/bad.md', '[missing](../README.md#not-a-heading)')
        self.assertTrue(any('Broken fragment' in x for x in validation.doc_errors(self.root)))

    def test_link_escaping_repository_detected(self):
        self.write('docs/bad.md', '[outside](../../outside.md)')
        self.assertTrue(any('Unsafe local link' in x for x in validation.doc_errors(self.root)))

    def test_malformed_toml_is_not_a_silent_pass(self):
        self.write('.codex/config.toml', '[agents\n')
        result = self.cli('agents', 'check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ERROR:', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_missing_skill_fails(self):
        (self.root/'.agents/skills/implement-task/SKILL.md').unlink()
        self.assertNotEqual(self.cli('agents','check').returncode, 0)

    def test_non_scoped_claude_rule_rejected(self):
        self.write('.claude/rules/unsafe.md', '---\nname: all\n---\nRead all files')
        self.assertTrue(any('path-scoped' in e for e in validation.agent_errors(self.root)))

    def test_duplicate_context_route_rejected(self):
        path=self.root/'docs/context/routes.json'
        data=core.load_json(path)
        data['topics']['implementation']['optional']=[data['topics']['implementation']['required'][0]]
        core.dump_json(path,data)
        self.assertTrue(any('Duplicate route' in e for e in validation.doc_errors(self.root)))

    def test_context_only_routes_not_bodies(self):
        packet=knowledge.context(self.root,'implementation')
        self.assertFalse(any('content' in x for x in packet['files']))
        self.assertIn('sha256',packet['files'][0])

    def test_unknown_context_topic_errors(self):
        self.assertEqual(self.cli('context','--topic','no-such-topic').returncode,2)

    def test_snapshot_drift_and_exclusive_creation(self):
        packet=knowledge.context(self.root,'implementation')
        knowledge.save_snapshot(self.root,packet,'.repo-local/a.json')
        with self.assertRaises(FileExistsError):
            knowledge.save_snapshot(self.root,packet,'.repo-local/a.json')
        path=self.root/'docs/agents/definition-of-done.md'
        path.write_text(path.read_text()+'\nChanged test source.\n')
        report=knowledge.compare_snapshot(self.root,'.repo-local/a.json')
        self.assertIn('docs/agents/definition-of-done.md',report['changed'])

    def test_snapshot_rejects_tracked_output_location(self):
        with self.assertRaises(ValueError):
            knowledge.save_snapshot(self.root,knowledge.context(self.root,'implementation'),'docs/snapshot.json')

    def test_snapshot_reports_missing_consumed_file(self):
        knowledge.save_snapshot(self.root,knowledge.context(self.root,'implementation'),'.repo-local/a.json')
        (self.root/'docs/agents/definition-of-done.md').unlink()
        result=knowledge.compare_snapshot(self.root,'.repo-local/a.json')
        self.assertIn('docs/agents/definition-of-done.md',result['missing'])

    def test_snapshot_detects_new_route(self):
        knowledge.save_snapshot(self.root,knowledge.context(self.root,'implementation'),'.repo-local/a.json')
        path=self.root/'docs/context/routes.json';data=core.load_json(path)
        data['topics']['implementation']['required'].append({'path':'docs/project/BRIEF.md','reason':'new dependency'})
        core.dump_json(path,data)
        result=knowledge.compare_snapshot(self.root,'.repo-local/a.json')
        self.assertIn('docs/project/BRIEF.md',result['newly_routed'])

    def test_blank_record_does_not_claim_execution(self):
        path=knowledge.new_record(self.root,'evidence','sample','tests')
        self.assertIn('NOT RUN',core.text(path))
        with self.assertRaises(FileExistsError):
            knowledge.new_record(self.root,'evidence','sample','tests')

    def test_scaffold_rejects_bad_slug_and_bucket(self):
        for slug,bucket in [('../escape','tests'),('a/b','tests'),('valid','invalid')]:
            with self.assertRaises(ValueError):
                knowledge.new_record(self.root,'evidence',slug,bucket)

    def test_all_record_kinds_create(self):
        for kind in knowledge.BUCKETS:
            path=knowledge.new_record(self.root,kind,'new-'+kind)
            self.assertTrue(path.is_file())

    def test_catalog_and_search_current_sources(self):
        path=knowledge.new_record(self.root,'research','queue-design')
        path.write_text(path.read_text()+'\nLatency disconfirmation evidence.\n')
        results=knowledge.search_records(self.root,'latency','research')
        self.assertEqual(len(results),1)
        self.assertEqual(results[0]['authority'],'NOT_INFERRED')
        self.assertTrue(results[0]['matches'])

    def test_catalog_cache_detects_drift(self):
        self.assertEqual(self.cli('catalog','check').returncode,2)
        self.assertEqual(self.cli('catalog','build','--write').returncode,0)
        self.assertEqual(self.cli('catalog','check').returncode,0)
        knowledge.new_record(self.root,'research','new-finding')
        self.assertEqual(self.cli('catalog','check').returncode,1)

    def test_unknown_changed_path_falls_back(self):
        plan=workflow.verification_plan(self.root,changed=['unknown/new-file.ts'])
        self.assertTrue(plan['unmapped_paths'])
        self.assertEqual(len(plan['checks']),7)
        self.assertTrue(all(x['status']=='NOT_CONFIGURED' for x in plan['checks']))

    def test_area_mapping_selects_named_checks(self):
        self.command(['{python}','-c','pass'])
        self.write('docs/agents/areas/demo.md','# Demo\n')
        core.dump_json(self.root/'.repo/areas.json',{'schema_version':1,'areas':[{
            'id':'demo','guide':'docs/agents/areas/demo.md','paths':['src/*'],'checks':['test']}]})
        plan=workflow.verification_plan(self.root,changed=['src/deep/module.py'])
        self.assertEqual([x['name'] for x in plan['checks']],['test'])

    def test_setup_never_runs_in_verification(self):
        with self.assertRaises(ValueError):
            workflow.verification_plan(self.root,names=['setup'])

    def test_external_mutation_declaration_rejected(self):
        self.command(['{python}','-c','pass'])
        path=self.root/'.repo/project.json';data=core.load_json(path)
        data['commands']['test']['mutates_external']=True;core.dump_json(path,data)
        self.assertTrue(validation.config_errors(self.root))

    def test_shell_string_rejected(self):
        path=self.root/'.repo/project.json';data=core.load_json(path)
        data['commands']['test']='npm test && curl example.com';core.dump_json(path,data)
        self.assertTrue(any('not a shell string' in e for e in validation.config_errors(self.root)))

    def test_invalid_timeout_and_escaping_cwd_rejected(self):
        self.command(['{python}','-c','pass'])
        path=self.root/'.repo/project.json';data=core.load_json(path)
        data['commands']['test'].update(timeout_seconds=0,cwd='../escape');core.dump_json(path,data)
        self.assertGreaterEqual(len(validation.config_errors(self.root)),2)

    def test_verify_requires_execute_and_does_not_run(self):
        self.command(['{python}','-c','from pathlib import Path; Path("SENTINEL").write_text("x")'])
        result=self.cli('verify','run','--name','test')
        self.assertEqual(result.returncode,2)
        self.assertFalse((self.root/'SENTINEL').exists())

    def test_verify_success_receipt_is_real(self):
        self.command(['{python}','-c','print("local test result")'])
        plan=workflow.verification_plan(self.root,names=['test'])
        receipt,code,path=workflow.execute_verification(self.root,plan)
        self.assertEqual(code,0)
        self.assertEqual(receipt['checks'][0]['status'],'PASS')
        self.assertTrue(path.exists())
        self.assertEqual(receipt['checks'][0]['log_sha256'],core.sha(self.root/receipt['checks'][0]['log_path']))

    def test_verify_failure_is_not_pass(self):
        self.command(['{python}','-c','raise SystemExit(7)'])
        receipt,code,_=workflow.execute_verification(self.root,workflow.verification_plan(self.root,names=['test']))
        self.assertEqual(code,1)
        self.assertEqual(receipt['checks'][0]['exit_code'],7)
        self.assertEqual(receipt['checks'][0]['status'],'FAIL')

    def test_verify_missing_executable_blocked(self):
        self.command(['no-such-executable-template-fixture-456'])
        receipt,code,_=workflow.execute_verification(self.root,workflow.verification_plan(self.root,names=['test']))
        self.assertEqual(code,1)
        self.assertEqual(receipt['checks'][0]['status'],'BLOCKED')

    def test_verify_timeout_is_blocked(self):
        self.command(['{python}','-c','import time; time.sleep(5)'],timeout=1)
        receipt,code,_=workflow.execute_verification(self.root,workflow.verification_plan(self.root,names=['test']))
        self.assertEqual(code,1)
        self.assertEqual(receipt['checks'][0]['status'],'BLOCKED')

    def test_unconfigured_checks_are_incomplete(self):
        receipt,code,_=workflow.execute_verification(self.root,workflow.verification_plan(self.root))
        self.assertEqual(code,2)
        self.assertEqual(receipt['overall'],'INCOMPLETE')

    def test_empty_registry_not_vacuous_success(self):
        path=self.root/'.repo/project.json';data=core.load_json(path);data['commands']={};core.dump_json(path,data)
        with self.assertRaises(ValueError):
            workflow.verification_plan(self.root)

    def test_branch_report_never_claims_remote_freshness(self):
        report=core.state(self.root)
        self.assertEqual(report['remote_freshness'],'NOT_VERIFIED')
        self.assertEqual(report['pr_state'],'NOT_VERIFIED')
        self.assertEqual(self.cli('branch','check','--strict').returncode,2)

    def test_init_does_not_install_or_create_app(self):
        result=self.cli('init','--name','Example','--branch','dev')
        self.assertEqual(result.returncode,0)
        self.assertEqual(core.load_json(self.root/'.repo/project.json')['project_name'],'Example')
        self.assertFalse((self.root/'package.json').exists())
        self.assertEqual(self.cli('init','--name','Another').returncode,2)

    def test_adoption_dry_run_has_no_writes(self):
        self.manifest();dest=self.base/'destination';dest.mkdir()
        plan=workflow.adoption_plan(self.root,dest)
        self.assertEqual(plan['conflicts'],0)
        self.assertEqual(list(dest.iterdir()),[])

    def test_adoption_conflict_blocks_copy(self):
        self.manifest();dest=self.base/'destination';dest.mkdir();(dest/'README.md').write_text('Existing owner')
        plan=workflow.adoption_plan(self.root,dest)
        self.assertGreater(plan['conflicts'],0)
        with self.assertRaises(ValueError):
            workflow.apply_adoption(self.root,plan)
        self.assertFalse((dest/'AGENTS.md').exists())
        self.assertEqual((dest/'README.md').read_text(),'Existing owner')

    def test_adoption_copy_and_repeat_are_idempotent(self):
        self.manifest();dest=self.base/'destination';dest.mkdir()
        plan=workflow.adoption_plan(self.root,dest)
        count=workflow.apply_adoption(self.root,plan)
        self.assertGreater(count,50)
        again=workflow.adoption_plan(self.root,dest)
        self.assertEqual(workflow.apply_adoption(self.root,again),0)

    def test_adoption_refuses_overlapping_destination(self):
        self.manifest()
        with self.assertRaises(ValueError):
            workflow.adoption_plan(self.root,self.root/'docs')

    def test_adoption_refuses_changed_source(self):
        self.manifest();self.write('AGENTS.md','changed source');dest=self.base/'destination';dest.mkdir()
        with self.assertRaises(ValueError):
            workflow.adoption_plan(self.root,dest)

    def test_checks_accept_a_real_app_and_do_not_execute_registered_commands(self):
        self.write('package.json', '{"name":"fixture-app","private":true}')
        self.write('apps/browser/index.html', '<p>Synthetic first slice</p>')
        self.write('node_modules/huge-dependency/README.md', '[irrelevant](missing.md)')
        self.command(['{python}', '-c', 'from pathlib import Path; Path("SHOULD_NOT_RUN").touch()'])
        self.assertEqual(self.cli('check').returncode, 0)
        self.assertFalse((self.root / 'SHOULD_NOT_RUN').exists())

    def test_readme_and_scripts_agree_about_python(self):
        self.assertIn('Python 3.11',core.text(self.root/'README.md'))
        self.assertIn('tools/tests',core.text(self.root/'README.md'))


    def setup_git_fixture(self):
        if not shutil.which('git'):
            self.skipTest('Git unavailable to test environment')
        def run(*args):
            result = subprocess.run(['git', '-c', 'user.name=Template Test',
                                     '-c', 'user.email=template@example.invalid',
                                     '-c', 'commit.gpgsign=false', *args],
                                    cwd=self.root, text=True, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout.strip()
        run('init', '-b', 'main')
        run('add', '.')
        run('commit', '-m', 'Fixture baseline')
        return run

    def test_git_auto_uses_cached_origin_head_not_feature_name(self):
        run = self.setup_git_fixture()
        run('update-ref', 'refs/remotes/origin/main', 'HEAD')
        run('symbolic-ref', 'refs/remotes/origin/HEAD', 'refs/remotes/origin/main')
        run('checkout', '-b', 'feature/test')
        report = core.state(self.root)
        self.assertEqual(report['integration_branch'], 'main')
        self.assertEqual(report['branch'], 'feature/test')
        self.assertEqual(report['working_tree'], 'CLEAN')
        self.assertEqual(report['ahead'], 0)
        self.assertEqual(report['behind'], 0)
        self.assertEqual(self.cli('branch', 'check', '--strict').returncode, 0)
        self.assertEqual(report['remote_freshness'], 'NOT_VERIFIED')
        self.assertEqual(run('remote'), '')  # no real remote/network was used

    def test_git_strict_refuses_missing_cached_tip_and_detached_head(self):
        cfg = core.load_json(self.root / '.repo/project.json')
        cfg['integration_branch'] = 'main'
        core.dump_json(self.root / '.repo/project.json', cfg)
        run = self.setup_git_fixture()
        run('checkout', '-b', 'feature/test')
        self.assertEqual(self.cli('branch', 'check', '--strict').returncode, 2)
        run('update-ref', 'refs/remotes/origin/main', 'HEAD')
        run('checkout', '--detach')
        self.assertEqual(self.cli('branch', 'check', '--strict').returncode, 2)

    def test_git_hygiene_flags_tracked_secret_name_without_reading_contents(self):
        run = self.setup_git_fixture()
        self.write('.env', 'SYNTHETIC_FIXTURE_ONLY=not-a-real-credential')
        run('add', '-f', '.env')
        result = self.cli('hygiene')
        self.assertEqual(result.returncode, 1)
        self.assertIn('".env"', result.stdout)
        self.assertNotIn('SYNTHETIC_FIXTURE_ONLY', result.stdout)
        self.assertIn('Filename-only', result.stdout)

    def test_missing_infrastructure_suite_cannot_pass_static_check(self):
        (self.root / 'tools/tests/test_repo_tool.py').unlink()
        self.assertTrue(any('tools/tests/test_repo_tool.py' in e
                            for e in validation.doc_errors(self.root)))

    def test_invalid_project_json_shape_reports_clear_error(self):
        self.write('.repo/project.json', '[]')
        self.assertIn('project.json must be a JSON object', validation.config_errors(self.root))


if __name__=='__main__':
    unittest.main()
