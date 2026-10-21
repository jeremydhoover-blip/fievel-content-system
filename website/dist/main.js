'use strict';
document.body.classList.add('js');
const get = id => document.getElementById(id);
const entityText = {
 context: 'Product context defines who you serve, what they need and what your experience should achieve. It shapes your content standards.',
 standards: 'Content standards capture your voice, terminology and writing patterns. They guide how your AI communicates and behaves.',
 sources: 'Knowledge sources hold the information your AI can draw from, along with its authority and permitted use. They ground AI behavior.',
 behavior: 'AI behavior defines responsibilities, boundaries, clarification and recovery. It is guided by your standards and grounded in your sources.',
 skills: 'Instructions and skills turn guidance into reusable directions and task workflows for your agent. They need to reflect your intended behavior.',
 evaluations: 'Evaluations connect your rules to scenarios, checks and review so you can assess behavior and identify what needs improvement.',
 governance: 'Governance defines ownership, approval and review so knowledge and instructions can be maintained as your system changes.',
 tools: 'Tools and connectors, such as MCP servers, give your AI data and actions. Your behavior rules decide when it may use them, and your checks confirm it does.'
};
function selectEntity(button) {
 document.querySelectorAll('[data-entity]').forEach(item => item.setAttribute('aria-pressed', String(item.dataset.entity === button.dataset.entity)));
 get('entity-title').textContent = button.getAttribute('aria-label');
 get('entity-title').hidden = false;
 get('entity-empty-logo').hidden = true;
 get('entity-description').textContent = entityText[button.dataset.entity];
}
document.querySelectorAll('[data-entity]').forEach(button => {
 button.addEventListener('click',()=>selectEntity(button));
 if(button.tagName.toLowerCase()==='g') button.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();selectEntity(button);}});
});
// Directory listing pages. Leave empty until a listing is live; links then fall back to the install steps.
const pluginListings = { claude: '', codex: '' };
document.querySelectorAll('[data-plugin]').forEach(link => {
 const url = pluginListings[link.dataset.plugin];
 if (!url) return;
 link.href = url; link.target = '_blank'; link.rel = 'noopener';
 link.textContent = 'Get the Fievel plugin'; delete link.dataset.startPath;
});
document.querySelectorAll('[data-plugin-icon]').forEach(link => {
 const url = pluginListings[link.dataset.pluginIcon];
 if (url) link.href = url;
});
function choosePath(name) {
 document.querySelectorAll('[data-path]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.path === name)));
 document.querySelectorAll('[data-path-panel]').forEach(panel => { panel.hidden = panel.dataset.pathPanel !== name; });
}
document.querySelectorAll('[data-path]').forEach(button => button.addEventListener('click', () => choosePath(button.dataset.path)));
document.querySelectorAll('[data-start-path]').forEach(link => link.addEventListener('click', () => choosePath(link.dataset.startPath)));
choosePath('plugin');
// Copy fields wrap long commands; size each one to its text where field-sizing is unsupported.
const copyAreas=[...document.querySelectorAll('.copy-field textarea')];
function fitCopyAreas(){copyAreas.forEach(area=>{if(area.offsetParent===null)return;area.style.height='auto';area.style.height=area.scrollHeight+'px';});}
if(!CSS.supports('field-sizing','content')){fitCopyAreas();window.addEventListener('resize',fitCopyAreas);document.querySelectorAll('[data-path]').forEach(button=>button.addEventListener('click',fitCopyAreas));}
// Success shows on the button itself; the status line stays for screen readers and for manual-copy help.
const copyTimers=new Map();
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
 const field=get(button.dataset.copy), status=get('copy-status');
 try {
  if(!navigator.clipboard?.writeText) throw Error('Clipboard unavailable');
  await navigator.clipboard.writeText(field.value);
  status.classList.remove('is-visible');
  status.textContent=`${button.dataset.label||'Text'} copied.`;
  button.textContent='Copied';button.classList.add('is-copied');
  clearTimeout(copyTimers.get(button));
  copyTimers.set(button,setTimeout(()=>{button.textContent='Copy';button.classList.remove('is-copied');},2000));
 } catch {field.focus();field.select();status.classList.add('is-visible');status.textContent='Text selected. Use your device copy command to copy it.';}
}));
// A single owned timer makes pause and replay deterministic and cancellable.
const messages=[...document.querySelectorAll('[data-message]')];
const chat=get('chat-window'), typing=get('typing'), userTyping=get('user-typing'), play=get('play');
const motion=window.matchMedia('(prefers-reduced-motion: reduce)');
let timer=null, remaining=0, deadline=0, eventIndex=0, state='ready';
const events=[
 {delay:0,visible:1},
 {delay:2200,visible:1,dots:true},
 {delay:1200,visible:2},
 {delay:1800,visible:2,user:true},
 {delay:1500,visible:3},
 {delay:1500,visible:3,dots:true},
 {delay:1400,visible:4,dots:true},
 {delay:1500,visible:5},
 {delay:1800,visible:5,user:true},
 {delay:1500,visible:6},
 {delay:1500,visible:6,dots:true},
 {delay:1400,visible:7,dots:true},
 {delay:1500,visible:8},
 {delay:1200,visible:9},
 {delay:2200,visible:9,pick:true},
 {delay:1200,visible:9,dots:true,pick:true},
 {delay:1400,visible:10,dots:true},
 {delay:1500,visible:11},
 {delay:1800,visible:11,user:true},
 {delay:1800,visible:12},
 {delay:1500,visible:12,dots:true},
 {delay:1400,visible:13,dots:true},
 {delay:1500,visible:14},
 {delay:1500,visible:14,user:true},
 {delay:1200,visible:15},
 {delay:1500,visible:15,dots:true},
 {delay:1400,visible:16,dots:true},
 {delay:1500,visible:17},
 {delay:3000,visible:17,done:true}
];
function cancel(){if(timer!==null)clearTimeout(timer);timer=null;}
// The choice card in the example answers itself once the user's pick plays, or whenever it is shown past that point.
const choiceCard=document.querySelector('.choice-card'), choiceIndex=messages.indexOf(choiceCard);
function answerChoice(answered){choiceCard.classList.toggle('is-answered',answered);choiceCard.querySelector('[data-pick]').checked=answered;}
function show(visible,dots,user,pick){
 answerChoice(Boolean(pick)||visible>choiceIndex+1);
 messages.forEach((message,index)=>{const wasHidden=message.hidden;message.hidden=index>=visible;message.classList.toggle('entering',wasHidden&&!message.hidden&&state==='playing');});
 typing.hidden=!dots;
 userTyping.hidden=!user;
 chat.scrollTop=chat.scrollHeight;
}
function controls(){
 play.textContent=state==='playing'?'Pause':state==='paused'?'Resume':state==='ended'?'Play again':'Play example';
 play.disabled=motion.matches;
 play.dataset.state=motion.matches?'static':state;
 get('playback-state').dataset.state=play.dataset.state;
 typing.style.animationPlayState=state==='paused'?'paused':'running';
 [typing,userTyping].forEach(indicator=>indicator.querySelectorAll('*').forEach(part=>part.style.animationPlayState=state==='paused'?'paused':'running'));
 get('playback-state').textContent=motion.matches?'Static view for reduced motion':({ready:'Ready to play',playing:'Playing',paused:'Paused',ended:'Example complete'}[state]);
}
function schedule(delay){remaining=delay;deadline=performance.now()+delay;timer=setTimeout(advance,delay);}
function advance(){
 timer=null;if(state!=='playing')return;
 const event=events[eventIndex];show(event.visible,event.dots,event.user,event.pick);eventIndex++;
 if(event.done){state='ended';controls();return;}
 schedule(events[eventIndex].delay);
}
function start(){
 if(motion.matches)return;
 cancel();eventIndex=0;state='playing';show(0,false);controls();schedule(0);
}
function pause(){if(state!=='playing')return;remaining=Math.max(0,deadline-performance.now());cancel();state='paused';controls();}
play.addEventListener('click',()=>{
 if(state==='playing')pause();
 else if(state==='paused'){state='playing';controls();schedule(remaining);}
 else start();
});
document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
function applyMotion(){
 cancel();state='ready';eventIndex=0;
 if(motion.matches){show(messages.length,false);chat.scrollTop=chat.scrollHeight;}
 else {show(2,false);chat.scrollTop=0;}
 controls();
}
motion.addEventListener('change',applyMotion);
document.querySelector('.playback').hidden=false;
applyMotion();

// Highlight real graph relationships on hover, keyboard focus and selection.
const graphLinks = [ ['context','standards'], ['sources','behavior'], ['standards','behavior'], ['behavior','skills'], ['evaluations','behavior'], ['governance','skills'], ['governance','sources'], ['behavior','tools'] ];
// The wide and phone maps list their edges in the same order as graphLinks.
const graphPaths = [...document.querySelectorAll('.ontology-edges path')];
function highlightConnections(key){graphPaths.forEach((path,index)=>path.classList.toggle('is-connected',graphLinks[index%graphLinks.length].includes(key)));}
function selectedConnections(){highlightConnections(document.querySelector('[data-entity][aria-pressed="true"]')?.dataset.entity);}
document.querySelectorAll('[data-entity]').forEach(node=>{
 node.addEventListener('pointerenter',()=>highlightConnections(node.dataset.entity));
 node.addEventListener('pointerleave',selectedConnections);
 node.addEventListener('focus',()=>highlightConnections(node.dataset.entity));
 node.addEventListener('blur',selectedConnections);
 node.addEventListener('click',selectedConnections);
 node.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' ')selectedConnections();});
});
selectedConnections();
// Content is visible by default. Entrances are progressive enhancement only.
const decorativeAnimations = new Set();
function entrance(element){
 if(motion.matches || !element.animate)return;
 const animation=element.animate([{opacity:.65,transform:'translateY(10px)'},{opacity:1,transform:'translateY(0)'}],{duration:420,easing:'cubic-bezier(.2,.7,.2,1)'});
 decorativeAnimations.add(animation);
 animation.finished.then(()=>decorativeAnimations.delete(animation)).catch(()=>decorativeAnimations.delete(animation));
}
if('IntersectionObserver' in window){
 const reveals=new IntersectionObserver(entries=>entries.forEach(entry=>{
  if(entry.isIntersecting){reveals.unobserve(entry.target);entrance(entry.target);}
 }),{threshold:.12});
 document.querySelectorAll('.demo,.setup-companion,.evaluation-flow,.agent-options,.path-options').forEach(element=>reveals.observe(element));
}
// One topic open at a time: native exclusive accordion via name, with this fallback for older browsers.
const agentMore=[...document.querySelectorAll('[data-agent] details')];
agentMore.forEach(details=>details.addEventListener('toggle',()=>{
 if(details.open)agentMore.forEach(other=>{if(other!==details&&other.open)other.open=false;});
}));
const setupTopics=[...document.querySelectorAll('.setup-topics details')];
setupTopics.forEach(details=>details.addEventListener('toggle',()=>{
 if(!details.open)return;
 setupTopics.forEach(other=>{if(other!==details&&other.open)other.open=false;});
 entrance(details.querySelector('p'));
}));
motion.addEventListener('change',()=>{if(motion.matches)decorativeAnimations.forEach(animation=>animation.cancel());});

// Evaluation steps: select to explain, and light the connectors around a hovered or selected step.
const evalText = {
 rules: 'Each rule has its own tag, so you can always see which check tests which rule.',
 scenarios: 'Scenarios are realistic situations, including unknowns, conflicting sources and requests the AI must decline. Each check inside one links to a rule.',
 literal: 'Automatic checks look for required or forbidden words in saved responses. They catch known slips quickly, but they cannot judge meaning.',
 human: 'People review meaning, tone, accuracy and permissions. Fievel prepares the review sheet and never fills in a judgment for you.',
 improve: 'Results show which rules hold and which need work. Adjust a rule or the prompt, save new responses and check again.'
};
const evalSteps=[...document.querySelectorAll('[data-eval]')], evalLinks=[...document.querySelectorAll('.eval-connector[data-link]')];
// Hidden copies of every step's text share the detail's grid cell, so it is always as tall as the longest one and selecting never moves the page.
const evalDetail=get('eval-detail'), evalFrame=document.createElement('div');
evalFrame.className='eval-detail-frame';evalDetail.before(evalFrame);evalFrame.append(evalDetail);
evalSteps.forEach(step=>{
 const sizer=document.createElement('div');sizer.className='eval-detail eval-sizer';sizer.setAttribute('aria-hidden','true');
 const title=document.createElement('h3'),text=document.createElement('p');
 title.textContent=step.querySelector('strong')?.textContent||step.textContent;text.textContent=evalText[step.dataset.eval];
 sizer.append(title,text);evalFrame.append(sizer);
});
function lightEval(key){evalLinks.forEach(link=>link.classList.toggle('is-connected',Boolean(key)&&link.dataset.link.split(' ').includes(key)));}
function selectedEval(){lightEval(document.querySelector('[data-eval][aria-pressed="true"]')?.dataset.eval);}
evalSteps.forEach(step=>{
 step.addEventListener('click',()=>{
  evalSteps.forEach(item=>item.setAttribute('aria-pressed',String(item===step)));
  get('eval-empty-logo').hidden=true;
  get('eval-title').hidden=false;
  get('eval-title').textContent=step.querySelector('strong')?.textContent||step.textContent;
  get('eval-description').textContent=evalText[step.dataset.eval];
  selectedEval();
 });
 step.addEventListener('pointerenter',()=>lightEval(step.dataset.eval));
 step.addEventListener('pointerleave',selectedEval);
 step.addEventListener('focus',()=>lightEval(step.dataset.eval));
 step.addEventListener('blur',selectedEval);
});
