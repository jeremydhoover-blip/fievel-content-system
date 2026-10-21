import copy
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('fievel', ROOT / 'scripts/fievel.py')
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '.scratch'
        scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        def cleanup():
            # Verify the absolute target before recursive temporary cleanup.
            assert Path(self.temp.name).resolve().is_relative_to(scratch.resolve())
            self.temp.cleanup()
        self.addCleanup(cleanup)
        self.folder = f.initialize(Path(self.temp.name) / 'system', example=True)

    def edit(self, name, change):
        path = self.folder / (name + '.json')
        value = f.read(path)
        change(value)
        path.write_text(json.dumps(value), encoding='utf-8')

    def test_schema_and_bundled_packages(self):
        f.Draft202012Validator.check_schema(f.read(ROOT / 'schemas/content-system.schema.json'))
        for folder in ('examples/wayfarer', 'templates/content-system'):
            f.validate(ROOT / folder)

    def test_initialization_preserves_existing_work(self):
        marker = self.folder / 'mine.txt'
        marker.write_text('keep')
        with self.assertRaises(ValueError):
            f.initialize(self.folder, True)
        self.assertEqual(marker.read_text(), 'keep')

    def test_template_starts_pending(self):
        folder = f.initialize(Path(self.temp.name) / 'new')
        data = f.validate(folder)
        self.assertEqual(set(data['progress']['stages'].values()), {'pending'})
        self.assertIsNone(data['governance']['owner'])
        self.assertEqual(data['sources'], [])

    def test_invalid_shape_rejected(self):
        self.edit('product', lambda d: d.update(audiences='everyone'))
        with self.assertRaisesRegex(ValueError, 'audiences'):
            f.validate(self.folder)

    def test_unknown_fields_rejected(self):
        self.edit('behavior', lambda d: d.update(hidden_policy=True))
        with self.assertRaisesRegex(ValueError, 'Additional properties'):
            f.validate(self.folder)

    def test_unknown_requirement_rejected(self):
        self.edit('evaluation', lambda d: d['scenarios'][0]['checks'][0].update(requirement_id='missing'))
        with self.assertRaisesRegex(ValueError, 'Unknown requirement'):
            f.validate(self.folder)

    def test_unknown_source_rejected(self):
        self.edit('behavior', lambda d: d['rules'][0].update(source_ids=['missing']))
        with self.assertRaisesRegex(ValueError, 'Unknown source'):
            f.validate(self.folder)

    def test_duplicate_ids_rejected(self):
        self.edit('behavior', lambda d: d['rules'].append(copy.deepcopy(d['rules'][0])))
        with self.assertRaisesRegex(ValueError, 'Duplicate requirement'):
            f.validate(self.folder)

    def test_duplicate_scenarios_rejected(self):
        self.edit('evaluation', lambda d: d['scenarios'].append(copy.deepcopy(d['scenarios'][0])))
        with self.assertRaisesRegex(ValueError, 'Duplicate scenario'):
            f.validate(self.folder)

    def test_duplicate_check_ids_rejected(self):
        self.edit('evaluation', lambda d: d['scenarios'][0]['checks'].append(copy.deepcopy(d['scenarios'][0]['checks'][0])))
        with self.assertRaisesRegex(ValueError, 'Duplicate check'):
            f.validate(self.folder)

    def test_uncovered_requirement_rejected(self):
        self.edit('behavior', lambda d: d['rules'].append({'id':'extra','instruction':'New rule','status':'draft','source_ids':[]}))
        with self.assertRaisesRegex(ValueError, 'without quality checks'):
            f.validate(self.folder, require_coverage=True)

    def test_partial_draft_to_execution_journey(self):
        folder = f.initialize(Path(self.temp.name) / 'partial')
        standards = f.read(folder / 'standards.json')
        standards['rules'] = [{'id':'library-next-step',
            'instruction':"Name library support when escalation is needed.",
            'status':'draft','source_ids':[]}]
        (folder / 'standards.json').write_text(json.dumps(standards),encoding='utf-8')
        progress = f.read(folder / 'progress.json')
        progress['stages']['2'] = 'drafted'
        progress['decisions'] = ['No renewal tool is available.']
        progress['next_action'] = 'Identify the policy owner.'
        (folder / 'progress.json').write_text(json.dumps(progress),encoding='utf-8')

        # A learner can stop and inspect a sound draft before stage 5 exists.
        data = f.validate(folder)
        self.assertEqual(f.coverage_gaps(data), ['library-next-step'])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(f.main(['status',str(folder)]),0)
        self.assertIn('library-next-step',output.getvalue())
        self.assertIn('Identify the policy owner.',output.getvalue())
        self.assertEqual(f.read(folder / 'progress.json')['decisions'],progress['decisions'])

        # Incompleteness is still an error at the explicit coverage/execution gate.
        with self.assertRaisesRegex(ValueError,'without quality checks'):
            f.validate(folder,require_coverage=True)
        with self.assertRaisesRegex(ValueError,'without quality checks'):
            f.evaluate(folder,{'escalation':'Contact library support.'})

        definition = {'scenarios':[{'id':'escalation','situation':'I need a renewal, but it did not work.',
            'context':'No tool or policy is available. Escalation is needed.',
            'checks':[{'id':'destination','requirement_id':'library-next-step',
                'question':'Is library support named?', 'method':'contains','value':'library support'}]}]}
        (folder / 'evaluation.json').write_text(json.dumps(definition),encoding='utf-8')
        self.assertEqual(f.coverage_gaps(f.validate(folder,require_coverage=True)),[])
        self.assertEqual(f.evaluate(folder,{'escalation':'Contact library support.'})['summary'],
                         {'pass':1,'fail':0,'not_run':0})
        definition['scenarios'][0]['checks'][0]['requirement_id'] = 'unknown'
        (folder / 'evaluation.json').write_text(json.dumps(definition),encoding='utf-8')
        for strict in (False,True):
            with self.subTest(strict=strict), self.assertRaisesRegex(ValueError,'Unknown requirement'):
                f.validate(folder,require_coverage=strict)

    def test_partial_draft_cli_modes(self):
        self.edit('behavior',lambda d: d['rules'].append({'id':'uncovered',
            'instruction':'New draft rule.','status':'draft','source_ids':[]}))
        output = io.StringIO()
        errors = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            self.assertEqual(f.main(['validate',str(self.folder)]),0)
            self.assertEqual(f.main(['validate',str(self.folder),'--require-coverage']),2)
        self.assertIn('uncovered',output.getvalue())
        self.assertIn('without quality checks',errors.getvalue())

    def test_empty_literal_rejected(self):
        self.edit('evaluation', lambda d: d['scenarios'][0]['checks'][1].update(value=''))
        with self.assertRaises(ValueError):
            f.validate(self.folder)

    def test_authored_literal_pass_fixture_does_not_pass_human_checks(self):
        result = f.evaluate(self.folder, f.read(ROOT / 'examples/responses-good.json'))
        self.assertEqual(result['summary'], {'pass':3,'fail':0,'not_run':6})
        self.assertTrue(all(row['status']=='not_run' for row in result['results'] if row['method']=='human'))
        self.assertEqual(result['target'], 'saved_responses')

    def test_bad_fixture_fails(self):
        result = f.evaluate(self.folder, f.read(ROOT / 'examples/responses-bad.json'))
        self.assertEqual(result['summary'], {'pass':0,'fail':3,'not_run':6})

    def test_missing_responses_not_run(self):
        result = f.evaluate(self.folder, {'refund-status':'Unknown'})
        self.assertEqual(result['summary']['not_run'],9)

    def test_invalid_response_targets_rejected(self):
        for value in ({}, [], {'unknown':'text'}, {'payment-unknown':''}, {'payment-unknown':42}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                f.evaluate(self.folder, value)

    def test_human_review_is_pending_and_identifies_responses(self):
        responses = f.read(ROOT / 'examples/responses-good.json')
        review = f.review_sheet(self.folder, responses)
        self.assertEqual(review['kind'],'human_review')
        self.assertIsNone(review['reviewer'])
        self.assertEqual(len(review['judgments']),6)
        self.assertEqual({j['status'] for j in review['judgments']},{'pending'})
        self.assertEqual(review['responses'],responses)

    def test_changed_system_changes_evidence_hash(self):
        responses = {'refund-status':'Unknown'}
        first = f.evaluate(self.folder, responses)
        self.edit('product',lambda d: d.update(name='Changed'))
        second = f.evaluate(self.folder, responses)
        self.assertNotEqual(first['system_sha256'],second['system_sha256'])

    def test_reports_never_overwrite(self):
        path = Path(self.temp.name) / 'report.json'
        f.write_new(path, {'original':True})
        with self.assertRaises(FileExistsError):
            f.write_new(path, {})
        self.assertEqual(f.read(path),{'original':True})

    def test_cli_end_to_end_from_other_directory(self):
        project = Path(self.temp.name) / 'cli'
        def cli(*args):
            return subprocess.run([sys.executable,str(ROOT/'scripts/fievel.py'),*map(str,args)],
                cwd=self.temp.name,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(cli('init',project,'--example').returncode,0)
        self.assertEqual(cli('status',project).returncode,0)
        self.assertEqual(cli('validate',project).returncode,0)
        report = project/'results/good.json'
        result = cli('check',project,'--responses',ROOT/'examples/responses-good.json','--out',report)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(f.read(report)['summary']['not_run'],6)
        self.assertEqual(cli('check',project,'--responses',ROOT/'examples/responses-bad.json','--out',project/'results/bad.json').returncode,1)
        self.assertEqual(cli('check',project,'--responses',ROOT/'examples/responses-good.json','--out',report).returncode,2)

    def test_cli_execution_coverage_distinguishes_not_run_reasons(self):
        responses = f.read(ROOT / 'examples/responses-good.json')
        first_id = next(iter(responses))
        target = Path(self.temp.name) / 'partial-responses.json'
        f.write_new(target, {first_id: responses[first_id]})
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = f.main(['check', str(self.folder), '--responses', str(target),
                           '--out', str(Path(self.temp.name) / 'partial-run.json')])
        self.assertEqual(code, 0)
        report = f.read(Path(self.temp.name) / 'partial-run.json')
        missing = sum(row['scenario_id'] != first_id for row in report['results'])
        awaiting = sum(row['scenario_id'] == first_id and row['method'] == 'human'
                       for row in report['results'])
        self.assertIn(f'{missing} checks missing saved responses', output.getvalue())
        self.assertIn(f'{awaiting} checks awaiting human review', output.getvalue())
        self.assertIn('This is not an overall quality verdict', output.getvalue())

    def test_cli_all_human_explicitly_reports_zero_execution(self):
        def all_human(data):
            for scenario in data['scenarios']:
                for check in scenario['checks']:
                    check['method'] = 'human'
                    check['value'] = ''
        self.edit('evaluation', all_human)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = f.main(['check', str(self.folder), '--responses',
                           str(ROOT / 'examples/responses-good.json'), '--out',
                           str(Path(self.temp.name) / 'all-human.json')])
        self.assertEqual(code, 0)  # Preserve the documented exit-code contract.
        self.assertIn('Executed 0 of 9 defined checks', output.getvalue())
        self.assertIn('No automated checks ran', output.getvalue())
        self.assertIn('9 checks awaiting human review', output.getvalue())

    def test_adapters_and_skill_metadata(self):
        self.assertEqual(f.adapters(check=True),8)
        for path in (ROOT/'.agents/skills').glob('*/SKILL.md'):
            text = path.read_text(encoding='utf-8')
            self.assertTrue(text.startswith('---\n'))
            self.assertIn('name: '+path.parent.name+'\n',text)
            self.assertIn('description: ',text)
            self.assertLess(len(text.split('description: ',1)[1].splitlines()[0]),1024)


if __name__ == '__main__':
    unittest.main()
