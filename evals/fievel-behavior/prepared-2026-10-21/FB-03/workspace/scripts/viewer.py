"""Read-only, offline snapshots of selected Fievel package files."""
from collections import Counter
from datetime import datetime, timezone
import base64
import hashlib
from html import escape
import json
from pathlib import Path

from . import fievel as f

ROOT = Path(__file__).resolve().parents[1]
LESSONS = (
    ('System connections', 'content-design/system-relationships.md'),
    ('Use existing guidelines', 'content-design/using-existing-guidelines.md'),
    ('Instructions and skills', 'ai-fundamentals/instructions-and-skills.md'),
)


def load_snapshot(folder, report=None):
    folder = Path(folder).resolve()
    if not folder.is_dir():
        raise ValueError('Choose an existing content-system folder.')
    schema = f.read(ROOT / 'schemas/content-system.schema.json')
    package, digests, issues = {}, {}, []

    def issue(file, message):
        issues.append({'file': file, 'message': message})

    for name in f.FILES:
        filename = name + '.json'
        try:
            content = (folder / filename).read_bytes()
            digests[filename] = hashlib.sha256(content).hexdigest()
            value = json.loads(content.decode('utf-8-sig'))
            errors = list(f.Draft202012Validator(schema['properties'][name]).iter_errors(value))
            if errors:
                for error in errors[:20]:
                    locator = '/'.join(map(str, error.path)) or '(root)'
                    issue(filename, f'{locator}: {error.message}')
                if len(errors) > 20:
                    issue(filename, f'{len(errors) - 20} additional schema errors omitted.')
            else:
                package[name] = value
        except (ValueError, OSError) as exc:
            issue(filename, str(exc))

    sources = package.get('sources', [])
    source_counts = Counter(s['id'] for s in sources)
    raw_rules = [(kind, index, rule) for kind in ('standards', 'behavior')
                 for index, rule in enumerate(package.get(kind, {}).get('rules', []))]
    rule_counts = Counter(r['id'] for _, _, r in raw_rules)
    scenarios = package.get('evaluation', {}).get('scenarios', [])
    scenario_counts = Counter(s['id'] for s in scenarios)
    for label, counts, filename in (('source', source_counts, 'sources.json'),
                                    ('rule', rule_counts, 'standards.json / behavior.json'),
                                    ('scenario', scenario_counts, 'evaluation.json')):
        for id, count in counts.items():
            if count > 1:
                issue(filename, f'Ambiguous {label} ID {id}: {count} records.')

    def state(count):
        return 'linked' if count == 1 else ('missing' if count == 0 else 'ambiguous')

    checks = []
    for si, scenario in enumerate(scenarios):
        counts = Counter(c['id'] for c in scenario['checks'])
        for id, count in counts.items():
            if count > 1:
                issue('evaluation.json', f'Ambiguous check ID {id} in {scenario["id"]}.')
        for ci, check in enumerate(scenario['checks']):
            target_state = state(rule_counts[check['requirement_id']])
            if target_state != 'linked':
                issue('evaluation.json', f'{target_state.capitalize()} requirement {check["requirement_id"]} for check {check["id"]}.')
            checks.append(dict(check, scenario_id=scenario['id'], situation=scenario['situation'],
                               context=scenario['context'], target_state=target_state,
                               key=f'check-{si}-{ci}', locator=f'scenarios[{si}].checks[{ci}]'))

    rules = []
    for kind, index, rule in raw_rules:
        links = []
        for source_id in rule['source_ids']:
            link_state = state(source_counts[source_id])
            record = next((s for s in sources if s['id'] == source_id), None) if link_state == 'linked' else None
            links.append({'id': source_id, 'state': link_state, 'source': record})
            if link_state != 'linked':
                issue(kind + '.json', f'{link_state.capitalize()} source {source_id} for rule {rule["id"]}.')
        linked_checks = [c for c in checks if c['requirement_id'] == rule['id'] and c['target_state'] == 'linked']
        rules.append(dict(rule, kind=kind, key=f'{kind}-{index}', file=kind+'.json',
                          locator=f'rules[{index}]', source_links=links, checks=linked_checks,
                          uncovered=not linked_checks, ambiguous=rule_counts[rule['id']] != 1))

    system_hash = f.fingerprint(package) if len(package) == len(f.FILES) else None
    report_state = _report(folder, report, system_hash)
    lessons = []
    for title, path in LESSONS:
        try:
            lessons.append({'title': title, 'path': 'knowledge/' + path,
                            'text': (ROOT / 'knowledge' / path).read_text(encoding='utf-8')})
        except OSError as exc:
            issue('knowledge/' + path, str(exc))
    return {'kind': 'fievel_viewer_snapshot', 'viewer_version': '1',
            'generated_at': datetime.now(timezone.utc).isoformat(), 'folder': folder.name,
            'system_sha256': system_hash, 'file_sha256': digests, 'package': package,
            'issues': issues, 'rules': rules, 'checks': checks, 'report': report_state,
            'stages': list(f.STAGES), 'lessons': lessons}


def _report(folder, path, system_hash):
    result = {'state': 'none', 'summary': None, 'results': [], 'responses': {},
              'name': None, 'message': 'No execution report selected. Defined checks are not results.'}
    if path is None:
        return result
    result['name'] = Path(path).name
    try:
        report = f.read(path)
        if not isinstance(report, dict):
            raise ValueError('Report must be a JSON object.')
        if report.get('kind') != 'deterministic_execution':
            result.update(state='unsupported', message='This viewer accepts deterministic execution reports only. Human judgments have not been validated.')
            return result
        if not isinstance(report.get('system_sha256'), str):
            raise ValueError('Missing package identity in the report.')
        if system_hash is None:
            raise ValueError('Cannot match a report to structurally invalid or incomplete package files.')
        if report['system_sha256'] != system_hash:
            result.update(state='stale', message='The selected report describes a different package snapshot. Its totals are not presented as current results.')
            return result
        expected = f.evaluate(folder, report.get('responses'))
        for key in ('target', 'system_sha256', 'responses_sha256', 'summary', 'results'):
            if json.dumps(report.get(key), sort_keys=True) != json.dumps(expected[key], sort_keys=True):
                raise ValueError(f'Report {key} does not reproduce from the selected package and responses.')
        timestamp = report.get('executed_at')
        if not isinstance(timestamp, str) or datetime.fromisoformat(timestamp).tzinfo is None:
            raise ValueError('Missing or invalid execution timestamp with timezone.')
        result.update(state='reproduced', summary=expected['summary'], results=expected['results'],
                      responses=expected['responses'], executed_at=timestamp,
                      message='Literal outcomes reproduce against this package and the embedded saved responses. This does not verify response origin, human judgments or overall quality.')
    except (ValueError, OSError) as exc:
        result.update(state='invalid', message=str(exc))
    return result


def export_viewer(folder, output, report=None):
    output = Path(output)
    if output.suffix.lower() != '.html':
        raise ValueError('Choose a new .html output filename.')
    if output.exists():
        raise FileExistsError('Viewer output already exists; choose a new filename to preserve it.')
    model = load_snapshot(folder, report)
    assets = ROOT / 'viewer'
    css = (assets / 'viewer.css').read_text(encoding='utf-8')
    script = (assets / 'viewer.js').read_text(encoding='utf-8')
    def digest(content):
        return base64.b64encode(hashlib.sha256(content.encode('utf-8')).digest()).decode('ascii')
    csp = (f"default-src 'none'; script-src 'sha256-{digest(script)}'; "
           f"style-src 'sha256-{digest(css)}'; connect-src 'none'; img-src 'none'; "
           "object-src 'none'; base-uri 'none'; form-action 'none'")
    payload = json.dumps(model, ensure_ascii=True).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    title = model['package'].get('product', {}).get('name', 'Content system')
    template = (assets / 'shell.html').read_text(encoding='utf-8')
    replacements = {'@@TITLE@@': escape(title), '@@CSP@@': escape(csp, quote=True),
                    '@@CSS@@': css, '@@DATA@@': payload, '@@SCRIPT@@': script}
    # Replace tokens in the original template only; user strings cannot become tokens.
    import re
    html = re.sub(r'@@(?:TITLE|CSP|CSS|DATA|SCRIPT)@@', lambda match: replacements[match.group()], template)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(html)
    return output.resolve()
