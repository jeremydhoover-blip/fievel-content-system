"""Read-only checks of the prepared inputs, never behavioral execution."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
for trial in sorted(root.glob('FB-*')):
    workspace = trial / 'workspace'
    before = json.loads((trial / 'before-manifest.json').read_text(encoding='utf-8'))
    actual = {p.relative_to(workspace).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in workspace.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    assert actual == before, f'{trial.name}: workspace differs from initial hashes'
    record = json.loads((trial / 'run-record.json').read_text(encoding='utf-8'))
    assert record['status'] == 'not_run'
    for turn in record['turns']:
        assert not turn['executed']
        assert turn['canonical_user_turn'] in (trial / turn['file']).read_text(encoding='utf-8')
    package = workspace / 'my-content-system'
    if trial.name == 'FB-03':
        progress = json.loads((package / 'progress.json').read_text(encoding='utf-8'))
        assert progress['decisions'] == ['No renewal tool is available']
        assert progress['open_questions'] == ['Who owns renewal policy?']
        assert progress['next_action'] == 'Inventory the available sources'
        assert progress['stages']['1'] == progress['stages']['2'] == 'drafted'
        assert all(progress['stages'][str(i)] == 'pending' for i in range(3, 8))
        assert json.loads((package / 'evaluation.json').read_text(encoding='utf-8'))['scenarios'] == []
        assert (workspace / 'unrelated-sentinel.txt').exists()
    else:
        assert not package.exists()
    print(f'{trial.name}: prepared input integrity verified; behavioral status not_run')
