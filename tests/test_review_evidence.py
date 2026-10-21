import copy
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import fievel as f
from scripts.review_evidence import prepare_review, validate_review


class EvidenceReviewTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '.scratch'
        scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        def cleanup():
            assert Path(self.temp.name).resolve().is_relative_to(scratch.resolve())
            self.temp.cleanup()
        self.addCleanup(cleanup)
        self.folder = f.initialize(Path(self.temp.name) / 'system', True)
        self.responses = f.read(ROOT / 'examples/responses-good.json')
        self.config = f.read(ROOT / 'examples/review-evidence-config.json')
        self.review = prepare_review(self.folder, self.responses, self.config)

    def completed_fixture(self):
        # Synthetic validator input, never a real human review or quality result.
        r = copy.deepcopy(self.review)
        r.update(reviewer='Synthetic validator fixture', reviewed_at='2026-10-21T12:00:00+03:00')
        for row in r['judgments']:
            row.update(status='fail', rationale='Synthetic rationale for validator testing only.',
                       response_evidence=self.responses[row['scenario_id']])
        return r

    def test_pending_self_contained_and_legacy_unchanged(self):
        self.assertEqual(validate_review(self.review)['pending'], 6)
        self.assertIn('product', self.review['system_snapshot'])
        self.assertEqual(f.review_sheet(self.folder, self.responses)['kind'], 'human_review')
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            validate_review(self.review, require_complete=True)

    def test_complete_can_contain_fail_and_needs_no_current_files(self):
        self.assertEqual(validate_review(self.completed_fixture(), require_complete=True)['fail'], 6)
        path = self.folder / 'product.json'
        data = f.read(path)
        data['name'] = 'Changed'
        path.write_text(json.dumps(data), encoding='utf-8')
        self.assertEqual(validate_review(self.review)['pending'], 6)
        with self.assertRaisesRegex(ValueError, 'stale'):
            validate_review(self.review, self.folder)

    def test_all_snapshot_hashes_checked(self):
        for field in ['system_sha256', 'responses_sha256', 'config_sha256']:
            r = copy.deepcopy(self.review)
            r[field] = 'tampered'
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'hash mismatch'):
                validate_review(r)

    def test_exact_membership_and_shape(self):
        mutations = [lambda r:r['judgments'].pop(),
                     lambda r:r['judgments'].append(copy.deepcopy(r['judgments'][0])),
                     lambda r:r['judgments'][0].update(check_id='unknown'),
                     lambda r:r.update(version='99'),
                     lambda r:r.update(extra='not permitted'),
                     lambda r:r['judgments'][0].update(status='approved')]
        for mutate in mutations:
            r = copy.deepcopy(self.review)
            mutate(r)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                validate_review(r)

    def test_decisions_require_human_metadata_rationale_and_actual_quote(self):
        mutations = [lambda r:r.update(reviewer=None),
                     lambda r:r.update(reviewer='  '),
                     lambda r:r.update(reviewer_kind='ai'),
                     lambda r:r.update(reviewed_at='2026-10-21'),
                     lambda r:r.update(reviewed_at='invalid'),
                     lambda r:r['judgments'][0].update(rationale='  '),
                     lambda r:r['judgments'][0].update(response_evidence='invented quotation')]
        for mutate in mutations:
            r = self.completed_fixture()
            mutate(r)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                validate_review(r, require_complete=True)

    def test_missing_responses_never_become_judgments(self):
        responses = {'payment-unknown':self.responses['payment-unknown']}
        cfg = copy.deepcopy(self.config)
        cfg['response_origins'] = {'payment-unknown':cfg['response_origins']['payment-unknown']}
        r = prepare_review(self.folder, responses, cfg)
        self.assertEqual(validate_review(r)['not_run'], 5)
        row = next(j for j in r['judgments'] if j['status'] == 'not_run')
        row['status'] = 'pass'
        with self.assertRaisesRegex(ValueError, 'Missing response'):
            validate_review(r)

    def test_missing_source_or_origin_blocks_completed_decisions(self):
        for kind in ['source', 'origin']:
            r = self.completed_fixture()
            if kind == 'source':
                r['review_config']['source_evidence'] = []
            else:
                for origin in r['review_config']['response_origins'].values():
                    origin.update(kind='unknown', description=None)
            r['config_sha256'] = f.fingerprint(r['review_config'])
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                validate_review(r, require_complete=True)

    def test_borderline_and_insufficient_evidence_stay_unresolved(self):
        for state in ['borderline', 'insufficient_evidence']:
            r = self.completed_fixture()
            r['judgments'][0]['status'] = state
            self.assertEqual(validate_review(r)[state], 1)
            with self.assertRaisesRegex(ValueError, 'incomplete'):
                validate_review(r, require_complete=True)

    def test_configuration_rejects_missing_duplicate_and_unknown_links(self):
        for mutate in [lambda c:c['rubrics'].pop(),
                       lambda c:c['rubrics'].append(copy.deepcopy(c['rubrics'][0])),
                       lambda c:c['source_evidence'][0].update(source_id='missing'),
                       lambda c:c['rubrics'][0].update(pass_='wrong key')]:
            cfg = copy.deepcopy(self.config)
            mutate(cfg)
            with self.assertRaises(ValueError):
                prepare_review(self.folder, self.responses, cfg)

    def test_cli_entry_from_another_directory(self):
        output = Path(self.temp.name) / 'from-other-cwd.json'
        def cli(*args):
            return subprocess.run([sys.executable, str(ROOT / 'scripts/fievel.py'), *map(str,args)],
                                  cwd=self.temp.name, capture_output=True, text=True)
        prepared = cli('review', self.folder, '--responses', ROOT/'examples/responses-good.json',
                       '--evidence-config', ROOT/'examples/review-evidence-config.json', '--out', output)
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        checked = cli('validate-review', output, '--folder', self.folder)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        incomplete = cli('validate-review', output, '--require-complete')
        self.assertEqual(incomplete.returncode, 2, incomplete.stderr)
        self.assertIn('incomplete', incomplete.stderr)

    def test_cli_and_no_overwrite(self):
        path = Path(self.temp.name) / 'review.json'
        command = ['review',str(self.folder),'--responses',str(ROOT/'examples/responses-good.json'),
                   '--evidence-config',str(ROOT/'examples/review-evidence-config.json'),'--out',str(path)]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(f.main(command), 0)
            self.assertEqual(f.main(command), 2)
            self.assertEqual(f.main(['validate-review',str(path)]), 0)
            self.assertEqual(f.main(['validate-review',str(path),'--require-complete']), 2)
        self.assertEqual(f.read(path)['reviewer'], None)


if __name__ == '__main__':
    unittest.main()
