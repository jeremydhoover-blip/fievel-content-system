import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import fievel as f
from scripts.review_evidence import prepare_review
from scripts.review_page import export_review_page

class ReviewPageTests(unittest.TestCase):
    def setUp(self):
        (ROOT/'.scratch').mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.scratch');self.base=Path(self.temp.name)
        def cleanup():
            assert self.base.resolve().is_relative_to((ROOT/'.scratch').resolve())
            self.temp.cleanup()
        self.addCleanup(cleanup)
        self.review=prepare_review(ROOT/'examples/wayfarer',f.read(ROOT/'examples/responses-good.json'),f.read(ROOT/'examples/review-evidence-config.json'))
    def save(self):
        path=self.base/'review.json';f.write_new(path,self.review);return path
    def test_page_preserves_inputs_and_refuses_overwrite(self):
        path=self.save();before=path.read_bytes();out=self.base/'review.html'
        export_review_page(path,out)
        self.assertEqual(before,path.read_bytes())
        html=out.read_text(encoding='utf-8')
        self.assertIn('No automatic saving',html)
        self.assertIn('connect-src &#x27;none&#x27;',html)
        self.assertIn('no-refund-promise',html)
        with self.assertRaises(FileExistsError):export_review_page(path,out)
    def test_unsafe_text_is_escaped_in_visible_and_embedded_data(self):
        unsafe='</script><img src=x onerror=alert(1)>'
        self.review['system_snapshot']['product']['name']=unsafe
        self.review['system_sha256']=f.fingerprint(self.review['system_snapshot'])
        path=self.save();out=self.base/'safe.html';export_review_page(path,out)
        html=out.read_text(encoding='utf-8')
        self.assertNotIn(unsafe,html)
        self.assertIn('&lt;/script&gt;',html)
        self.assertIn('\\u003c/script',html)
    def test_cli_rejects_legacy_and_wrong_suffix_before_writing(self):
        path=self.base/'legacy.json';f.write_new(path,{'kind':'human_review'})
        out=self.base/'invalid.html'
        with contextlib.redirect_stderr(io.StringIO()),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(f.main(['review-page',str(path),'--out',str(out)]),2)
        self.assertFalse(out.exists())
        path=self.save()
        with self.assertRaises(ValueError):export_review_page(path,self.base/'bad.txt')
    def test_missing_response_remains_not_run_and_uneditable(self):
        config=f.read(ROOT/'examples/review-evidence-config.json')
        config['response_origins']={'refund-status':config['response_origins']['refund-status']}
        self.review=prepare_review(ROOT/'examples/wayfarer',{'refund-status':'No status available'},config)
        out=self.base/'partial.html';export_review_page(self.save(),out)
        html=out.read_text(encoding='utf-8')
        self.assertIn('No response supplied',html)
        self.assertIn('<fieldset disabled>',html)
        self.assertEqual(sum(j['status']=='not_run' for j in self.review['judgments']),4)

if __name__=='__main__':unittest.main()
