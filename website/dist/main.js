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
 governance: 'Governance defines ownership, approval and review so knowledge and instructions can be maintained as your system changes.'
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
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
 const field=get(button.dataset.copy), status=get('copy-status');
 try {
  if(!navigator.clipboard?.writeText) throw Error('Clipboard unavailable');
  await navigator.clipboard.writeText(field.value);
  status.textContent=`${button.dataset.label||'Text'} copied.`;
 } catch {field.focus();field.select();status.textContent='Text selected. Use your device copy command to copy it.';}
}));
// A single owned timer makes pause and replay deterministic and cancellable.
const messages=[...document.querySelectorAll('[data-message]')];
const chat=get('chat-window'), typing=get('typing'), play=get('play');
const motion=window.matchMedia('(prefers-reduced-motion: reduce)');
let timer=null, remaining=0, deadline=0, eventIndex=0, state='ready';
const events=[
 {delay:0,visible:1,dots:false},
 {delay:2200,visible:1,dots:true},
 {delay:1200,visible:2,dots:false},
 {delay:3500,visible:3,dots:false},
 {delay:2500,visible:3,dots:true},
 {delay:1200,visible:4,dots:false},
 {delay:3500,visible:5,dots:false},
 {delay:2500,visible:5,dots:true},
 {delay:1200,visible:6,dots:false},
 {delay:4000,visible:6,dots:false,done:true}
];
function cancel(){if(timer!==null)clearTimeout(timer);timer=null;}
function show(visible,dots){
 messages.forEach((message,index)=>{const wasHidden=message.hidden;message.hidden=index>=visible;message.classList.toggle('entering',wasHidden&&!message.hidden&&state==='playing');});
 typing.hidden=!dots;
 chat.scrollTop=chat.scrollHeight;
}
function controls(){
 play.textContent=state==='playing'?'Pause':state==='paused'?'Resume':state==='ended'?'Play again':'Play example';
 play.disabled=motion.matches;
 play.dataset.state=motion.matches?'static':state;
 get('playback-state').dataset.state=play.dataset.state;
 typing.style.animationPlayState=state==='paused'?'paused':'running';
 typing.querySelectorAll('i').forEach(dot=>dot.style.animationPlayState=state==='paused'?'paused':'running');
 get('playback-state').textContent=motion.matches?'Static view for reduced motion':({ready:'Ready to play',playing:'Playing',paused:'Paused',ended:'Example complete'}[state]);
}
function schedule(delay){remaining=delay;deadline=performance.now()+delay;timer=setTimeout(advance,delay);}
function advance(){
 timer=null;if(state!=='playing')return;
 const event=events[eventIndex];show(event.visible,event.dots);eventIndex++;
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
 if(motion.matches){show(6,false);chat.scrollTop=chat.scrollHeight;}
 else {show(2,false);chat.scrollTop=0;}
 controls();
}
motion.addEventListener('change',applyMotion);
document.querySelector('.playback').hidden=false;
applyMotion();

// Highlight real graph relationships on hover, keyboard focus and selection.
const graphLinks = [ ['context','standards'], ['sources','behavior'], ['standards','behavior'], ['behavior','skills'], ['evaluations','behavior'], ['governance','skills'], ['governance','sources'] ];
const graphPaths = [...document.querySelectorAll('.ontology-edges path')];
function highlightConnections(key){graphPaths.forEach((path,index)=>path.classList.toggle('is-connected',graphLinks[index].includes(key)));}
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
 document.querySelectorAll('.demo,.setup-companion,.evaluation-flow,.agent-options,.start-steps').forEach(element=>reveals.observe(element));
}
document.querySelectorAll('.setup-topics details').forEach(details=>details.addEventListener('toggle',()=>{if(details.open)entrance(details.querySelector('p'));}));
motion.addEventListener('change',()=>{if(motion.matches)decorativeAnimations.forEach(animation=>animation.cancel());});
