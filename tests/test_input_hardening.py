import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import fievel as f
from scripts.viewer import load_snapshot

class InputHardeningTests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".scratch").mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.scratch')
        self.base=Path(self.temp.name)
        def cleanup():
            assert self.base.resolve().is_relative_to((ROOT/'.scratch').resolve())
            self.temp.cleanup()
        self.addCleanup(cleanup)
    def test_ambiguous_and_nonstandard_json_rejected_with_path(self):
        values=['{"a":1,"a":2}','{"a":{"x":1,"x":2}}','{"a":NaN}','{"a":Infinity}','{"a":1e999}','"\\ud800"','['*2000+'0'+']'*2000]
        for i,value in enumerate(values):
            path=self.base/f'bad-{i}.json';path.write_text(value,encoding='utf-8')
            with self.subTest(i=i),self.assertRaisesRegex(ValueError,path.name):f.read(path)
    def test_encoding_and_truncation_errors_identify_file(self):
        for name,value in [('encoding.json',b'\xff\xfe\x01'),('truncated.json',b'{"a":')]:
            path=self.base/name;path.write_bytes(value)
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,name):f.read(path)
    def test_valid_bom_unicode_and_false_values_preserved(self):
        path=self.base/'valid.json';path.write_bytes(b'\xef\xbb\xbf'+ '{"text":"caf\u00e9","value":false,"empty":null}'.encode('utf-8'))
        self.assertEqual(f.read(path),{'text':'caf\u00e9','value':False,'empty':None})
    def test_serialization_failure_leaves_no_output_or_parent(self):
        for i,value in enumerate([{'bad':object()},{'bad':float('nan')},{'bad':'\ud800'}]):
            path=self.base/f'output-{i}'/'report.json'
            with self.subTest(i=i),self.assertRaises((TypeError,ValueError)):f.write_new(path,value)
            self.assertFalse(path.exists())
            self.assertFalse(path.parent.exists())
    def test_viewer_reports_duplicate_json_as_diagnostic(self):
        folder=f.initialize(self.base/'package',True)
        (folder/'product.json').write_text('{"name":"first","name":"second"}')
        snapshot=load_snapshot(folder)
        self.assertIn('Duplicate JSON key',str(snapshot))
    def test_explicit_null_config_is_not_treated_as_omitted(self):
        package=f.initialize(self.base/'system',True)
        config=self.base/'null.json';config.write_text('null')
        commands=[['sources-audit',str(package),'--as-of','2026-10-21','--provenance',str(config)],
                  ['review',str(package),'--responses',str(ROOT/'examples/responses-good.json'),
                   '--evidence-config',str(config)],
                  ['validate-review',str(config)]]
        for i,args in enumerate(commands):
            output=self.base/f'rejected-{i}.json'
            if args[0]!='validate-review':args+=['--out',str(output)]
            err=io.StringIO()
            with self.subTest(command=args[0]),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(err):
                self.assertEqual(f.main(args),2)
            self.assertNotIn('Traceback',err.getvalue())
            self.assertFalse(output.exists())

    def test_cli_rejects_deep_json_without_traceback_or_output(self):
        path=self.base/'deep.json';path.write_text('['*2000+'0'+']'*2000)
        output=self.base/'result.json';err=io.StringIO()
        with contextlib.redirect_stderr(err):
            code=f.main(['validate-review',str(path)])
        self.assertEqual(code,2)
        self.assertNotIn('Traceback',err.getvalue())
        self.assertIn(path.name,err.getvalue())
        self.assertFalse(output.exists())

if __name__=='__main__':unittest.main()
