//TITLE: Qubit and the Bloch sphere
//NOTE: A qubit state is a point on a sphere. |0> is the north pole, |1> the south pole; the equator holds equal superpositions. Apply gates and watch the point move. The bars show the probability of measuring 0 or 1. Drag on the sphere to rotate the view.
const cv=setup($('c'),0.62),ctl=$('k');let a=[1,0],b=[0,0],yaw=0.6,pit=0.35,meas='';
const cm={mul:(x,y)=>[x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]],add:(x,y)=>[x[0]+y[0],x[1]+y[1]]};const s=Math.SQRT1_2;
function apply(m){const na=cm.add(cm.mul(m[0][0],a),cm.mul(m[0][1],b)),nb=cm.add(cm.mul(m[1][0],a),cm.mul(m[1][1],b));a=na;b=nb;meas=''}
const e=(th)=>[Math.cos(th),Math.sin(th)];const Z=[0,0],O=[1,0],I=[0,1];
const G={H:[[[s,0],[s,0]],[[s,0],[-s,0]]],X:[[Z,O],[O,Z]],Y:[[Z,[0,-1]],[I,Z]],Z:[[O,Z],[Z,[-1,0]]],S:[[O,Z],[Z,I]],T:[[O,Z],[Z,e(Math.PI/4)]]};
Object.keys(G).forEach(k=>btn(ctl,k,()=>apply(G[k])));
const rx=th=>[[[Math.cos(th/2),0],[0,-Math.sin(th/2)]],[[0,-Math.sin(th/2)],[Math.cos(th/2),0]]];
btn(ctl,'Rx(30°)',()=>apply(rx(Math.PI/6)),1);btn(ctl,'Reset |0>',()=>{a=[1,0];b=[0,0];meas=''},1);
btn(ctl,'Measure',()=>{const p0=a[0]**2+a[1]**2;if(Math.random()<p0){a=[1,0];b=[0,0];meas='measured 0 (state collapsed to |0>)'}else{a=[0,0];b=[1,0];meas='measured 1 (state collapsed to |1>)'}},1);
drag(cv,null,null);let lx=0,ly=0,dn=false;cv.addEventListener('pointerdown',ev=>{dn=true;[lx,ly]=pos(cv,ev)});cv.addEventListener('pointermove',ev=>{if(!dn)return;const[x,y]=pos(cv,ev);yaw+=(x-lx)*0.01;pit+=(y-ly)*0.01;pit=Math.max(-1.4,Math.min(1.4,pit));lx=x;ly=y});addEventListener('pointerup',()=>dn=false);
loop(()=>{const c=cv.ctx,W=cv.W,H=cv.H;c.clearRect(0,0,W,H);const R=Math.min(H*.4,W*.28),cx=W*.38,cy=H*.5;
const P=(x,y,z)=>{ // x right, y depth, z up
 const x1=x*Math.cos(yaw)-y*Math.sin(yaw),y1=x*Math.sin(yaw)+y*Math.cos(yaw),z1=z*Math.cos(pit)-y1*Math.sin(pit),y2=z*Math.sin(pit)+y1*Math.cos(pit);return[cx+x1*R,cy-z1*R,y2]};
c.strokeStyle=css('--line');c.lineWidth=1;c.beginPath();c.arc(cx,cy,R,0,7);c.stroke();
const ring=(f)=>{c.beginPath();for(let i=0;i<=64;i++){const t=i/64*6.2832,q=P(...f(t));i?c.lineTo(q[0],q[1]):c.moveTo(q[0],q[1])}c.stroke()};
ring(t=>[Math.cos(t),Math.sin(t),0]);ring(t=>[Math.cos(t),0,Math.sin(t)]);ring(t=>[0,Math.cos(t),Math.sin(t)]);
c.fillStyle=css('--mut');c.font='12px sans-serif';[['|0>',0,0,1.12],['|1>',0,0,-1.12],['+x',1.12,0,0],['+y',0,1.12,0]].forEach(l=>{const q=P(l[1],l[2],l[3]);c.fillText(l[0],q[0]-8,q[1]+4)});
// state vector: bloch coords
const th=2*Math.acos(Math.min(1,Math.hypot(a[0],a[1]))),ph=Math.atan2(b[1],b[0])-Math.atan2(a[1],a[0]);
const bx=Math.sin(th)*Math.cos(ph),by=Math.sin(th)*Math.sin(ph),bz=Math.cos(th);const q=P(bx,by,bz),o=P(0,0,0);
c.strokeStyle=css('--acc2');c.lineWidth=3;c.beginPath();c.moveTo(o[0],o[1]);c.lineTo(q[0],q[1]);c.stroke();c.fillStyle=css('--acc2');c.beginPath();c.arc(q[0],q[1],7,0,7);c.fill();
const p0=a[0]**2+a[1]**2,p1=1-p0,bx0=W*.68,bw=W*.28;c.fillStyle=css('--fg');c.font='13px sans-serif';c.fillText('P(0) = '+p0.toFixed(3),bx0,cy-40);
c.fillStyle=css('--acc');c.fillRect(bx0,cy-30,bw*p0,18);c.fillStyle=css('--fg');c.fillText('P(1) = '+p1.toFixed(3),bx0,cy+20);c.fillStyle=css('--ok');c.fillRect(bx0,cy+30,bw*p1,18);
const f=z=>(z[0]>=0?'+':'')+z[0].toFixed(2)+(z[1]>=0?'+':'')+z[1].toFixed(2)+'i';
$('r').innerHTML='state = ('+f(a)+')|0> + ('+f(b)+')|1> &nbsp; '+meas+'<br>H makes a superposition, X flips, Z flips the phase (invisible in P(0)/P(1) but real: try H then Z then H).'});
