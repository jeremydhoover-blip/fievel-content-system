import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from scripts.build_plugin import ROOT, build


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
