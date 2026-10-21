'use strict';
const original=JSON.parse(document.getElementById('review-data').textContent);
const get=id=>document.getElementById(id);
get('editing').disabled=false;
let dirty=false;
document.addEventListener('input',()=>{dirty=true;});
document.addEventListener('change',()=>{dirty=true;});
window.addEventListener('beforeunload',event=>{if(dirty){event.preventDefault();event.returnValue='';}});
get('set-time').addEventListener('click',()=>{get('reviewed-at').value=new Date().toISOString();dirty=true;});
get('download').addEventListener('click',()=>{
 const r=JSON.parse(JSON.stringify(original)),errors=[];
 r.reviewer=get('reviewer').value.trim()||null;
 r.reviewed_at=get('reviewed-at').value.trim()||null;
 const validTime=r.reviewed_at&&/T.*(?:Z|[+-]\d{2}:\d{2})$/.test(r.reviewed_at)&&!Number.isNaN(Date.parse(r.reviewed_at));
 const rules=[...r.system_snapshot.standards.rules,...r.system_snapshot.behavior.rules];
 const available=new Set(r.review_config.source_evidence.map(s=>s.source_id));
 for(let i=0;i<r.judgments.length;i++){
  const row=r.judgments[i];
  row.status=get('status-'+i).value;row.rationale=get('reason-'+i).value;row.response_evidence=get('quote-'+i).value;
  if(row.status==='pending'||row.status==='not_run'){
   if(row.rationale||row.response_evidence)errors.push(`Check ${i+1}: select a decision before adding rationale or evidence.`);
   continue;
  }
  if(!r.reviewer||!validTime)errors.push('Enter reviewer identity and a review time including timezone.');
  if(!row.rationale.trim()||!row.response_evidence.trim())errors.push(`Check ${i+1}: rationale and an exact response excerpt are required.`);
  else if(!r.responses[row.scenario_id].includes(row.response_evidence))errors.push(`Check ${i+1}: the excerpt must match the saved response exactly.`);
  if(row.status==='pass'||row.status==='fail'){
   const scenario=r.system_snapshot.evaluation.scenarios.find(s=>s.id===row.scenario_id);
   const check=scenario.checks.find(c=>c.id===row.check_id);
   const rule=rules.find(rule=>rule.id===check.requirement_id);
   if(rule.source_ids.some(id=>!available.has(id)))errors.push(`Check ${i+1}: source evidence is missing; use insufficient evidence.`);
   if(r.review_config.response_origins[row.scenario_id].kind==='unknown')errors.push(`Check ${i+1}: response origin is unknown.`);
  }
 }
 if(r.reviewed_at&&(!validTime||!r.reviewer))errors.push('A valid review time requires reviewer identity and a timezone.');
 if(errors.length){get('feedback').textContent=[...new Set(errors)].join(' ');get('feedback').focus();return;}
 const blob=new Blob([JSON.stringify(r,null,2)+'\n'],{type:'application/json'});
 const url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='human-review.json';link.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
 const unresolved=r.judgments.filter(j=>!['pass','fail'].includes(j.status)).length;
 get('feedback').textContent=`Download requested. ${unresolved} unresolved checks. Validate the saved file with the CLI. Downloading does not confirm it was saved.`;
});
