const {chromium}=require(process.env.FIEVEL_PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{execFileSync}=require('child_process');
(async()=>{
 const out=path.resolve('.scratch/review-page-qa');fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({headless:true,executablePath:process.env.FIEVEL_BROWSER_EXECUTABLE});
 try{
  const page=await browser.newPage({viewport:{width:1280,height:900},acceptDownloads:true});
  const errors=[],requests=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
  const url=pathToFileURL(path.resolve(process.env.FIEVEL_REVIEW_PAGE||'docs/audits/2026-10-21/review-page/example-v2.html')).href;
  await page.goto(url);
  assert.equal(await page.locator('.card').count(),2);
  assert.equal(await page.locator('#editing').isEnabled(),true);
  await page.locator('[data-status="0"]').selectOption('pass');
  await page.locator('#download').click();assert((await page.locator('#feedback').textContent()).includes('reviewer identity'));
  const data=await page.locator('#review-data').textContent();const original=JSON.parse(data);
  await page.locator('#reviewer').fill('Synthetic browser validator fixture');
  await page.locator('#reviewed-at').fill('2026-10-21T14:30:00+03:00');
  for(let i=0;i<2;i++){
   await page.locator(`[data-status="${i}"]`).selectOption('pass');
   await page.locator(`[data-reason="${i}"]`).fill('Synthetic browser test; not an actual human judgment.');
   await page.locator(`[data-quote="${i}"]`).fill(original.responses['refund-status']);
  }
  await page.locator('[data-quote="0"]').fill('invented quote');await page.locator('#download').click();
  assert((await page.locator('#feedback').textContent()).includes('match the saved response'));
  await page.locator('[data-quote="0"]').fill(original.responses['refund-status']);
  const downloadPromise=page.waitForEvent('download');await page.locator('#download').click();const download=await downloadPromise;
  const destination=path.join(out,'synthetic-validator-input.json');await download.saveAs(destination);
  const saved=JSON.parse(fs.readFileSync(destination,'utf8'));assert.equal(saved.system_sha256,original.system_sha256);assert.equal(saved.config_sha256,original.config_sha256);
  execFileSync('python',['scripts/fievel.py','validate-review',destination,'--require-complete']);
  await page.screenshot({path:path.join(out,'review-desktop.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.screenshot({path:path.join(out,'review-mobile.png'),fullPage:true});
  await page.locator('#reviewer').focus();await page.keyboard.press('Tab');assert.equal(await page.locator('#reviewed-at').evaluate(el=>el===document.activeElement),true);
  const nojs=await browser.newContext({javaScriptEnabled:false});const staticPage=await nojs.newPage();await staticPage.goto(url);assert.equal(await staticPage.locator('.card').count(),2);assert(await staticPage.locator('#download').isDisabled());await nojs.close();
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  fs.writeFileSync('docs/audits/2026-10-21/review-page/browser-results.json',JSON.stringify({checks:['input errors','invalid quote blocked','synthetic download roundtrip passes CLI','immutable hashes preserved','keyboard labels','390px no overflow','no-JS readable disabled form'],errors,externalRequests:requests,syntheticJudgmentsOnly:true},null,2));
  console.log('Review page browser checks passed; downloaded judgments are synthetic test inputs only.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
