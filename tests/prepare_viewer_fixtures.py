"""Create fictional packages for optional browser QA in a NEW directory."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import fievel as f, viewer as v


def prepare(destination):
    root = Path(destination)
    root.mkdir(parents=True, exist_ok=False)
    for name in ('normal', 'empty', 'broken', 'malformed', 'stale', 'hostile', 'large'):
        folder = f.initialize(root / name, example=name != 'empty')
        def edit(filename, change):
            path = folder / (filename + '.json')
            data = f.read(path)
            change(data)
            path.write_text(json.dumps(data), encoding='utf-8')
        if name == 'broken':
            edit('behavior', lambda d: d['rules'][0].update(source_ids=['missing-policy']))
            edit('evaluation', lambda d: d['scenarios'][0]['checks'][0].update(requirement_id='unknown-rule'))
        if name == 'malformed':
            (folder / 'product.json').write_text('{broken', encoding='utf-8')
        if name == 'stale':
            edit('product', lambda d: d.update(name='Changed after report'))
        if name == 'hostile':
            edit('product', lambda d: d.update(name='</script><img src="https://example.invalid/leak" onerror="window.ATTACKED=1"><script>window.ATTACKED=1</script>'))
            edit('sources', lambda d: d[0].update(location='javascript:window.ATTACKED=1'))
            edit('evaluation', lambda d: d['scenarios'][0].update(id='constructor'))
        if name == 'large':
            behavior, evaluation = f.read(folder / 'behavior.json'), f.read(folder / 'evaluation.json')
            for i in range(180):
                id = f'additional-{i}'
                behavior['rules'].append({'id': id, 'instruction': f'Draft additional rule {i} for larger-package testing.', 'status': 'draft', 'source_ids': []})
                evaluation['scenarios'].append({'id': f'case-{i}', 'situation': f'Situation {i}', 'context': 'Authored scale fixture', 'checks': [
                    {'id': 'review', 'requirement_id': id, 'question': 'Does the response follow this draft rule?', 'method': 'human', 'value': ''}]})
            (folder / 'behavior.json').write_text(json.dumps(behavior), encoding='utf-8')
            (folder / 'evaluation.json').write_text(json.dumps(evaluation), encoding='utf-8')
        report = ROOT / 'evals/evidence/literal-pass.json' if name in ('normal', 'stale') else None
        v.export_viewer(folder, root / (name + '.html'), report)
    return root.resolve()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python tests/prepare_viewer_fixtures.py <new-directory>')
    print(prepare(sys.argv[1]))
