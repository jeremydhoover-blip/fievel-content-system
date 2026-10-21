const { chromium } = require(process.env.FIEVEL_PLAYWRIGHT_MODULE || 'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert');
const {pathToFileURL}=require('url');let browser;
(async()=>{
 const out=path.resolve(process.env.FIEVEL_LANDING_OUT||'.scratch/landing-page-02-qa');fs.mkdirSync(out,{recursive:true});
 browser=await chromium.launch({headless:true,executablePath:process.env.FIEVEL_BROWSER_EXECUTABLE||undefined});
 const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[],external=[],layouts=[];
 const url=process.env.FIEVEL_LANDING_URL||pathToFileURL(path.resolve('website/dist/index.html')).href;
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 page.on('request',r=>{if(/^https?:/.test(r.url())&&!r.url().startsWith(new URL(url).origin))external.push(r.url());});
 await page.clock.install();await page.goto(url);
 assert.equal(await page.locator('h1').count(),1);
 assert.equal(await page.locator('.playback button').count(),1);
 assert.equal(await page.locator('.transcript,.map-description').count(),0);
 await page.locator('.watch').click();assert.equal(await page.locator('#playback-state').textContent(),'Ready to play');
 assert.equal(await page.locator('.actions .primary').getAttribute('href'),'#get-started');
 for(const heading of (await page.locator('h1,h2,h3,title').allTextContents()).filter(Boolean))assert(/^[\p{L}\p{N}\s]+$/u.test(heading),heading);
 for(const file of ['index.html','styles.css','main.js'])assert(!fs.readFileSync(path.join('website/dist',file),'utf8').includes('\u2014'));
 assert.equal(await page.locator('.overline,.eyebrow').count(),0);
 assert.equal(await page.locator('[data-entity]:visible').count(),8);
 {const top=()=>page.locator('.hero h1').evaluate(n=>n.getBoundingClientRect().top-n.closest('.hero').getBoundingClientRect().top);const before=await top();await page.locator('[data-entity="context"]:visible').click();assert(Math.abs(await top()-before)<1,"map selection shifted the hero copy");}
 assert.equal(await page.locator('.ontology-graph:visible .ontology-edges path').count(),8);
 assert(!/booking|refund|behavior\.json|no files are being written/i.test(await page.locator('body').innerText()));
 assert((await page.locator('[data-message="1"]').textContent()).includes("I'm Fievel"));
 for(const [entity,text] of [['standards','voice'],['sources','ground'],['behavior','responsibilities'],['skills','workflows'],['evaluations','scenarios'],['governance','ownership'],['context','who you serve'],['tools','MCP servers']]){
  await page.locator(`[data-entity="${entity}"]:visible`).click();assert((await page.locator('#entity-detail').textContent()).includes(text));
 }
 await page.locator('[data-entity="behavior"]:visible').hover();assert.equal(await page.locator('.ontology-graph:visible .ontology-edges .is-connected').count(),5);
 await page.locator('[data-entity="governance"]:visible').focus();assert.equal(await page.locator('.ontology-graph:visible .ontology-edges .is-connected').count(),2);
 const repo='https://github.com/jeremydhoover-blip/fievel-content-system';
 for(const link of await page.locator('a[href^="https://github.com/"]').evaluateAll(nodes=>nodes.map(n=>n.href)))assert(link.startsWith(repo));
 for(const id of await page.locator('a[href^="#"]').evaluateAll(nodes=>nodes.map(n=>n.getAttribute('href').slice(1)).filter(Boolean)))assert(await page.locator(`[id="${id}"]`).count());
 assert.equal(await page.locator('.foundation-details,[role=tablist]').count(),0);
 for(const [agent,text] of [['claude','/getting-started'],['copilot','VS Code'],['codex','$getting-started']]){
  const card=page.locator(`[data-agent="${agent}"]`),body=card.locator('details p').first();
  assert(await body.isHidden());assert((await card.locator('.agent-link').getAttribute('href')).startsWith('https://'));
  await card.locator('summary').click();assert(await body.isVisible());assert((await body.textContent()).includes(text));
 }
 assert.equal(await page.locator('[data-agent] details[open]').count(),1);
 assert.equal(await page.locator('[data-agent] .agent-tools strong').allTextContents().then(t=>t.join('|')),'Local MCP server|Hosted MCP server|Repository tools');
 assert.equal(await page.locator('[data-agent] details p').evaluateAll(nodes=>nodes.filter(n=>/validat|untested|\bpilot\b/i.test(n.textContent)).length),0);
 await page.locator('.setup-topics details').first().locator('summary').click();assert(await page.locator('.setup-topics details').first().locator('p').isVisible());await page.locator('.setup-topics details').nth(1).locator('summary').click();assert(await page.locator('.setup-topics details').nth(1).locator('p').isVisible());assert(await page.locator('.setup-topics details').first().locator('p').isHidden());assert.equal(await page.locator('.setup-topics details[open]').count(),1);
 {const band=()=>page.locator('#evaluations').evaluate(n=>n.getBoundingClientRect().height);const before=await band();for(const step of ['rules','scenarios','literal','human','improve']){await page.locator(`[data-eval="${step}"]`).click();assert(Math.abs(await band()-before)<1,'evaluation step changed the section height');}}
 assert.equal(await page.locator('.eval-branches>div').count(),2);for(const [step,text] of [['rules','its own tag'],['scenarios','realistic situations'],['literal','forbidden words'],['human','never fills in'],['improve','check again']]){await page.locator(`[data-eval="${step}"]`).click();assert((await page.locator('#eval-detail').textContent()).includes(text));assert.equal(await page.locator(`[data-eval="${step}"]`).getAttribute('aria-pressed'),'true');}await page.locator('[data-eval="scenarios"]').hover();assert.equal(await page.locator('.eval-connector.is-connected').count(),3);await page.locator('[data-eval="literal"]').hover();assert.equal(await page.locator('.eval-connector.is-connected').count(),2);await page.locator('[data-eval="improve"]').hover();assert.equal(await page.locator('.eval-connector.is-connected').count(),2);
 // A controlled clock verifies that pause preserves the current typing phase and resume delay.
 assert.equal(await page.locator('[data-message]:visible').count(),2);
 await page.locator('#play').click();await page.clock.runFor(2300);
 assert(await page.locator('#typing').isVisible());await page.locator('#play').click();
 const paused=await page.locator('#chat-window').innerText();await page.clock.runFor(7000);assert.equal(await page.locator('#chat-window').innerText(),paused);
 assert.equal(await page.locator('#play').textContent(),'Resume');
 await page.locator('#play').click();await page.clock.runFor(1200);assert.equal(await page.locator('[data-message]:visible').count(),2);await page.clock.runFor(1900);assert(await page.locator('#user-typing').isVisible());assert(await page.locator('#typing').isHidden());await page.screenshot({path:path.join(out,'conversation-playing.png'),fullPage:false});
 await page.clock.runFor(25000);assert(await page.locator('.choice-card').isVisible());
 await page.clock.runFor(40000);assert.equal(await page.locator('#playback-state').textContent(),'Example complete');
 assert.equal(await page.locator('[data-message]:visible').count(),17);assert(await page.locator('.choice-card [data-pick]').isChecked());assert.equal(await page.locator('.choice-card input:checked').count(),1);
 await page.locator('#play').click();await page.clock.runFor(1);assert.equal(await page.locator('[data-message]:visible').count(),1);assert.equal(await page.locator('.choice-card input:checked').count(),0);await page.locator('#play').click();
 await page.emulateMedia({reducedMotion:'reduce'});await page.waitForFunction(()=>document.getElementById('play').disabled);assert.equal(await page.locator('[data-message]:visible').count(),17);assert(await page.locator('.choice-card [data-pick]').isChecked());assert(await page.locator('#play').isDisabled());assert(await page.locator('#typing').isHidden());
 assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');
 await page.emulateMedia({reducedMotion:'no-preference'});await page.waitForFunction(()=>!document.getElementById('play').disabled);assert.equal(await page.locator('[data-message]:visible').count(),2);
 await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>window.copiedText=text}}));
 assert(await page.locator('#path-plugin').isVisible());assert(await page.locator('#path-clone').isHidden());assert.equal(await page.locator('[data-path="plugin"]').getAttribute('aria-pressed'),'true');for(const [id,tool,install] of [['claude-install','Claude Code','claude plugin install'],['codex-install','Codex','codex plugin add']]){await page.locator(`[data-copy="${id}"]`).click();const text=await page.evaluate(()=>window.copiedText);assert(text.includes('marketplace add jeremydhoover-blip/fievel-content-system')&&text.includes(`${install} fievel@fievel-content-system`),text);assert.equal(await page.locator('#copy-status').textContent(),`${tool} install commands copied.`);assert.equal(await page.locator(`[data-copy="${id}"]`).textContent(),'Copied');assert(await page.locator('#copy-status').evaluate(n=>!n.classList.contains('is-visible')));}await page.locator('[data-copy="plugin-prompt"]').click();assert((await page.evaluate(()=>window.copiedText)).startsWith('Start Fievel'));await page.locator('[data-agent="copilot"] .agent-plugin').click();assert(await page.locator('#path-clone').isVisible());assert(await page.locator('#path-plugin').isHidden());await page.locator('[data-agent="codex"] .agent-plugin').click();assert(await page.locator('#path-plugin').isVisible());assert.equal(await page.locator('[data-agent] .agent-plugin[data-plugin]').count(),2);await page.locator('[data-path="clone"]').click();assert.equal(await page.locator('[data-path="clone"]').getAttribute('aria-pressed'),'true');await page.locator('[data-copy="clone-command"]').click();assert.equal(await page.evaluate(()=>window.copiedText),`git clone ${repo}.git`);
 assert.equal(await page.locator('.footer a[href$="LICENSE"]').getAttribute('href'),`${repo}/blob/main/LICENSE`);assert.equal(await page.locator('.footer a[href="./privacy.html"]').count(),1);assert(!/all rights reserved/i.test(await page.locator('.footer').textContent()));
 await page.evaluate(()=>{navigator.clipboard.writeText=async()=>{throw Error('denied');};});await page.locator('[data-copy="first-prompt"]').click();assert((await page.locator('#copy-status').textContent()).includes('Text selected'));assert.equal(await page.evaluate(()=>document.activeElement.id),'first-prompt');
 await page.goto(url);await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.className),'skip');await page.keyboard.press('Enter');assert.equal(await page.evaluate(()=>location.hash),'#main');
 for(const width of [1440,1024,768,390,320]){
  await page.setViewportSize({width,height:1000});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`Overflow at ${width}`);assert.equal(await page.locator('.ontology-graph:visible').count(),1);assert.equal(await page.locator('.ontology-node rect:visible').count(),8);assert.equal(await page.locator('.ontology-graph:visible').evaluate(n=>n.closest('.graph-scroll')?n.closest('.graph-scroll').scrollWidth>n.closest('.graph-scroll').clientWidth+1:false),false,`Map scrolls at ${width}`);for(const area of await page.locator('.copy-field textarea:visible').all())assert(await area.evaluate(n=>n.scrollWidth<=n.clientWidth+1&&n.scrollHeight<=n.clientHeight+1),`Copy field scrolls at ${width}`);
  layouts.push({width,overflow:false,connectedGraph:true});
  if([1440,390].includes(width))await page.screenshot({path:path.join(out,`landing-${width}.png`),fullPage:true});
 }
 const fallback=await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:1000}});await fallback.goto(url);
 assert.equal(await fallback.locator('[data-message]:visible').count(),17);assert.equal(await fallback.locator('.tool-call:visible').count(),10);assert(await fallback.locator('.choice-card [data-pick]').isChecked());assert.equal(await fallback.locator('figcaption strong').textContent(),'Example conversation');assert.equal(await fallback.locator('#typing .thinking-text').textContent(),'Thinking');assert(await fallback.locator('#path-plugin').isVisible());assert(await fallback.locator('#path-clone').isVisible());assert(await fallback.locator('.path-options').isHidden());assert(await fallback.locator('.playback').isHidden());await fallback.close();
 assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
 const result={url,layouts,errors,external,checks:['writing rules','eight content system entities and labeled relationships','map selection keeps the hero copy in place','plugin and clone start paths','removed content breakdown','agent cards with collapsed setup and download links','expandable numbered setup topics and visual evaluation branches','thinking phase pause and resume','tool call activity','question card with a selected option','user typing dots','selectable evaluation steps','evaluation selection keeps the page in place','completion and replay','live reduced motion changes','static no JS fallback','copy success and denial fallback','plugin install commands','MIT license footer','section anchors','skip link','relative assets']};
 fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(result,null,2));await browser.close();console.log(JSON.stringify(result));
})().catch(async error=>{console.error(error);if(browser)await browser.close();process.exitCode=1;});
