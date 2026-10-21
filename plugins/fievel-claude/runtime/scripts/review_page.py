"""Generate an offline human review form from a validated evidence package."""
import base64
import hashlib
from html import escape
import json
from pathlib import Path
from . import fievel as core
from .review_evidence import validate_review, human_checks

ROOT=Path(__file__).resolve().parents[1]


def export_review_page(report_path, output):
    review=core.read(report_path)
    validate_review(review)
    output=Path(output)
    if output.suffix.lower()!='.html':raise ValueError('Choose a new .html output')
    def e(value):return escape(str(value),quote=True)
    def display(value):return 'Unknown' if value is None else ('Yes' if value is True else 'No' if value is False else str(value))
    data=review['system_snapshot'];config=review['review_config']
    checks=human_checks(data)
    rules={r['id']:r for r in data['standards']['rules']+data['behavior']['rules']}
    sources={s['id']:s for s in data['sources']}
    rubrics={(r['scenario_id'],r['check_id']):r for r in config['rubrics']}
    evidence={s['source_id']:s for s in config['source_evidence']}
    cards=[]
    for i,row in enumerate(review['judgments']):
        pair=(row['scenario_id'],row['check_id']);scenario,check=checks[pair]
        rule=rules[check['requirement_id']];rubric=rubrics[pair]
        response=review['responses'].get(pair[0]);missing=response is None
        source_html=''
        for sid in rule['source_ids']:
            source_html+='<details><summary>'+e(sources[sid]['title'])+'</summary><dl>'+''.join('<dt>'+e(key.replace('_',' ').capitalize())+'</dt><dd>'+e(display(value))+'</dd>' for key,value in sources[sid].items())+'</dl>'
            passage=evidence.get(sid)
            source_html+=('<p>'+e(passage['locator'])+'</p><blockquote>'+e(passage['excerpt'])+'</blockquote>' if passage else '<p>No source excerpt supplied</p>')+'</details>'
        if not rule['source_ids']:source_html='<p>No sources declared for this rule</p>'
        options=''.join('<option value="'+state+'"'+(' selected' if row['status']==state else '')+'>'+state.replace('_',' ')+'</option>' for state in (['not_run'] if missing else ['pending','pass','fail','borderline','insufficient_evidence']))
        cards.append(f'''<section class="card" aria-labelledby="check-{i}"><h2 id="check-{i}">{e(check['question'])}</h2>
<p class="muted">{e(pair[0])} / {e(pair[1])}</p><h3>Situation and context</h3><p>{e(scenario['situation'])}</p><p>{e(scenario['context'])}</p>
<h3>Saved response</h3><blockquote>{e(response) if response is not None else 'No response supplied; this check cannot be judged'}</blockquote>
<p class="muted">Origin: {e((config['response_origins'][pair[0]]['kind'].replace('_',' ').capitalize()+': '+(config['response_origins'][pair[0]]['description'] or 'Unknown')) if pair[0] in config['response_origins'] else 'No response supplied')}</p>
<h3>Requirement</h3><p>{e(rule['id'])} · {e(rule['status'])}</p><p>{e(rule['instruction'])}</p>
<h3>Assessment criteria</h3><p>{e(rubric['why'])}</p><dl>{''.join('<dt>'+label+'</dt><dd>'+e(rubric[key])+'</dd>' for key,label in [('pass','Pass'),('fail','Fail'),('borderline','Borderline')])}</dl>
<h3>Source evidence</h3>{source_html}<fieldset {'disabled' if missing else ''}><legend>Your judgment</legend>
<label for="status-{i}">Status</label><select id="status-{i}" data-status="{i}">{options}</select>
<label for="reason-{i}">Rationale</label><textarea id="reason-{i}" data-reason="{i}" rows="3">{e(row['rationale'])}</textarea>
<label for="quote-{i}">Exact excerpt from the saved response</label><textarea id="quote-{i}" data-quote="{i}" rows="2">{e(row['response_evidence'])}</textarea></fieldset></section>''')
    css=(ROOT/'review-ui/review.css').read_text(encoding='utf-8')
    script=(ROOT/'review-ui/review.js').read_text(encoding='utf-8')
    def sha(value):return base64.b64encode(hashlib.sha256(value.encode()).digest()).decode()
    csp=f"default-src 'none'; script-src 'sha256-{sha(script)}'; style-src 'sha256-{sha(css)}'; connect-src 'none'; img-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"
    payload=json.dumps(review,ensure_ascii=True).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="{e(csp)}"><title>Review saved responses</title><style>{css}</style></head><body><main>
<h1>Review saved responses</h1><p>Frozen evidence for {e(data['product']['name'])}. Rule status and source authority are declared, not authenticated.</p>
<p>No automatic saving. Download your JSON before closing. Sharing this page shares its embedded evidence.</p><noscript><p>JavaScript is off. Evidence remains readable; editing and download require JavaScript.</p></noscript>
<fieldset id="editing" disabled><legend>Human review</legend><label for="reviewer">Reviewer identity</label><input id="reviewer" value="{e(review['reviewer'] or '')}">
<label for="reviewed-at">Review time with timezone</label><input id="reviewed-at" value="{e(review['reviewed_at'] or '')}" placeholder="YYYY-MM-DDTHH:MM:SS+03:00"><button id="set-time" type="button">Use current time</button>
{''.join(cards)}<button type="button" id="download">Download review JSON</button></fieldset>
<p id="feedback" role="status" tabindex="-1"></p><p>Downloaded records still need <code>python scripts/fievel.py validate-review your-review.json</code>. Use <code>--require-complete</code> only when all checks have pass or fail decisions. Record validity is not a quality verdict.</p>
</main><script type="application/json" id="review-data">{payload}</script><script>{script}</script></body></html>'''
    encoded=html.encode('utf-8')
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('xb') as stream:stream.write(encoded)
    return output.resolve()
