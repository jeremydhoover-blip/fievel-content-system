const { chromium } = require(process.env.FIEVEL_PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const fixtureRoot = path.resolve(process.argv[2] || '.scratch/viewer-fixtures');

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: process.env.FIEVEL_BROWSER_EXECUTABLE || undefined });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
  const errors = [], network = [], results = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  page.on('request', request => { if (/^https?:/.test(request.url())) network.push(request.url()); });
  const url = name => 'file:///' + path.join(fixtureRoot, name + '.html').replaceAll('\\', '/');
  const visit = async name => { await page.goto(url(name)); await page.locator('#overview-title').waitFor(); };
  const view = async name => { await page.locator(`[data-view="${name}"]`).click(); };

  await visit('normal');
  assert.equal(await page.locator('#overview-title').textContent(), 'Wayfarer');
  assert.equal(await page.locator('.inventory-item').count(), 3);
  await page.screenshot({ path: path.join(fixtureRoot, 'viewer-overview-wide.png'), fullPage: true });
  assert.equal(await page.locator('.brand-mark').count(), 0);
  assert.equal(await page.locator('#next-action, [data-view="learn"], [data-view="files"]').count(), 0);
  assert.equal(await page.locator('.map-row').count(), 5);
  assert.equal(await page.locator('.architecture svg .diagram-node').count(), 4);
  assert.equal(await page.locator('.coverage .distribution').count(), 2);
  assert.equal(await page.locator('.map-row details[open]').count(), 0);
  await page.locator('.map-rule-button').first().click();
  assert(await page.locator('[data-panel="connections"]').isVisible());
  await view('overview');
  await page.locator('.snapshot-info summary').click();
  assert(await page.getByRole('heading', { name: 'About this snapshot' }).isVisible());
  assert((await page.locator('.snapshot-popover').textContent()).includes('new.html'));
  await page.locator('.snapshot-info summary').click();
  await page.locator('.inventory-item').first().click();
  assert.equal(await page.evaluate(() => document.activeElement.id), 'rule-search');
  await page.locator('#rule-search').fill('refund');
  assert.equal(await page.locator('[data-rule-key]').count(), 1);
  await page.locator('[data-rule-key="behavior-0"]').click();
  assert.equal(await page.locator('#rule-search').inputValue(), 'refund');
  assert((await page.locator('#rule-detail').textContent()).includes('Do not invent a reason'));
  assert.equal(await page.locator('#rule-detail .check-group').count(), 2);
  await page.locator('#rule-search').fill('nothing-matches-this');
  await page.getByRole('heading', { name: 'No matching rules', exact: true }).waitFor();
  await page.getByRole('button', { name: 'Clear search & filters', exact: true }).click();
  assert.equal(await page.locator('[data-rule-key]').count(), 5);
  await page.locator('#rule-kind').selectOption('standards');
  assert.equal(await page.locator('[data-rule-key]').count(), 2);
  await page.locator('#rule-kind').selectOption('all');
  await page.locator('.jump-selector > summary').click();
  await page.locator('#rule-picker').selectOption('behavior-0');
  await page.locator('#rule-picker').focus();
  await page.keyboard.press('ArrowDown');
  assert((await page.locator('#rule-detail').textContent()).includes('Do not claim to cancel'));
  await view('sources');
  assert.equal(await page.locator('#source-list > section').count(), 1);
  await page.locator('.source-links').getByRole('button', { name: 'behavior-1', exact: true }).click();
  assert((await page.locator('#rule-detail').textContent()).includes('Do not invent'));
  await page.goBack();
  await page.locator('[data-panel="sources"]').waitFor({ state: 'visible' });
  await page.goForward();
  await page.locator('[data-panel="connections"]').waitFor({ state: 'visible' });
  await page.goto(url('normal') + '#connections?rule=behavior-2');
  await page.locator('#rule-detail').waitFor();
  assert((await page.locator('#rule-detail').textContent()).includes('When policy evidence conflicts'));
  await view('checks');
  assert((await page.locator('#report-state').textContent()).includes('reproduced'));
  assert((await page.locator('#report-state').textContent()).includes('Checks not run6'));
  results.push({ case: 'normal', interactions: 'overview action, snapshot disclosure, search/filter/reset, retained search on selection, native keyboard selector, source-to-rule navigation, back/forward, direct rule link, report, lesson and diagnostics passed' });

  const layouts = [];
  for (const width of [1024, 736, 360, 320]) {
    await page.setViewportSize({ width, height: 1100 });
    for (const name of ['overview', 'connections', 'sources', 'checks']) {
      await view(name);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
      layouts.push({ width, view: name, overflow });
      assert(!overflow, JSON.stringify({ width, view: name }));
    }
    if (width === 360) {
      await view('connections');
      await page.screenshot({ path: path.join(fixtureRoot, 'viewer-connections-narrow.png'), fullPage: true });
    }
  }
  for (const name of ['empty', 'broken', 'malformed', 'stale', 'hostile', 'large']) {
    await visit(name);
    if (name === 'empty') {
      await view('connections');
      assert(await page.locator('#rule-picker').isDisabled());
      assert((await page.locator('#rule-detail').textContent()).includes('Your first rule'));
    }
    if (name === 'broken') {
      await view('connections');
      await page.locator('#rule-search').fill('behavior-1');
      assert((await page.locator('#rule-detail').textContent()).includes('MISSING source: missing-policy'));
    }
    if (name === 'malformed') {
      assert((await page.locator('#overview-title').textContent()).includes('unavailable'));
      assert(await page.locator('#banner').isVisible());
    }
    if (name === 'stale') {
      await view('checks');
      assert((await page.locator('#report-state').textContent()).includes('earlier or different'));
      assert(!(await page.locator('#report-state').textContent()).includes('Literal passes'));
    }
    if (name === 'hostile') {
      assert.equal(await page.evaluate(() => window.ATTACKED), undefined);
      assert.equal(await page.locator('img').count(), 0);
      assert.equal(await page.locator('a[href^="javascript:"]').count(), 0);
      assert((await page.locator('#overview-title').textContent()).includes('</script>'));
      await view('checks');
      assert.equal(await page.getByRole('heading', { name: 'Saved response', exact: true }).count(), 0);
    }
    if (name === 'large') {
      await view('connections');
      assert.equal(await page.locator('#rule-picker option').count(), 185);
      assert.equal(await page.locator('[data-rule-key]').count(), 40);
      await page.getByRole('button', { name: 'Show more rules', exact: true }).click();
      assert.equal(await page.locator('[data-rule-key]').count(), 80);
      await page.locator('#rule-search').fill('additional-179');
      assert.equal(await page.locator('[data-rule-key]').count(), 1);
      assert((await page.locator('#rule-detail').textContent()).includes('additional-179'));
    }
    results.push({ case: name, status: 'passed' });
  }
  await visit('normal');
  await page.setViewportSize({ width: 1440, height: 1100 });
  await view('connections');
  await page.locator('#rule-search').fill('behavior-1');
  await page.screenshot({ path: path.join(fixtureRoot, 'viewer-connections-wide.png'), fullPage: true });
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.screenshot({ path: path.join(fixtureRoot, 'viewer-connections-dark.png'), fullPage: true });
  assert.equal(errors.length, 0, JSON.stringify(errors));
  assert.equal(network.length, 0, JSON.stringify(network));
  const evidence = { kind: 'real-file-viewer-heuristic-refinement-check', browser: await browser.version(), executed_at: new Date().toISOString(), results, layouts, scriptErrors: errors, unexpectedNetworkRequests: network, limitations: ['Heuristic self-review, not intended-user evidence', 'No independent accessibility/conformance study', 'Snapshots require regeneration'] };
  fs.writeFileSync(path.join(fixtureRoot, 'viewer-browser-results.json'), JSON.stringify(evidence, null, 2));
  console.log(JSON.stringify({ fixtures: results.length, layouts: layouts.length, errors, network }));
  await browser.close();
})().catch(error => { console.error(error); process.exit(1); });
