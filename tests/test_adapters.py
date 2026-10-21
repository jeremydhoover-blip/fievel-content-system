import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.adapters import sync_adapters

class AdapterOwnershipTests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".scratch").mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.scratch')
        self.root=Path(self.temp.name)
        def cleanup():
            assert self.root.resolve().is_relative_to((ROOT/'.scratch').resolve())
            self.temp.cleanup()
        self.addCleanup(cleanup)
        self.canonical=self.root/'.agents/skills/one/SKILL.md'
        self.canonical.parent.mkdir(parents=True)
        self.canonical.write_text('original\n',encoding='utf-8')
        self.generated=self.root/'.claude/skills/one/SKILL.md'
    def snapshot(self):
        return {p.relative_to(self.root).as_posix():p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
    def test_initial_sync_and_source_update(self):
        self.assertEqual(sync_adapters(self.root),3)
        self.assertEqual(sync_adapters(self.root,True),3)
        self.canonical.write_text('updated\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'drift'):
            sync_adapters(self.root,True)
        sync_adapters(self.root)
        self.assertEqual(self.generated.read_text(),'updated\n')
    def test_retired_skill_blocks_check_and_sync_without_writes(self):
        sync_adapters(self.root)
        self.canonical.unlink()
        before=self.snapshot()
        for check in (True,False):
            with self.assertRaisesRegex(ValueError,'Stale'):
                sync_adapters(self.root,check)
            self.assertEqual(before,self.snapshot())
    def test_rename_retains_old_copy_until_manual_resolution(self):
        sync_adapters(self.root)
        target=self.root/'.agents/skills/two/SKILL.md'
        target.parent.mkdir(parents=True)
        self.canonical.rename(target)
        with self.assertRaisesRegex(ValueError,'Stale'):
            sync_adapters(self.root)
        self.generated.unlink()  # Explicit fixture simulation of manual resolution.
        sync_adapters(self.root)
        self.assertTrue((self.root/'.claude/skills/two/SKILL.md').exists())
        self.assertNotIn('.claude/skills/one/SKILL.md',json.loads((self.root/'.claude/fievel-adapters.json').read_text())['files'])
    def test_unrelated_and_modified_files_preserved(self):
        sync_adapters(self.root)
        unrelated=self.root/'.claude/skills/personal/SKILL.md'
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text('personal skill')
        self.assertEqual(sync_adapters(self.root,True),3)
        self.generated.write_text('user changes')
        before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'Locally modified'):
            sync_adapters(self.root)
        self.assertEqual(before,self.snapshot())
    def test_identical_legacy_copy_adopted_and_missing_manifest_detected(self):
        self.generated.parent.mkdir(parents=True)
        self.generated.write_text('original\n')
        with self.assertRaisesRegex(ValueError,'manifest missing'):
            sync_adapters(self.root,True)
        sync_adapters(self.root)
        self.assertEqual(sync_adapters(self.root,True),3)
    def test_conflicting_unowned_copy_blocks_all_writes(self):
        self.generated.parent.mkdir(parents=True)
        self.generated.write_text('unrelated content')
        before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'Unowned'):
            sync_adapters(self.root)
        self.assertEqual(before,self.snapshot())
    def test_malicious_or_unsupported_manifest_rejected(self):
        sync_adapters(self.root)
        path=self.root/'.claude/fievel-adapters.json'
        for relative in ('../outside','.claude/skills/../SKILL.md','C:/elsewhere','.claude/fievel-adapters.json'):
            path.write_text(json.dumps({'version':'1.0','files':{relative:'0'*64}}))
            with self.subTest(relative=relative),self.assertRaises(ValueError):
                sync_adapters(self.root)
    def test_missing_owned_copy_is_restored(self):
        sync_adapters(self.root)
        self.generated.unlink()
        with self.assertRaises(ValueError):sync_adapters(self.root,True)
        sync_adapters(self.root)
        self.assertEqual(self.generated.read_text(),'original\n')

if __name__=='__main__':unittest.main()
