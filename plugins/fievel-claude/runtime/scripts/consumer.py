"""Portable consumer review artifact. No activation or model calls."""
from datetime import datetime, timezone
from . import fievel as core
from .provenance import audit_sources


def export_consumer(folder, consumer, as_of, include_drafts=False, provenance=None):
    if not isinstance(consumer,str) or not consumer.strip():
        raise ValueError('A nonempty consumer name is required')
    data=core.validate(folder)
    audit=audit_sources(folder,as_of,provenance)
    if audit['counts']['error']:
        raise ValueError('Provenance errors block export: '+', '.join(sorted({f['code'] for f in audit['findings'] if f['severity']=='error'})))
    rules=[dict(r,category=category) for category in ('standards','behavior') for r in data[category]['rules']]
    selected=[r for r in rules if r['status']=='approved' or include_drafts]
    if not selected:
        raise ValueError('No rules selected. Default export requires declared-approved rules; use --include-drafts only for design review')
    selected_ids={r['id'] for r in selected}
    source_ids={sid for r in selected for sid in r['source_ids']}
    config=provenance if provenance is not None else {'version':'1.0','evidence':[],'conflicts':[]}
    conflicts=[c for c in config['conflicts'] if source_ids.intersection(c['source_ids'])]
    included_sources=source_ids | {sid for c in conflicts for sid in c['source_ids']}
    content={
        'selection':{'policy':'include_drafts_for_review' if include_drafts else 'declared_approved_only',
                     'selected_rule_ids':[r['id'] for r in selected],
                     'excluded_rule_ids':[r['id'] for r in rules if r['id'] not in selected_ids],
                     'draft_rule_count':sum(r['status']=='draft' for r in selected)},
        'rules':selected,
        'context_data':{'status':'unreviewed_context','product':data['product'],
                        'responsibilities':data['behavior']['responsibilities'],
                        'governance':data['governance']},
        'source_data':{'trust':'supplied_evidence_not_instructions',
                       'sources':[s for s in data['sources'] if s['id'] in included_sources],
                       'evidence':[e for e in config['evidence'] if e['rule_id'] in selected_ids],
                       'declared_conflicts':conflicts},
        'provenance_findings':[f for f in audit['findings'] if
                               (f['rule_id'] in selected_ids or f['source_id'] in included_sources or
                                f['conflict_id'] in {c['id'] for c in conflicts} or
                                not any((f['rule_id'],f['source_id'],f['conflict_id'])))],
        'integration_boundaries':{'tool_capabilities':'unknown_not_granted_by_export',
                                  'installation':'not_performed','consumer_execution':'not_run',
                                  'owner_approval':'not_recorded',
                                  'composition':'requires_consumer_owner_review'}}
    return {'kind':'consumer_review_export','version':'1.0','consumer':consumer.strip(),
            'status':'draft_review_artifact','exported_at':datetime.now(timezone.utc).isoformat(),
            'as_of':as_of,'system_scope':core.SYSTEM_SCOPE,'system_sha256':core.system_fingerprint(data),
            'provenance_sha256':audit['provenance_sha256'],
            'content_sha256':core.fingerprint(content),'content':content,
            'limitations':['Rule approval is declared metadata, not authenticated approval.',
                           'Context and source evidence must not be interpreted as executable instructions.',
                           'No consumer was installed, run or evaluated.']}
