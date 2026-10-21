"""Content-scoped system fingerprint and legacy report migration (ADR-007)."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts import fievel as f
from scripts import review_evidence as r
from scripts import viewer as v

ROOT = Path(__file__).resolve().parents[1]
RESPONSES = json.loads((ROOT / 'examples/responses-good.json').read_text(encoding='utf-8'))
CONFIG = json.loads((ROOT / 'examples/review-evidence-config.json').read_text(encoding='utf-8'))
LEGACY_REPORT = ROOT / 'evals/evidence/literal-pass.json'
LEGACY_REVIEWS = [ROOT / 'docs/audits/2026-10-21/review-evidence/pending-example.json',
                  ROOT / 'evals/human-review-calibration/round-01/reviewer-a/C01.json']


class ContentFingerprintTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '.scratch'
        scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.folder = f.initialize(self.base / 'system', example=True)

    def edit(self, name, change):
        path = self.folder / f'{name}.json'
        data = f.read(path)
        change(data)
        path.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def save(self, name, value):
        path = self.base / name
        path.write_text(json.dumps(value), encoding='utf-8')
        return path

    def save_progress(self):
        self.edit('progress', lambda d: d.update(next_action='Review the saved responses with the content lead'))

    def test_progress_edit_keeps_identity_and_content_edit_changes_it(self):
        first = f.evaluate(self.folder, RESPONSES)
        self.assertEqual(first['system_scope'], 'content')
        self.save_progress()
        self.assertEqual(f.evaluate(self.folder, RESPONSES)['system_sha256'], first['system_sha256'])
        for name in ('product', 'governance'):
            self.edit(name, lambda d: d.update(name='Changed') if name == 'product' else d.update(owner='Changed owner'))
            self.assertNotEqual(f.evaluate(self.folder, RESPONSES)['system_sha256'], first['system_sha256'], name)
        sheet = f.review_sheet(self.folder, RESPONSES)
        self.assertEqual(sheet['system_scope'], 'content')

    def test_new_report_stays_current_in_viewer_after_progress_save(self):
        report = self.save('run.json', f.evaluate(self.folder, RESPONSES))
        self.save_progress()
        self.assertEqual(v.load_snapshot(self.folder, report)['report']['state'], 'reproduced')
        self.edit('product', lambda d: d.update(name='Changed'))
        self.assertEqual(v.load_snapshot(self.folder, report)['report']['state'], 'stale')

    def test_legacy_report_keeps_seven_file_meaning(self):
        legacy = json.loads(LEGACY_REPORT.read_text(encoding='utf-8'))
        self.assertNotIn('system_scope', legacy)
        self.assertEqual(v.load_snapshot(self.folder, LEGACY_REPORT)['report']['state'], 'reproduced')
        self.save_progress()
        self.assertEqual(v.load_snapshot(self.folder, LEGACY_REPORT)['report']['state'], 'stale')

    def test_unknown_scope_is_rejected(self):
        report = dict(f.evaluate(self.folder, RESPONSES), system_scope='future')
        with self.assertRaises(ValueError):
            f.matches_system(report, f.validate(self.folder))
        self.assertEqual(v.load_snapshot(self.folder, self.save('odd.json', report))['report']['state'], 'invalid')

    def test_review_evidence_versions(self):
        review = r.prepare_review(self.folder, RESPONSES, CONFIG)
        self.assertEqual(review['version'], '1.1')
        self.save_progress()
        r.validate_review(review, folder=self.folder)
        self.edit('product', lambda d: d.update(name='Changed'))
        with self.assertRaises(ValueError):
            r.validate_review(review, folder=self.folder)
        for path in LEGACY_REVIEWS:
            legacy = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(legacy['version'], '1.0')
            r.validate_review(legacy)
            tampered = json.loads(json.dumps(legacy))
            tampered['system_snapshot']['progress']['next_action'] = 'Tampered'
            with self.assertRaises(ValueError):
                r.validate_review(tampered)
