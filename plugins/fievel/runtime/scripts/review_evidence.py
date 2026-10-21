"""Opt-in self-contained human review evidence. No source fetching or model calls."""
from datetime import datetime, timezone
from . import fievel as core

STATES = ('pending', 'not_run', 'pass', 'fail', 'borderline', 'insufficient_evidence')


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label}: nonempty text required')


def keys(value, expected, label):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError(f'{label}: expected fields {sorted(expected)}')


def human_checks(data):
    return {(scenario['id'], check['id']): (scenario, check)
            for scenario in data['evaluation']['scenarios'] for check in scenario['checks']
            if check['method'] == 'human'}


def validate_inputs(data, responses, config):
    core.validate_data(data, require_coverage=True)
    known = {s['id'] for s in data['evaluation']['scenarios']}
    if not isinstance(responses, dict) or not responses or set(responses) - known:
        raise ValueError('Responses must map known scenario IDs to nonempty text')
    for response in responses.values():
        text(response, 'Response')
    keys(config, ['version', 'rubrics', 'source_evidence', 'response_origins'], 'Review configuration')
    if config['version'] != '1.0':
        raise ValueError('Unsupported review configuration version')
    if not isinstance(config['rubrics'], list) or not isinstance(config['source_evidence'], list):
        raise ValueError('Rubrics and source_evidence must be arrays')
    rubrics = {}
    for rubric in config['rubrics']:
        keys(rubric, ['scenario_id', 'check_id', 'why', 'pass', 'fail', 'borderline'], 'Rubric')
        for field, value in rubric.items():
            text(value, 'Rubric ' + field)
        pair = (rubric['scenario_id'], rubric['check_id'])
        if pair in rubrics:
            raise ValueError('Duplicate rubric')
        rubrics[pair] = rubric
    if set(rubrics) != set(human_checks(data)):
        raise ValueError('Rubrics must match every human check exactly')
    sources = {source['id'] for source in data['sources']}
    evidence = {}
    for source in config['source_evidence']:
        keys(source, ['source_id', 'locator', 'excerpt'], 'Source evidence')
        for field, value in source.items():
            text(value, 'Source evidence ' + field)
        if source['source_id'] not in sources or source['source_id'] in evidence:
            raise ValueError('Unknown or duplicate source evidence ID')
        evidence[source['source_id']] = source
    origins = config['response_origins']
    if not isinstance(origins, dict) or set(origins) != set(responses):
        raise ValueError('Response origins must match supplied responses exactly')
    for origin in origins.values():
        keys(origin, ['kind', 'description'], 'Response origin')
        if origin['kind'] not in ('authored_fixture', 'saved_model_response', 'manual', 'unknown'):
            raise ValueError('Unsupported response origin kind')
        if origin['description'] is not None:
            text(origin['description'], 'Response origin description')
        if origin['kind'] != 'unknown':
            text(origin['description'], 'Known response origin description')
    return evidence


def prepare_review(folder, responses, config):
    data = core.validate(folder, require_coverage=True)
    validate_inputs(data, responses, config)
    # Version 1.1 identifies the package by content files only (ADR-007).
    review = {'kind': 'human_review_evidence', 'version': '1.1',
              'prepared_at': datetime.now(timezone.utc).isoformat(),
              'system_snapshot': data, 'system_sha256': core.system_fingerprint(data),
              'responses': responses, 'responses_sha256': core.fingerprint(responses),
              'review_config': config, 'config_sha256': core.fingerprint(config),
              'reviewer': None, 'reviewer_kind': 'human', 'reviewed_at': None,
              'judgments': [{'scenario_id': sid, 'check_id': cid,
                            'status': 'pending' if sid in responses else 'not_run',
                            'rationale': '', 'response_evidence': ''}
                           for sid, cid in human_checks(data)]}
    validate_review(review)
    return review


def timestamp(value, label):
    text(value, label)
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise ValueError(f'{label}: ISO timestamp required') from None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f'{label}: timezone required')


def validate_review(review, folder=None, require_complete=False):
    keys(review, ['kind', 'version', 'prepared_at', 'system_snapshot', 'system_sha256',
                  'responses', 'responses_sha256', 'review_config', 'config_sha256',
                  'reviewer', 'reviewer_kind', 'reviewed_at', 'judgments'], 'Evidence review')
    if review['kind'] != 'human_review_evidence' or review['version'] not in ('1.0', '1.1'):
        raise ValueError('Unsupported evidence review version or kind; regenerate legacy sheets')
    # 1.0 hashed all seven files; 1.1 hashes content files only (ADR-007).
    identity = {'system_sha256': review['system_sha256'],
                'system_scope': core.SYSTEM_SCOPE if review['version'] == '1.1' else None}
    if review['reviewer_kind'] != 'human':
        raise ValueError('AI suggestions cannot be validated as human review')
    timestamp(review['prepared_at'], 'prepared_at')
    data, responses, config = review['system_snapshot'], review['responses'], review['review_config']
    if not core.matches_system(identity, data):
        raise ValueError('system_sha256: snapshot hash mismatch')
    for value, hash_key in [(responses, 'responses_sha256'), (config, 'config_sha256')]:
        if core.fingerprint(value) != review[hash_key]:
            raise ValueError(f'{hash_key}: snapshot hash mismatch')
    evidence = validate_inputs(data, responses, config)
    if folder is not None and not core.matches_system(identity, core.validate(folder)):
        raise ValueError('Review is stale for the current package')
    expected = human_checks(data)
    rules = {r['id']: r for r in data['standards']['rules'] + data['behavior']['rules']}
    if not isinstance(review['judgments'], list):
        raise ValueError('Judgments must be an array')
    seen = set()
    counts = {state: 0 for state in STATES}
    for row in review['judgments']:
        keys(row, ['scenario_id', 'check_id', 'status', 'rationale', 'response_evidence'], 'Judgment')
        text(row['scenario_id'], 'Scenario ID')
        text(row['check_id'], 'Check ID')
        pair = (row['scenario_id'], row['check_id'])
        if pair not in expected or pair in seen:
            raise ValueError('Unknown or duplicate judgment')
        seen.add(pair)
        status = row['status']
        if not isinstance(status, str) or status not in STATES:
            raise ValueError('Unsupported judgment status')
        counts[status] += 1
        if not isinstance(row['rationale'], str) or not isinstance(row['response_evidence'], str):
            raise ValueError('Rationale and response_evidence must be text')
        response = responses.get(pair[0])
        if response is None:
            if status != 'not_run' or row['rationale'] or row['response_evidence']:
                raise ValueError('Missing response must stay not_run without judgment evidence')
        elif status == 'not_run':
            raise ValueError('Supplied response cannot be marked not_run')
        elif status == 'pending':
            if row['rationale'] or row['response_evidence']:
                raise ValueError('Pending judgments must not contain completed evidence')
        else:
            text(review['reviewer'], 'Reviewer')
            timestamp(review['reviewed_at'], 'reviewed_at')
            text(row['rationale'], 'Rationale')
            text(row['response_evidence'], 'Response evidence')
            if row['response_evidence'] not in response:
                raise ValueError('Response evidence must quote an exact excerpt of the supplied response')
            if status in ('pass', 'fail'):
                rule = rules[expected[pair][1]['requirement_id']]
                if set(rule['source_ids']) - set(evidence):
                    raise ValueError('Decision requires source evidence; use insufficient_evidence')
                if config['response_origins'][pair[0]]['kind'] == 'unknown':
                    raise ValueError('Decision requires a recorded response origin')
    if seen != set(expected):
        raise ValueError('Missing human check judgments')
    if review['reviewer'] is not None:
        text(review['reviewer'], 'Reviewer')
    if review['reviewed_at'] is not None:
        timestamp(review['reviewed_at'], 'reviewed_at')
        text(review['reviewer'], 'Reviewer')
    if require_complete and (not expected or any(counts[s] for s in STATES if s not in ('pass', 'fail'))):
        raise ValueError('Review incomplete: every human check needs a pass or fail decision')
    return counts
