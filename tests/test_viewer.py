import hashlib
from html import unescape
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import fievel as f
from scripts import viewer as v


class ViewerTests(unittest.TestCase):
    def setUp(self):
        scratch = f.ROOT / '.scratch'
        scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        def cleanup():
            assert Path(self.temp.name).resolve().is_relative_to(scratch.resolve())
            self.temp.cleanup()
        self.addCleanup(cleanup)
        self.folder = f.initialize(Path(self.temp.name) / 'project', example=True)

    def edit(self, name, change):
        path = self.folder / (name + '.json')
        value = f.read(path)
        change(value)
        path.write_text(json.dumps(value), encoding='utf-8')

    def report(self):
        result = f.evaluate(self.folder, f.read(f.ROOT / 'examples/responses-good.json'))
        path = Path(self.temp.name) / 'run.json'
        f.write_new(path, result)
        return path

    def test_real_package_relationships_and_no_implicit_results(self):
        data = v.load_snapshot(self.folder)
        self.assertEqual(data['package']['product']['name'], 'Wayfarer')
        self.assertEqual(len(data['rules']), 5)
        self.assertEqual(len(data['checks']), 9)
        rule = next(r for r in data['rules'] if r['id'] == 'behavior-1')
        self.assertEqual(rule['source_links'][0]['state'], 'linked')
        self.assertEqual(len(rule['checks']), 2)
        self.assertEqual(data['report']['state'], 'none')
        self.assertFalse(data['issues'])

    def test_empty_and_uncovered_drafts_remain_visible(self):
        blank = f.initialize(Path(self.temp.name) / 'blank')
        data = v.load_snapshot(blank)
        self.assertEqual(data['rules'], [])
        self.assertEqual(data['package']['progress']['stages']['1'], 'pending')
        self.edit('behavior', lambda d: d['rules'].append(
            {'id':'new-rule','instruction':'A draft rule','source_ids':[],'status':'draft'}))
        data = v.load_snapshot(self.folder)
        self.assertTrue(next(r for r in data['rules'] if r['id'] == 'new-rule')['uncovered'])

    def test_broken_source_and_requirement_links_are_diagnostic(self):
        self.edit('behavior', lambda d: d['rules'][0].update(source_ids=['missing']))
        self.edit('evaluation', lambda d: d['scenarios'][0]['checks'][0].update(requirement_id='absent'))
        data = v.load_snapshot(self.folder)
        self.assertEqual(next(r for r in data['rules'] if r['id'] == 'behavior-1')['source_links'][0]['state'], 'missing')
        self.assertEqual(data['checks'][0]['target_state'], 'missing')
        self.assertTrue(any('missing' in i['message'].lower() for i in data['issues']))

    def test_ambiguous_sources_and_rules_not_silently_resolved(self):
        self.edit('sources', lambda d: d.append(dict(d[0])))
        self.edit('behavior', lambda d: d['rules'].append(dict(d['rules'][0])))
        data = v.load_snapshot(self.folder)
        self.assertEqual(data['rules'][0]['source_links'][0]['state'], 'ambiguous')
        self.assertEqual(data['checks'][0]['target_state'], 'ambiguous')

    def test_missing_malformed_and_schema_invalid_files(self):
        (self.folder / 'product.json').write_text('{invalid', encoding='utf-8')
        (self.folder / 'governance.json').unlink()
        self.edit('standards', lambda d: d.update(rules='not a list'))
        data = v.load_snapshot(self.folder)
        self.assertNotIn('product', data['package'])
        self.assertNotIn('standards', data['package'])
        self.assertIsNone(data['system_sha256'])
        self.assertGreaterEqual(len(data['issues']), 3)
        v.export_viewer(self.folder, Path(self.temp.name) / 'diagnostic.html')

    def test_report_reproduced_but_never_infers_human_passes(self):
        data = v.load_snapshot(self.folder, self.report())
        self.assertEqual(data['report']['state'], 'reproduced')
        self.assertEqual(data['report']['summary'], {'pass':3,'fail':0,'not_run':6})

    def test_stale_or_altered_report_totals_are_not_displayed(self):
        path = self.report()
        value = f.read(path)
        value['summary']['pass'] = 99
        path.write_text(json.dumps(value), encoding='utf-8')
        data = v.load_snapshot(self.folder, path)
        self.assertEqual(data['report']['state'], 'invalid')
        self.assertIsNone(data['report']['summary'])
        self.edit('product', lambda d: d.update(name='Revised product'))
        data = v.load_snapshot(self.folder, path)
        self.assertEqual(data['report']['state'], 'stale')
        self.assertIsNone(data['report']['summary'])

    def test_unsupported_or_unreadable_report(self):
        path = Path(self.temp.name) / 'human.json'
        f.write_new(path, {'kind':'human_review','judgments':[]})
        self.assertEqual(v.load_snapshot(self.folder, path)['report']['state'], 'unsupported')
        path.write_text('null', encoding='utf-8')
        self.assertEqual(v.load_snapshot(self.folder, path)['report']['state'], 'invalid')

    def test_saved_responses_and_execution_timestamp_are_checked(self):
        path = self.report()
        original = f.read(path)
        for patch in ({'responses':{'payment-unknown':'Changed response'}},
                      {'executed_at':'not-a-date'}, {'executed_at':'2026-10-21T10:00:00'}):
            path.write_text(json.dumps(dict(original, **patch)), encoding='utf-8')
            self.assertEqual(v.load_snapshot(self.folder,path)['report']['state'], 'invalid')

    def test_export_preserves_inputs_and_refuses_existing_output(self):
        before = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.folder.iterdir() if p.is_file()}
        out = Path(self.temp.name) / 'snapshot.html'
        v.export_viewer(self.folder, out)
        self.assertEqual(before, {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.folder.iterdir() if p.is_file()})
        original = out.read_bytes()
        with self.assertRaises(FileExistsError):
            v.export_viewer(self.folder, out)
        self.assertEqual(out.read_bytes(), original)

    def test_html_and_script_strings_are_inert_data(self):
        attack = '</script><img src=x onerror="window.ATTACKED=1"><script>window.ATTACKED=1</script>'
        self.edit('product', lambda d: d.update(name=attack))
        out = Path(self.temp.name) / 'hostile.html'
        v.export_viewer(self.folder, out)
        html = out.read_text(encoding='utf-8')
        self.assertNotIn('<img src=x', html)
        self.assertIn('\\u003c/script\\u003e', html)
        self.assertIn("connect-src 'none'", unescape(html))
        self.assertNotIn('innerHTML', (f.ROOT/'viewer/viewer.js').read_text(encoding='utf-8'))

    def test_cli_runs_from_another_directory(self):
        out = Path(self.temp.name) / 'cli.html'
        run = subprocess.run([sys.executable,str(f.ROOT/'scripts/fievel.py'),'view',str(self.folder),
                              '--out',str(out)],cwd=self.temp.name,capture_output=True,text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(out.exists())


if __name__ == '__main__':
    unittest.main()
