// tiny helpers shared by all simulators
const $=id=>document.getElementById(id);
function css(n){return getComputedStyle(document.documentElement).getPropertyValue(n).trim()}
function setup(cv,aspect){ // returns ctx scaled to CSS pixels
  const dpr=window.devicePixelRatio||1;
  function fit(){const w=cv.clientWidth,h=Math.round(w*aspect);cv.style.height=h+'px';cv.width=w*dpr;cv.height=h*dpr;const c=cv.getContext('2d');c.setTransform(dpr,0,0,dpr,0,0);cv.W=w;cv.H=h;cv.ctx=c;if(cv.onfit)cv.onfit()}
  fit();new ResizeObserver(()=>{fit()}).observe(cv);return cv;
}
function slider(parent,label,min,max,step,val,cb,fmt){
  const l=document.createElement('label');const o=document.createElement('output');
  const i=document.createElement('input');i.type='range';i.min=min;i.max=max;i.step=step;i.value=val;
  const f=fmt||(v=>(+v).toFixed(step<1?2:0));o.textContent=f(val);
  i.oninput=()=>{o.textContent=f(i.value);cb(+i.value)};
  l.append(label+' ',i,o);parent.append(l);return i;
}
function btn(parent,label,cb,alt){const b=document.createElement('button');b.textContent=label;if(alt)b.className='alt';b.onclick=cb;parent.append(b);return b}
function gauss(){let u=0,v=0;while(!u)u=Math.random();while(!v)v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}
function pos(cv,e){const r=cv.getBoundingClientRect();const t=e.touches?e.touches[0]:e;return[t.clientX-r.left,t.clientY-r.top]}
function drag(cv,onDown,onMove){let on=false;
  cv.addEventListener('pointerdown',e=>{on=true;cv.setPointerCapture(e.pointerId);const p=pos(cv,e);onDown&&onDown(p[0],p[1])});
  cv.addEventListener('pointermove',e=>{if(on){const p=pos(cv,e);onMove(p[0],p[1])}});
  cv.addEventListener('pointerup',()=>on=false)}
function loop(fn){let last=performance.now();function f(t){const dt=Math.min(0.05,(t-last)/1000);last=t;fn(dt);requestAnimationFrame(f)}requestAnimationFrame(f)}
// follow the site's light/dark toggle when embedded
try{const pd=parent.document.documentElement,sync=()=>document.documentElement.setAttribute('data-theme',pd.getAttribute('data-theme')||'');sync();new MutationObserver(sync).observe(pd,{attributes:true,attributeFilter:['data-theme']})}catch(e){}
