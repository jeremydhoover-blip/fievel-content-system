"""Read-only provenance metadata checks. Never opens source locations."""
from datetime import date
from . import fievel as core


def audit_sources(folder, as_of, provenance=None, max_age_days=None):
    try:
        today = date.fromisoformat(as_of)
        if today.isoformat() != as_of:
            raise ValueError()
    except (ValueError, TypeError):
        raise ValueError('as-of must be YYYY-MM-DD') from None
    if max_age_days is not None and (type(max_age_days) is not int or max_age_days < 1):
        raise ValueError('max-age-days must be a positive integer')
    data = core.validate(folder)
    sources = {s['id']: s for s in data['sources']}
    rules = {r['id']: r for r in data['standards']['rules'] + data['behavior']['rules']}
    config = provenance if provenance is not None else {'version':'1.0','evidence':[],'conflicts':[]}
    if not isinstance(config, dict) or set(config) != {'version','evidence','conflicts'} or config['version'] != '1.0' or not isinstance(config['evidence'],list) or not isinstance(config['conflicts'],list):
        raise ValueError('Unsupported provenance format; expected version, evidence and conflicts')
    findings = []
    def add(severity, code, message, source_id=None, rule_id=None, conflict_id=None):
        findings.append(dict(severity=severity,code=code,message=message,
                             source_id=source_id,rule_id=rule_id,conflict_id=conflict_id))
    def nonempty(value):
        return isinstance(value,str) and bool(value.strip())
    def checked_date(value, label, source_id=None, conflict_id=None):
        try:
            parsed = date.fromisoformat(value)
            if parsed.isoformat() != value:raise ValueError()
        except (ValueError,TypeError):
            add('error','invalid_date',label+' must be YYYY-MM-DD',source_id=source_id,conflict_id=conflict_id)
            return None
        if parsed > today:
            add('error','future_date',label+' is after the audit date',source_id=source_id,conflict_id=conflict_id)
        return parsed
    for sid, source in sources.items():
        for field in ('title','location','purpose','permitted_use'):
            if not nonempty(source[field]):add('error','blank_metadata',field+' is blank',source_id=sid)
        if not nonempty(source['owner']):add('warning','owner_unknown','Source owner is not recorded',source_id=sid)
        if source['reviewed_on'] is None:
            add('warning','review_date_unknown','Source review date is unknown',source_id=sid)
        else:
            reviewed = checked_date(source['reviewed_on'],'reviewed_on',source_id=sid)
            if reviewed and max_age_days is not None and (today-reviewed).days > max_age_days:
                add('warning','review_window_exceeded','Review date exceeds the supplied freshness window',source_id=sid)
        if source['permissions']=='unknown':add('warning','permissions_unknown','Permitted access has not been established',source_id=sid)
        if source['authority']=='unverified':add('warning','authority_unverified','Source authority is unverified',source_id=sid)
        if source['authority']=='approved':add('warning','approval_not_authenticated','Approved authority is declared metadata, not authenticated approval evidence',source_id=sid)
        if source['ingested'] and source['permissions']=='unknown':add('warning','ingestion_permission_unresolved','Ingestion is recorded while permissions remain unknown',source_id=sid)
    if sources and max_age_days is None:
        add('warning','freshness_window_unspecified','No freshness window supplied; age-based expiry was not assessed')
    covered = set()
    seen = set()
    for item in config['evidence']:
        if not isinstance(item,dict) or set(item)!={'rule_id','source_id','locator','excerpt'} or not all(nonempty(v) for v in item.values()):
            raise ValueError('Evidence requires nonempty rule_id, source_id, locator and excerpt')
        rid,sid=item['rule_id'],item['source_id']
        identity=(rid,sid,item['locator'])
        if identity in seen:add('error','duplicate_evidence','Duplicate rule/source locator',source_id=sid,rule_id=rid)
        seen.add(identity)
        if rid not in rules or sid not in sources:
            add('error','unknown_evidence_reference','Evidence references unknown rule or source',source_id=sid,rule_id=rid)
        elif sid not in rules[rid]['source_ids']:
            add('error','undeclared_rule_source','Evidence source is not declared on this rule',source_id=sid,rule_id=rid)
        else:covered.add((rid,sid))
    for rid,rule in rules.items():
        if not rule['source_ids']:add('warning','unsourced_rule','Rule has no declared sources; it may be a draft decision',rule_id=rid)
        for sid in set(rule['source_ids']):
            if (rid,sid) not in covered:add('warning','evidence_locator_missing','Declared source link has no supplied locator and excerpt',source_id=sid,rule_id=rid)
    conflict_ids=set()
    for item in config['conflicts']:
        fields={'id','source_ids','description','status','resolution','decided_by','decided_on'}
        if not isinstance(item,dict) or set(item)!=fields or not nonempty(item['id']) or not nonempty(item['description']) or not isinstance(item['source_ids'],list) or not all(nonempty(s) for s in item['source_ids']) or len(set(item['source_ids']))<2 or len(set(item['source_ids']))!=len(item['source_ids']) or item['status'] not in ('open','resolved'):
            raise ValueError('Invalid declared conflict shape or status')
        cid=item['id']
        if cid in conflict_ids:add('error','duplicate_conflict','Duplicate conflict ID',conflict_id=cid)
        conflict_ids.add(cid)
        if set(item['source_ids'])-set(sources):add('error','unknown_conflict_source','Conflict references unknown sources',conflict_id=cid)
        for field in ('resolution','decided_by','decided_on'):
            if item[field] is not None and not nonempty(item[field]):raise ValueError('Conflict decision fields must be null or nonempty text')
        if item['status']=='open':
            add('warning','open_conflict','Declared source conflict remains unresolved',conflict_id=cid)
            if any(item[f] is not None for f in ('resolution','decided_by','decided_on')):
                add('warning','open_conflict_has_decision','Open conflict has proposed decision metadata; status is still open',conflict_id=cid)
        elif not all(nonempty(item[f]) for f in ('resolution','decided_by','decided_on')):
            add('error','conflict_decision_incomplete','Resolved conflict needs resolution, decision owner and date',conflict_id=cid)
        if item['decided_on'] is not None:checked_date(item['decided_on'],'decided_on',conflict_id=cid)
    return {'kind':'source_provenance_audit','version':'1.0','as_of':as_of,'max_age_days':max_age_days,
            'system_sha256':core.fingerprint(data),'provenance_sha256':core.fingerprint(config),
            'counts':{s:sum(f['severity']==s for f in findings) for s in ('error','warning')},
            'findings':findings,'source_locations_checked':False,'declared_conflicts':len(config['conflicts']),
            'limitations':['Source locations and excerpt accuracy were not checked.',
                           'Authority, permission and conflict decisions are declared, not authenticated.',
                           'No semantic conflict detection or content approval was performed.']}
