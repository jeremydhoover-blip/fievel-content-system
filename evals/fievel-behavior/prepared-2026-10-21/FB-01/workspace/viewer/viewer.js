(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('snapshot-data').textContent);
  const P = data.package;
  const get = id => document.getElementById(id);
  const names = { overview: 'Overview', connections: 'Rules & connections', sources: 'Sources', checks: 'Checks & results', files: 'Project health' };
  const node = (tag, text, className) => {
    const element = document.createElement(tag);
    if (text !== undefined && text !== null) element.textContent = String(text);
    if (className) element.className = className;
    return element;
  };
  const unknown = value => value === null || value === undefined || value === '' ? 'Not recorded' : String(value);
  const counts = { rules: data.rules.length, sources: (P.sources || []).length, checks: data.checks.length };
  let selectedKey = data.rules[0]?.key || null;
  let visibleLimit = 40;
  const resultIndex = new Map(data.report.results.map(result => [`${result.scenario_id}\0${result.check_id}`, result]));

  function list(parent, values, empty) {
    if (!values.length) { parent.append(node('p', empty, 'muted small')); return; }
    const ul = node('ul');
    values.forEach(value => ul.append(node('li', value)));
    parent.append(ul);
  }
  function row(parent, label, value) {
    const item = node('dl', undefined, 'row');
    item.append(node('dt', label), node('dd', value));
    parent.append(item);
  }
  function action(label, callback, className) {
    const button = node('button', label, className);
    button.type = 'button';
    button.addEventListener('click', callback);
    return button;
  }
  function disclosure(label, children) {
    const details = node('details');
    details.append(node('summary', label), ...children);
    return details;
  }
  function address(view, key) {
    return `#${view}${view === 'connections' && key ? `?rule=${encodeURIComponent(key)}` : ''}`;
  }
  function applyRoute() {
    if (location.hash === '#main') return;
    const [candidate, query] = location.hash.slice(1).split('?');
    const view = Object.hasOwn(names, candidate) ? candidate : 'overview';
    const key = new URLSearchParams(query || '').get('rule');
    if (key && data.rules.some(rule => rule.key === key)) {
      selectedKey = key;
      if (!matchingRules().some(rule => rule.key === key)) {
        get('rule-search').value = '';
        get('rule-kind').value = 'all';
      }
    }
    document.querySelectorAll('[data-panel]').forEach(panel => panel.hidden = panel.dataset.panel !== view);
    document.querySelectorAll('[data-view]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === view)));
    get('view-status').textContent = names[view];
    document.title = `${names[view]} · ${P.product?.name || data.folder}`;
    if (view === 'connections') renderRules();
  }
  function navigate(view, key = selectedKey, focus = false) {
    if (key) selectedKey = key;
    const hash = address(view, selectedKey);
    if (location.hash !== hash) history.pushState(null, '', hash);
    applyRoute();
    if (focus) {
      if (view === 'connections') get('rule-search').focus();
      else {
        const heading = document.querySelector(`[data-panel="${view}"] h1`);
        heading.setAttribute('tabindex', '-1');
        heading.focus();
      }
    }
  }
  const jump = (label, view, className) => action(label, () => navigate(view, selectedKey, true), className);
  document.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => navigate(button.dataset.view)));
  window.addEventListener('popstate', applyRoute);
  window.addEventListener('hashchange', applyRoute);

  get('project-name').textContent = P.product?.name || data.folder;
  get('overview-title').textContent = P.product?.name || 'Product information unavailable';
  get('purpose').textContent = P.product?.purpose || 'Your product context could not be read. Open Project health to see what needs repair.';
  const date = new Date(data.generated_at);
  const shortDate = new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric', timeZone: 'UTC' }).format(date);
  const fullDate = new Intl.DateTimeFormat('en', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'UTC' }).format(date);
  get('header-date').textContent = shortDate;
  get('snapshot-date').textContent = `Generated ${fullDate} UTC · version ${unknown(P.governance?.version)}`;
  document.querySelectorAll('[data-count]').forEach(element => element.textContent = counts[element.dataset.count]);
  if (data.issues.length) {
    const banner = node('div', undefined, 'notice attention');
    banner.append(node('h2', `${data.issues.length} item${data.issues.length === 1 ? '' : 's'} need attention`), node('p', 'Some saved information or connections could not be read reliably.'), jump('See what needs repair', 'files', 'text-button'));
    get('banner').append(banner);
  }

  const drafts = data.rules.filter(rule => rule.status === 'draft').length;
  const summaries = [
    { count: counts.rules, label: 'Rules', note: `${drafts} draft · ${counts.rules - drafts} labeled approved`, view: 'connections' },
    { count: counts.sources, label: 'Sources', note: 'Evidence to inspect', view: 'sources' },
    { count: counts.checks, label: 'Quality checks', note: data.report.state === 'reproduced' ? 'Report outcomes reproduced' : 'Definitions, not results', view: 'checks' }
  ];
  summaries.forEach(item => {
    const button = action('', () => navigate(item.view, selectedKey, true), 'inventory-item');
    button.setAttribute('aria-label', `${item.label}: ${item.count}. ${item.note}`);
    button.append(node('span', item.label, 'metric-label'), node('span', item.count, 'metric'), node('span', item.note, 'metric-note'));
    get('inventory').append(button);
  });
  // Shapes encode recorded structure, never an inferred quality score.
  const svgNS = 'http://www.w3.org/2000/svg';
  function svgElement(tag, attrs, text) {
    const element = document.createElementNS(svgNS, tag);
    Object.entries(attrs).forEach(([key,value]) => element.setAttribute(key, String(value)));
    if (text !== undefined) element.textContent = text;
    return element;
  }
  const diagram = node('section', undefined, 'surface architecture');
  diagram.append(node('h2', 'System at a glance'));
  const svg = svgElement('svg', {viewBox:'0 0 700 230', role:'img', 'aria-label': `${counts.sources} sources connect to ${counts.rules} recorded rules and ${counts.checks} defined quality checks. Lines show categories, not individual verified links.`});
  svg.append(svgElement('path',{d:'M170 115 C235 115 235 65 300 65 M170 115 C235 115 235 165 300 165 M450 65 C510 65 510 115 560 115 M450 165 C510 165 510 115 560 115',fill:'none',stroke:'currentColor','stroke-width':2, class:'diagram-lines'}));
  const groups = [[20,80,150,70,'Sources',counts.sources,'sources'],[290,25,170,75,'Content rules',data.rules.filter(r=>r.kind==='standards').length,'connections'],[290,135,170,75,'Behavior rules',data.rules.filter(r=>r.kind==='behavior').length,'connections'],[550,80,145,70,'Checks',counts.checks,'checks']];
  groups.forEach(([x,y,w,h,label,count]) => {
    svg.append(svgElement('rect',{x,y,width:w,height:h,rx:14,class:'diagram-node'}),svgElement('text',{x:x+16,y:y+29,class:'diagram-count'},count),svgElement('text',{x:x+16,y:y+51,class:'diagram-label'},label));
  });
  diagram.append(svg,node('p','Category map · inspect individual links below','small muted'));
  const coverage = node('section', undefined, 'surface coverage');
  coverage.append(node('h2','Recorded connections'));
  function bar(parent,label,value,total,caption) {
    const item = node('div',undefined,'distribution');
    const heading=node('div',undefined,'distribution-heading');heading.append(node('span',label),node('strong',`${value} / ${total}`));
    const track=node('div',undefined,'distribution-track');const fill=node('span');fill.style.width=`${total ? value/total*100 : 0}%`;track.append(fill);
    item.append(heading,track,node('p',caption,'small muted'));parent.append(item);
  }
  bar(coverage,'Rules with source links',data.rules.filter(r=>r.source_links.some(l=>l.state==='linked')).length,counts.rules,'Recorded links, not verified grounding');
  bar(coverage,'Rules with linked checks',data.rules.filter(r=>r.checks.length).length,counts.rules,'Check definitions, not passing results');
  get('visual-summary').append(diagram,coverage);
  const sourceCount=(P.sources||[]).filter(source=>data.rules.some(rule=>rule.source_ids.includes(source.id))).length;
  bar(get('source-summary'),'Sources referenced by rules',sourceCount,counts.sources,'Unreferenced sources remain visible below');
  const humanCount=data.checks.filter(check=>check.method==='human').length;
  bar(get('check-summary'),'Human review questions',humanCount,counts.checks,'Questions requiring contextual judgment');
  bar(get('check-summary'),'Literal checks',counts.checks-humanCount,counts.checks,'Definitions that can run against saved responses');
  const context = get('context');
  row(context, 'Audience', (P.product?.audiences || []).join(' · ') || 'Not recorded');
  row(context, 'Tasks', (P.product?.tasks || []).join(' · ') || 'Not recorded');
  row(context, 'Voice', P.standards?.voice || 'Not recorded');
  row(context, 'Owner', unknown(P.governance?.owner));
  if (P.product?.constraints?.length) row(context, 'Constraints', P.product.constraints.join(' · '));
  if (!data.rules.length) get('system-map').append(node('p', 'No rules are recorded in this snapshot.', 'empty'));
  data.rules.forEach((rule, index) => {
    const line = node('div', undefined, 'map-row');
    const sources = node('div', undefined, 'map-cell');
    rule.source_links.forEach(link => sources.append(node('p', link.state === 'linked' ? link.source.title : `${link.id} · ${link.state}`, link.state === 'linked' ? '' : 'tag attention')));
    if (!rule.source_links.length) sources.append(node('p', 'No source linked', 'muted'));
    const middle = node('div', undefined, 'map-cell map-rule');
    middle.append(node('span', rule.kind === 'standards' ? 'Content standard' : 'AI behavior', 'small muted'), action(rule.instruction, () => navigate('connections', rule.key, true), 'map-rule-button'), node('span', `${rule.id} · ${rule.status}`, 'small muted'));
    const checks = node('div', undefined, 'map-cell');
    if(rule.checks.length) checks.append(disclosure(`${rule.checks.length} linked check${rule.checks.length===1?'':'s'}`, rule.checks.map(check=>node('p',check.question))));
    if (!rule.checks.length) checks.append(node('p', 'No check linked', 'muted'));
    line.append(sources, middle, checks); if(index >= 8) line.hidden=true; get('system-map').append(line);
  });

  if(data.rules.length>8) { const more=action(`Show all ${data.rules.length} rule connections`,()=>{get('system-map').querySelectorAll('.map-row').forEach(row=>row.hidden=false);more.remove();});get('system-map').append(more); }

  function resultLabel(check) {
    const result = resultIndex.get(`${check.scenario_id}\0${check.id}`);
    if (!result) return check.method === 'human' ? 'Human review needed · no judgment loaded' : 'Defined · no current result';
    return result.status === 'not_run' ? 'Not run' : `Literal ${result.status}`;
  }
  function renderCheck(check) {
    const details = node('details', undefined, 'check-group');
    details.append(node('summary', check.question), node('p', resultLabel(check), 'tag'));
    details.append(node('h3', 'Situation'), node('p', check.situation), node('h3', 'Context'), node('p', check.context));
    row(details, 'Method', check.method === 'human' ? 'Human review' : check.method);
    row(details, 'Requirement', `${check.requirement_id} · ${check.target_state}`);
    if (check.method !== 'human') row(details, 'Literal text', check.value);
    if (Object.hasOwn(data.report.responses, check.scenario_id)) details.append(node('h3', 'Saved response'), node('p', data.report.responses[check.scenario_id]));
    details.append(disclosure('File reference', [node('p', `evaluation.json · ${check.locator} · ${check.id}`, 'small muted')]));
    return details;
  }
  const picker = get('rule-picker');
  data.rules.forEach(rule => { const option = node('option', `${rule.id} · ${rule.instruction}`); option.value = rule.key; picker.append(option); });
  picker.disabled = !data.rules.length;
  picker.addEventListener('change', () => navigate('connections', picker.value));
  function matchingRules() {
    const query = get('rule-search').value.trim().toLocaleLowerCase();
    const kind = get('rule-kind').value;
    return data.rules.filter(rule => (kind === 'all' || rule.kind === kind) && `${rule.id} ${rule.instruction}`.toLocaleLowerCase().includes(query));
  }
  function resetFilters() {
    get('rule-search').value = '';
    get('rule-kind').value = 'all';
    visibleLimit = 40;
    renderRules();
    get('rule-search').focus();
  }
  function renderRules() {
    const matches = matchingRules();
    if (!matches.some(rule => rule.key === selectedKey)) selectedKey = matches[0]?.key || null;
    picker.value = selectedKey || '';
    const shown = matches.slice(0, visibleLimit);
    get('rule-results').textContent = `${matches.length} of ${data.rules.length} rules${matches.length > shown.length ? ` · showing ${shown.length}; refine your search or show more` : ''}`;
    const container = get('rule-list');
    container.replaceChildren();
    shown.forEach(rule => {
      const button = action('', () => navigate('connections', rule.key), 'rule-item');
      button.dataset.ruleKey = rule.key;
      button.setAttribute('aria-pressed', String(rule.key === selectedKey));
      const meta = node('span', undefined, 'rule-id');
      meta.append(node('span', rule.id), node('span', rule.kind === 'standards' ? 'Content' : 'Behavior'));
      button.append(meta, node('span', rule.instruction, 'rule-wording'));
      button.addEventListener('keydown', event => {
        if (!['ArrowDown', 'ArrowUp'].includes(event.key)) return;
        const buttons = [...container.querySelectorAll('[data-rule-key]')];
        const index = buttons.indexOf(button) + (event.key === 'ArrowDown' ? 1 : -1);
        if (buttons[index]) { event.preventDefault(); buttons[index].focus(); }
      });
      container.append(button);
    });
    if (matches.length > shown.length) container.append(action('Show more rules', () => {
      const previousLimit = visibleLimit;
      visibleLimit += 40;
      renderRules();
      container.querySelectorAll('[data-rule-key]')[previousLimit]?.focus();
    }));
    const rule = matches.find(item => item.key === selectedKey);
    renderRule(rule);
  }
  function renderRule(rule) {
    const detail = get('rule-detail');
    detail.replaceChildren();
    if (!rule) {
      const empty = node('div', undefined, 'empty');
      empty.append(node('h2', data.rules.length ? 'No matching rules' : 'Your first rule starts here'), node('p', data.rules.length ? 'Try a different phrase, rule ID or type. Your rules have not been removed.' : 'No communication or behavior rules are recorded.'));
      empty.append(data.rules.length ? action('Clear search & filters', resetFilters) : jump('View system overview', 'overview'));
      detail.append(empty);
      return;
    }
    const heading = node('header', undefined, 'rule-heading');
    heading.append(node('span', rule.kind === 'standards' ? 'Content standard' : 'AI behavior', 'badge'), node('span', rule.status, 'badge'), node('h2', rule.instruction));
    heading.append(node('p', `${rule.id} · ${rule.source_links.length} source link${rule.source_links.length === 1 ? '' : 's'} · ${rule.checks.length} linked check${rule.checks.length === 1 ? '' : 's'}`, 'small muted'));
    heading.append(disclosure('Rule details', [node('p', `${rule.file} · ${rule.locator}`, 'small'), node('p', 'Status is the label saved in this package. Independent approver evidence is not recorded in this schema.', 'small muted')]));
    if (rule.ambiguous) heading.append(node('p', 'This ID occurs more than once. Repair it before assigning checks to one rule.', 'tag attention'));
    detail.append(heading);
    const trail = node('div', undefined, 'trail');
    const sources = node('section'); sources.append(node('h2', 'Sources behind this rule', 'node-label'));
    if (!rule.source_links.length) sources.append(node('p', 'No source linked. Keep inferred guidance separate from approved organizational standards.', 'muted'));
    rule.source_links.forEach(link => {
      if (link.state !== 'linked') { sources.append(node('p', `${link.state.toUpperCase()} source: ${link.id}`, 'tag attention'), jump('Inspect the broken connection', 'files', 'text-button')); return; }
      const source = link.source;
      sources.append(node('h3', source.title), node('p', source.authority, 'badge'), node('p', source.purpose, 'muted'));
      const metadata = node('div');
      row(metadata, 'Owner', unknown(source.owner)); row(metadata, 'Review date', unknown(source.reviewed_on));
      row(metadata, 'Permissions', source.permissions); row(metadata, 'Location', source.location); row(metadata, 'Permitted use', source.permitted_use);
      metadata.append(node('p', 'A linked record does not identify an exact supporting passage. Inspect the original source.', 'small muted'));
      sources.append(disclosure('Source details', [metadata]));
    });
    const checks = node('section'); checks.append(node('h2', 'Checks linked to this rule', 'node-label'));
    if (!rule.checks.length) checks.append(node('p', 'No unambiguous check linked yet. Define one when you reach the quality stage.'), jump('View all checks', 'checks', 'text-button'));
    rule.checks.forEach(check => checks.append(renderCheck(check)));
    trail.append(sources, checks); detail.append(trail);
  }
  function filterChanged() {
    visibleLimit = 40;
    renderRules();
    history.replaceState(null, '', address('connections', selectedKey));
  }
  get('rule-search').addEventListener('input', filterChanged);
  get('rule-kind').addEventListener('change', filterChanged);

  if (!(P.sources || []).length) {
    const empty = node('div', undefined, 'empty');
    empty.append(node('h2', 'Start with one source'), node('p', 'No source documents are recorded in this snapshot.'), jump('View system overview', 'overview'));
    get('source-list').append(empty);
  }
  (P.sources || []).forEach(source => {
    const card = node('section', undefined, 'surface');
    card.append(node('p', source.authority, 'badge'), node('h2', source.title), node('p', source.purpose));
    const locationInfo = node('div'); row(locationInfo, 'Owner', unknown(source.owner)); row(locationInfo, 'Location', source.location); card.append(disclosure('Document details', [locationInfo]));
    const extra = node('div'); row(extra, 'Review date', unknown(source.reviewed_on)); row(extra, 'Permissions', source.permissions); row(extra, 'Permitted use', source.permitted_use);
    card.append(disclosure('Source context & permissions', [extra]));
    const rules = data.rules.filter(rule => rule.source_ids.includes(source.id));
    const countBadge = node('div', undefined, 'source-count'); countBadge.append(node('strong', rules.length), node('span', 'linked rules')); card.prepend(countBadge);
    card.append(node('h3', 'Connected rules'));
    const links = node('div', undefined, 'source-links');
    rules.forEach(rule => { const button=action(rule.id, () => navigate('connections', rule.key, true)); button.title=rule.instruction; links.append(button); });
    if (!rules.length) links.append(node('p', 'No rule refers to this source yet.', 'muted small'));
    card.append(links); get('source-list').append(card);
  });

  const reportLabels = { none: 'No execution report selected', reproduced: 'Literal outcomes reproduced', stale: 'This report belongs to an earlier or different system', invalid: 'This report could not be verified', unsupported: 'This report type is not supported yet' };
  const report = get('report-state');
  report.append(node('h2', reportLabels[data.report.state]), node('p', data.report.message));
  if (data.report.name) report.append(node('p', `Selected file: ${data.report.name}`, 'small muted'));
  if (data.report.summary) {
    const metrics = node('div', undefined, 'report-metrics');
    row(metrics, 'Literal passes', data.report.summary.pass); row(metrics, 'Literal failures', data.report.summary.fail); row(metrics, 'Checks not run', data.report.summary.not_run);
    report.append(metrics);
  } else report.append(disclosure('How to include an execution report', [node('p', 'Generate a new snapshot with an explicitly selected saved execution report. No report is loaded automatically.'), node('code', 'python scripts/fievel.py view <folder> --report <execution.json> --out <new.html>')]));
  report.append(node('p', 'Human questions still need contextual review. Reproduced literal outcomes do not establish overall quality.', 'small muted'));
  if (!data.checks.length) get('check-list').append(node('div', 'No situations or checks defined yet. This snapshot has no evaluation definitions.', 'empty'));
  data.checks.forEach(check => get('check-list').append(renderCheck(check)));

  if (data.issues.length) {
    get('diagnostics').append(node('h2', 'Repair these saved files or references'), node('p', 'Ask Fievel to help resolve the items below, then generate a new snapshot. This page does not edit your files.'));
    list(get('diagnostics'), data.issues.map(issue => `${issue.file}: ${issue.message}`), '');
  } else get('diagnostics').append(node('h2', 'No structural issues found'), node('p', 'Files and declared references could be read. Content accuracy, source grounding and approval still need their own review.', 'muted'));
  const filePurposes = { product: 'Who your product serves and what it does.', standards: 'Voice, terminology and writing rules.', sources: 'Evidence records and permitted use.', behavior: 'What the assistant should do and when.', evaluation: 'Scenarios and quality-check definitions.', governance: 'Ownership and review arrangements.', progress: 'Saved decisions, questions and next action.' };
  ['product', 'standards', 'sources', 'behavior', 'evaluation', 'governance', 'progress'].forEach(name => {
    const detail = disclosure(`${name}.json${P[name] === undefined ? ' · unavailable or invalid' : ''}`, [node('p', filePurposes[name]), node('pre', P[name] === undefined ? 'See diagnostics. Invalid content is excluded from the typed view.' : JSON.stringify(P[name], null, 2))]);
    get('file-list').append(detail);
  });
  get('identity').textContent = JSON.stringify({ generated_at: data.generated_at, system_sha256: data.system_sha256, file_sha256: data.file_sha256 }, null, 2);
  renderRules();
  applyRoute();
})();
