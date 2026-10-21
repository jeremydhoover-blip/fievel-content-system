import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from scripts.build_plugin import ROOT, build, package_files


class PluginBundleTests(unittest.TestCase):
    def test_relocated_bundle_and_user_files(self):
        scratch = ROOT / '.scratch'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as tmp:
            base = Path(tmp)
            plugin = base / 'installed plugin'
            manifest = build(plugin)
            self.assertFalse(any('/my-content-system/' in p or '/.deps/' in p or '/evals/' in p for p in manifest))
            self.assertTrue(all(hashlib.sha256((plugin / p).read_bytes()).hexdigest() == h for p, h in manifest.items()))
            with self.assertRaises(FileExistsError):
                build(plugin)
            workspace = base / 'user workspace'
            workspace.mkdir()
            sentinel = workspace / 'AGENTS.md'
            sentinel.write_text('User instructions must survive', encoding='utf-8')
            # Supply the test environment's validator without embedding it in the bundle.
            import os
            env = dict(os.environ, PYTHONPATH=str(ROOT / '.deps'), PYTHONDONTWRITEBYTECODE='1')
            def run(*args):
                proc = subprocess.run([sys.executable, str(plugin / 'runtime/scripts/fievel.py'), *args],
                                      cwd=workspace, env=env, capture_output=True, text=True)
                self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            run('init', 'system', '--example')
            run('validate', 'system', '--require-coverage')
            run('check', 'system', '--responses', str(plugin / 'runtime/examples/responses-good.json'), '--out', 'run.json')
            run('view', 'system', '--out', 'view.html')
            run('review', 'system', '--responses', str(plugin / 'runtime/examples/responses-good.json'),
                '--evidence-config', str(plugin / 'runtime/examples/review-evidence-config.json'), '--out', 'review.json')
            run('review-page', 'review.json', '--out', 'review.html')
            self.assertEqual(sentinel.read_text(encoding='utf-8'), 'User instructions must survive')
            self.assertFalse((plugin / 'runtime/system').exists())
            self.assertTrue((workspace / 'view.html').is_file())
            self.assertEqual(json.loads((plugin / 'bundle-manifest.json').read_text()), manifest)
            self.assertTrue(all(hashlib.sha256((plugin / p).read_bytes()).hexdigest() == h for p, h in manifest.items()))

    def test_target_layouts_share_runtime(self):
        codex = package_files(target='codex')
        claude = package_files(target='claude')
        self.assertIn('plugin.json', codex)
        self.assertNotIn('.claude-plugin/plugin.json', codex)
        self.assertNotIn('plugin.json', claude)
        manifest = json.loads(claude['.claude-plugin/plugin.json'])
        self.assertIn(manifest['icon'].removeprefix('./'), claude)
        authored = json.loads((ROOT / 'plugin-src/plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['name'], authored['name'])
        self.assertEqual(manifest['version'], (ROOT / 'VERSION').read_text(encoding='utf-8').strip())
        self.assertEqual(manifest['version'], authored['version'])
        self.assertNotIn('$schema', manifest)
        self.assertNotIn('extensions', manifest)
        # Same skill and runtime bytes, so the skill's root-relative paths hold in both hosts.
        shared = {p for p in codex if p.startswith(('runtime/', 'skills/'))}
        self.assertEqual(shared, {p for p in claude if p.startswith(('runtime/', 'skills/'))})
        self.assertTrue(all(codex[p] == claude[p] for p in shared))
        with self.assertRaises(ValueError):
            package_files(target='vscode')

    def test_claude_bundle_runs_relocated(self):
        scratch = ROOT / '.scratch'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as tmp:
            plugin = Path(tmp) / 'claude plugin'
            build(plugin, target='claude')
            workspace = Path(tmp) / 'workspace'
            workspace.mkdir()
            import os
            env = dict(os.environ, PYTHONPATH=str(ROOT / '.deps'), PYTHONDONTWRITEBYTECODE='1')
            for args in (('init', 'system', '--example'), ('validate', 'system', '--require-coverage')):
                proc = subprocess.run([sys.executable, str(plugin / 'runtime/scripts/fievel.py'), *args],
                                      cwd=workspace, env=env, capture_output=True, text=True)
                self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            self.assertFalse((plugin / 'runtime/system').exists())

    def test_committed_bundles_match_fresh_builds(self):
        for target, folder in (('codex', 'plugins/fievel'), ('claude', 'plugins/fievel-claude')):
            with self.subTest(target=target):
                committed = ROOT / folder
                expected = package_files(target=target)
                # The manifest is skipped: Git line-ending conversion changes text hashes on checkout.
                actual = {p.relative_to(committed).as_posix(): p.read_bytes() for p in committed.rglob('*')
                          if p.is_file() and '__pycache__' not in p.parts and p.name != 'bundle-manifest.json'}
                self.assertEqual(sorted(actual), sorted(expected))
                self.assertTrue(all(actual[p] == expected[p] for p in expected),
                                f'{folder} is stale; rebuild with scripts/build_plugin.py --target {target}')

    def test_marketplaces_point_to_bundles(self):
        claude = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
        codex = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
        self.assertTrue(claude['name'] and claude['owner']['name'])
        for catalog, source_of, manifest_path in (
                (claude, lambda e: e['source'], '.claude-plugin/plugin.json'),
                (codex, lambda e: e['source']['path'], 'plugin.json')):
            [entry] = catalog['plugins']
            source = source_of(entry)
            self.assertTrue(source.startswith('./') and '..' not in source, source)
            manifest = json.loads((ROOT / source / manifest_path).read_text(encoding='utf-8'))
            self.assertEqual(entry['name'], manifest['name'])
