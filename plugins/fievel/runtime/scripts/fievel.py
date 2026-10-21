"""Fievel's local file workflow. No model calls or network access."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.deps'))
try:
    from jsonschema import Draft202012Validator
except ImportError:
    raise SystemExit('Install the validator first: python -m pip install --target .deps -r requirements.txt')

FILES = ('product', 'standards', 'sources', 'behavior', 'evaluation', 'governance', 'progress')
STAGES = ('Understand your product', 'Understand your content', 'Identify your sources',
          'Design AI behavior', 'Define quality', 'Try and improve', 'Maintain your system')


def decode_json(content, label):
    """Reject ambiguous/nonfinite JSON; always identify the input on failure."""
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key!r}')
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError(f'Nonfinite JSON number: {value}')
    try:
        value = json.loads(content.decode('utf-8-sig'), object_pairs_hook=unique_pairs,
                           parse_constant=invalid_constant)
        stack = [(value, 0)]
        while stack:
            node, depth = stack.pop()
            if depth > 128:
                raise ValueError('JSON nesting exceeds the 128-level limit')
            if isinstance(node, dict):
                stack.extend((child, depth + 1) for child in node.values())
            elif isinstance(node, list):
                stack.extend((child, depth + 1) for child in node)
        # Also catches overflowing exponents and escaped lone Unicode surrogates.
        json.dumps(value, ensure_ascii=False, allow_nan=False).encode('utf-8')
        return value
    except RecursionError:
        raise ValueError(f'{label}: JSON nesting is too deep') from None
    except (ValueError, UnicodeError) as exc:
        raise ValueError(f'{label}: invalid JSON or UTF-8: {exc}') from None


def read(path):
    return decode_json(Path(path).read_bytes(), str(path))


def write_new(path, value):
    """Validate serialization before creating an exclusively new report."""
    try:
        payload = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    except (UnicodeError, RecursionError) as exc:
        raise ValueError(f'Cannot serialize output {path}: {exc}') from None
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(payload)


def coverage_gaps(data):
    """Report uncovered rules in an otherwise structurally valid package."""
    requirements = {rule['id'] for rule in data['standards']['rules'] + data['behavior']['rules']}
    covered = {check['requirement_id'] for scenario in data['evaluation']['scenarios']
               for check in scenario['checks']}
    return sorted(requirements - covered)


def validate(folder, require_coverage=False):
    folder = Path(folder)
    data = {name: read(folder / (name + '.json')) for name in FILES}
    return validate_data(data, require_coverage)


def validate_data(data, require_coverage=False):
    schema = read(ROOT / 'schemas/content-system.schema.json')
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: str(e.path))
    if errors:
        raise ValueError('\n'.join(f'{"/".join(map(str, e.path))}: {e.message}' for e in errors))
    def unique(items, label):
        ids = [item['id'] for item in items]
        if len(ids) != len(set(ids)):
            raise ValueError(f'Duplicate {label} IDs')
        return set(ids)
    sources = unique(data['sources'], 'source')
    rules = data['standards']['rules'] + data['behavior']['rules']
    requirements = unique(rules, 'requirement')
    unique(data['evaluation']['scenarios'], 'scenario')
    for rule in rules:
        if not set(rule['source_ids']) <= sources:
            raise ValueError(f'Unknown source for {rule["id"]}')
    for scenario in data['evaluation']['scenarios']:
        unique(scenario['checks'], f'check in {scenario["id"]}')
        for check in scenario['checks']:
            if check['requirement_id'] not in requirements:
                raise ValueError(f'Unknown requirement: {check["requirement_id"]}')
    missing = coverage_gaps(data)
    if require_coverage and missing:
        raise ValueError('Requirements without quality checks: ' + ', '.join(missing))
    return data


def initialize(destination, example=False):
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError('Choose a new folder. Existing folders are never overwritten.')
    source = ROOT / ('examples/wayfarer' if example else 'templates/content-system')
    validate(source)
    shutil.copytree(source, destination)
    return destination


def fingerprint(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def evaluate(folder, responses):
    data = validate(folder, require_coverage=True)
    # Saved responses are a concrete target; this never generates an AI response.
    if not isinstance(responses, dict) or not responses:
        raise ValueError('Provide a nonempty object mapping scenario IDs to saved response text.')
    scenarios = data['evaluation']['scenarios']
    known = {s['id'] for s in scenarios}
    if set(responses) - known or any(not isinstance(v, str) or not v.strip() for v in responses.values()):
        raise ValueError('Responses must use known scenario IDs and nonempty text.')
    rows = []
    for scenario in scenarios:
        response = responses.get(scenario['id'])
        for check in scenario['checks']:
            status = 'not_run'
            if response is not None and check['method'] != 'human':
                found = check['value'].casefold() in response.casefold()
                passed = found if check['method'] == 'contains' else not found
                status = 'pass' if passed else 'fail'
            rows.append({'scenario_id': scenario['id'], 'check_id': check['id'],
                         'requirement_id': check['requirement_id'], 'question': check['question'],
                         'method': check['method'], 'status': status,
                         'reason': 'Human review required' if check['method'] == 'human' else
                         ('No saved response supplied' if response is None else 'Case-insensitive literal substring check')})
    counts = {status: sum(r['status'] == status for r in rows) for status in ('pass', 'fail', 'not_run')}
    return {'kind': 'deterministic_execution', 'executed_at': datetime.now(timezone.utc).isoformat(),
            'target': 'saved_responses', 'system_sha256': fingerprint(data),
            'responses_sha256': fingerprint(responses), 'responses': responses,
            'summary': counts, 'results': rows,
            'limitation': 'Literal checks cannot establish correctness, tone, authorization, or absence of invented facts.'}


def review_sheet(folder, responses):
    report = evaluate(folder, responses)
    return {'kind': 'human_review', 'system_sha256': report['system_sha256'],
            'responses_sha256': report['responses_sha256'], 'reviewer': None, 'reviewed_at': None,
            'responses': responses, 'judgments': [dict(row, status='pending', rationale='')
            for row in report['results'] if row['method'] == 'human']}


def adapters(check=False):
    """Synchronize owned copies, rejecting stale or locally modified outputs."""
    sys.path.insert(0, str(ROOT))
    from scripts.adapters import sync_adapters
    return sync_adapters(ROOT, check)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Fievel: build and check portable content systems locally')
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init', help='Create a draft in a NEW folder')
    init.add_argument('folder')
    init.add_argument('--example', action='store_true', help='Use the complete fictional booking example')
    validate_cmd = commands.add_parser('validate', help='Check draft structure and links; show coverage gaps')
    validate_cmd.add_argument('folder')
    validate_cmd.add_argument('--require-coverage', action='store_true',
                              help='Also fail if any rule lacks a linked quality check')
    commands.add_parser('status').add_argument('folder')
    view = commands.add_parser('view', help='Generate a read-only offline HTML snapshot')
    view.add_argument('folder')
    view.add_argument('--out', required=True, help='New .html file; never overwritten')
    view.add_argument('--report', help='Optional deterministic report to match and reproduce')
    for name in ('check', 'review'):
        cmd = commands.add_parser(name)
        cmd.add_argument('folder')
        cmd.add_argument('--responses', required=True)
        cmd.add_argument('--out', required=True, help='New output file; never overwritten')
    # Evidence review is opt-in; legacy review sheets remain unchanged.
    commands.choices['review'].add_argument('--evidence-config')
    review_page = commands.add_parser('review-page', help='Create a standalone offline evidence review form')
    review_page.add_argument('report')
    review_page.add_argument('--out', required=True)
    review_validation = commands.add_parser('validate-review', help='Validate a saved evidence review; not a content approval')
    review_validation.add_argument('report')
    review_validation.add_argument('--folder', help='Also reject a stale current package')
    review_validation.add_argument('--require-complete', action='store_true')
    consumer_cmd = commands.add_parser('export-consumer', help='Export a review artifact for a named consumer')
    consumer_cmd.add_argument('folder')
    consumer_cmd.add_argument('--consumer', required=True)
    consumer_cmd.add_argument('--as-of', required=True)
    consumer_cmd.add_argument('--out', required=True)
    consumer_cmd.add_argument('--include-drafts', action='store_true')
    consumer_cmd.add_argument('--provenance')
    sources_cmd = commands.add_parser('sources-audit', help='Audit declared source provenance offline')
    sources_cmd.add_argument('folder')
    sources_cmd.add_argument('--as-of', required=True)
    sources_cmd.add_argument('--provenance')
    sources_cmd.add_argument('--max-age-days', type=int)
    sources_cmd.add_argument('--strict', action='store_true')
    sources_cmd.add_argument('--out', help='New report path; never overwritten')
    sync = commands.add_parser('sync')
    sync.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'init':
            print(f'Created draft: {initialize(args.folder, args.example)}')
        elif args.command == 'sync':
            print(f'{adapters(args.check)} generated adapters checked' if args.check else f'{adapters()} adapters synchronized')
        elif args.command == 'validate':
            data = validate(args.folder, require_coverage=args.require_coverage)
            print('Structure and requirement links are valid. This is not content approval.')
            missing = coverage_gaps(data)
            if missing:
                print('Draft rules still needing quality checks: ' + ', '.join(missing))
        elif args.command == 'status':
            data = validate(args.folder)
            progress = data['progress']
            print(f'Path: {progress["path"]}; explanations: {progress["explanations"]}')
            for i, stage in enumerate(STAGES, 1):
                print(f'{i}. {stage}: {progress["stages"][str(i)]}')
            print('Next: ' + progress['next_action'])
            missing = coverage_gaps(data)
            if missing:
                print('Draft rules still needing quality checks: ' + ', '.join(missing))
        elif args.command == 'export-consumer':
            sys.path.insert(0, str(ROOT))
            from scripts.consumer import export_consumer
            provenance = read(args.provenance) if args.provenance else None
            if args.provenance and provenance is None:
                raise ValueError(f'{args.provenance}: provenance configuration must be an object, not null')
            result = export_consumer(args.folder, args.consumer, args.as_of, args.include_drafts, provenance)
            write_new(args.out, result)
            print(f'Saved consumer review artifact: {args.out}')
            print('Draft artifact only; no consumer installed, run or evaluated.')
        elif args.command == 'sources-audit':
            sys.path.insert(0, str(ROOT))
            from scripts.provenance import audit_sources
            provenance = read(args.provenance) if args.provenance else None
            if args.provenance and provenance is None:
                raise ValueError(f'{args.provenance}: provenance configuration must be an object, not null')
            result = audit_sources(args.folder, args.as_of, provenance, args.max_age_days)
            if args.out:
                write_new(args.out, result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1 if result['counts']['error'] or (args.strict and result['counts']['warning']) else 0
        elif args.command == 'review-page':
            sys.path.insert(0, str(ROOT))
            from scripts.review_page import export_review_page
            print(f'Saved offline review page: {export_review_page(args.report, args.out)}')
        elif args.command == 'validate-review':
            sys.path.insert(0, str(ROOT))
            from scripts.review_evidence import validate_review
            counts = validate_review(read(args.report), args.folder, args.require_complete)
            print('Review record valid. This is not content approval or an overall quality verdict.')
            print(json.dumps(counts))
        elif args.command == 'view':
            sys.path.insert(0, str(ROOT))
            from scripts.viewer import export_viewer
            print(f'Saved read-only snapshot: {export_viewer(args.folder, args.out, args.report)}')
            print('Regenerate to a new filename after edits; browser reload does not reread the project.')
        else:
            responses = read(args.responses)
            if args.command == 'review' and args.evidence_config:
                sys.path.insert(0, str(ROOT))
                from scripts.review_evidence import prepare_review
                result = prepare_review(args.folder, responses, read(args.evidence_config))
            else:
                result = evaluate(args.folder, responses) if args.command == 'check' else review_sheet(args.folder, responses)
            write_new(args.out, result)
            print(f'Saved {result["kind"]}: {args.out}')
            if args.command == 'check':
                print(json.dumps(result['summary']))
                rows = result['results']
                executed = result['summary']['pass'] + result['summary']['fail']
                missing = sum(row['scenario_id'] not in responses for row in rows)
                awaiting = sum(row['method'] == 'human' and row['scenario_id'] in responses
                               for row in rows)
                print(f'Executed {executed} of {len(rows)} defined checks; '
                      f'{missing} checks missing saved responses; '
                      f'{awaiting} checks awaiting human review.')
                if not executed:
                    print('No automated checks ran.')
                print('This is not an overall quality verdict. Exit code 0 means no literal failures were found.')
                return 1 if result['summary']['fail'] else 0
    except (ValueError, OSError) as exc:
        print(f'Fievel: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
