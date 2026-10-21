import copy
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import fievel as f
from scripts.provenance import audit_sources

class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        (ROOT/'.scratch').mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.scratch')
        self.folder=f.initialize(Path(self.temp.name)/'system',True)
        def cleanup():
            assert Path(self.temp.name).resolve().is_relative_to((ROOT/'.scratch').resolve())
            self.temp.cleanup()
        self.addCleanup(cleanup)
        data=f.validate(self.folder)
        self.config={'version':'1.0','conflicts':[],'evidence':[{'rule_id':r['id'],'source_id':sid,'locator':'handbook.md paragraph 1','excerpt':'Fictional evidence supplied by the test fixture'} for r in data['standards']['rules']+data['behavior']['rules'] for sid in r['source_ids']]}
    def edit_sources(self,change):
        p=self.folder/'sources.json';data=f.read(p);change(data);p.write_text(json.dumps(data),encoding='utf-8')
    def audit(self,config=None,days=365):return audit_sources(self.folder,'2026-10-21',self.config if config is None else config,days)
    def codes(self,result):return {v['code'] for v in result['findings']}
    def test_supplied_evidence_is_not_approval_or_original_verification(self):
        result=self.audit()
        self.assertEqual(result['counts'],{'error':0,'warning':0})
        self.assertFalse(result['source_locations_checked'])
        self.assertNotIn('pass',result)
    def test_unknown_metadata_and_missing_evidence_are_warnings(self):
        self.edit_sources(lambda d:d[0].update(owner=None,reviewed_on=None,permissions='unknown',authority='unverified'))
        result=self.audit({'version':'1.0','evidence':[],'conflicts':[]})
        self.assertEqual(result['counts']['error'],0)
        self.assertTrue({'owner_unknown','review_date_unknown','permissions_unknown','authority_unverified','evidence_locator_missing','ingestion_permission_unresolved'}<=self.codes(result))
    def test_invalid_future_and_old_dates(self):
        for value,code in [('nonsense','invalid_date'),('2026-02-30','invalid_date'),('2026-10-22','future_date'),('2020-01-01','review_window_exceeded')]:
            self.edit_sources(lambda d:d[0].update(reviewed_on=value))
            with self.subTest(value=value):self.assertIn(code,self.codes(self.audit()))
    def test_no_invented_freshness_policy(self):
        self.edit_sources(lambda d:d[0].update(reviewed_on='2020-01-01'))
        result=self.audit(days=None)
        self.assertNotIn('review_window_exceeded',self.codes(result))
        self.assertIn('freshness_window_unspecified',self.codes(result))
    def test_unknown_undeclared_and_duplicate_evidence(self):
        for change,code in [(lambda c:c['evidence'][0].update(rule_id='missing'),'unknown_evidence_reference'),(lambda c:c['evidence'].append(copy.deepcopy(c['evidence'][0])),'duplicate_evidence')]:
            config=copy.deepcopy(self.config);change(config)
            with self.subTest(code=code):self.assertIn(code,self.codes(self.audit(config)))
        self.edit_sources(lambda d:d.append(dict(d[0],id='other')))
        config=copy.deepcopy(self.config);config['evidence'][0]['source_id']='other'
        self.assertIn('undeclared_rule_source',self.codes(self.audit(config)))
    def test_declared_conflict_open_and_incomplete_resolution(self):
        self.edit_sources(lambda d:d.append(dict(d[0],id='other')))
        config=copy.deepcopy(self.config)
        conflict={'id':'conflict-1','source_ids':['wayfarer-handbook','other'],'description':'Contradiction declared by fixture','status':'open','resolution':None,'decided_by':None,'decided_on':None}
        config['conflicts']=[conflict]
        self.assertIn('open_conflict',self.codes(self.audit(config)))
        conflict['status']='resolved'
        self.assertIn('conflict_decision_incomplete',self.codes(self.audit(config)))
        conflict.update(resolution='Fictional resolution',decided_by='Fixture owner',decided_on='2026-10-21')
        self.assertNotIn('conflict_decision_incomplete',self.codes(self.audit(config)))
    def test_untrusted_locations_are_not_opened(self):
        self.edit_sources(lambda d:d[0].update(location='https://invalid.example/never-fetch'))
        result=self.audit()
        self.assertFalse(result['source_locations_checked'])
        self.assertEqual(result['counts']['error'],0)
    def test_invalid_inputs_and_blank_locator(self):
        for args in [('2026-13-01',self.config,365),('20261021',self.config,365),('2026-10-21',[],365),('2026-10-21',self.config,0)]:
            with self.subTest(args=args),self.assertRaises(ValueError):audit_sources(self.folder,*args)
        config=copy.deepcopy(self.config);config['evidence'][0]['locator']=' '
        with self.assertRaises(ValueError):self.audit(config)
    def test_read_only_cli_strict_and_overwrite(self):
        before={p.name:p.read_bytes() for p in self.folder.iterdir() if p.is_file()}
        path=Path(self.temp.name)/'audit.json'
        args=['sources-audit',str(self.folder),'--as-of','2026-10-21']
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(f.main(args+['--out',str(path)]),0)
            self.assertEqual(f.main(args+['--strict']),1)
            self.assertEqual(f.main(args+['--out',str(path)]),2)
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.folder.iterdir() if p.is_file()})

if __name__=='__main__':unittest.main()
