//TITLE: Pure pursuit path tracking (car-like robot)
//NOTE: A car with a bicycle model follows the dashed path by steering toward a look-ahead point on it. A short look-ahead reacts sharply but oscillates; a long one is smooth but cuts corners. Drag the path's blue handles to reshape it.
const cv=setup($('c'),0.55),ctl=$('k');let La=1.2,v=1.5,Lw=0.6,car,P=[[.1,.7],[.35,.2],[.65,.85],[.9,.3]],tr=[];const sc=()=>cv.W/10;
slider(ctl,'look-ahead distance',0.3,4,0.05,La,a=>La=a);slider(ctl,'speed',0.5,4,0.1,v,a=>v=a);btn(ctl,'Restart car',reset,1);
function reset(){car={x:P[0][0]*10,y:P[0][1]*10*cv.H/cv.W,th:0};tr=[]}cv.onfit=reset;reset();
let sel=-1;drag(cv,(x,y)=>{sel=-1;P.forEach((p,i)=>{if(Math.hypot(p[0]*cv.W-x,p[1]*cv.H-y)<16)sel=i})},(x,y)=>{if(sel>=0){P[sel]=[x/cv.W,y/cv.H];}});
function spline(){const out=[];const pp=[P[0],...P,P[3]];for(let i=1;i<pp.length-2;i++)for(let t=0;t<1;t+=.02){const a=pp[i-1],b=pp[i],c=pp[i+1],d=pp[i+2];out.push([0,1].map(k=>.5*((2*b[k])+(-a[k]+c[k])*t+(2*a[k]-5*b[k]+4*c[k]-d[k])*t*t+(-a[k]+3*b[k]-3*c[k]+d[k])*t*t*t)))}return out.map(p=>[p[0]*10,p[1]*10*cv.H/cv.W])}
loop(dt=>{const path=spline(),s=sc();let bi=0,bd=1e9;path.forEach((p,i)=>{const d=Math.hypot(p[0]-car.x,p[1]-car.y);if(d<bd){bd=d;bi=i}});let ti=bi;while(ti<path.length-1&&Math.hypot(path[ti][0]-car.x,path[ti][1]-car.y)<La)ti++;const tg=path[ti];
const ang=Math.atan2(tg[1]-car.y,tg[0]-car.x)-car.th,al=Math.atan2(Math.sin(ang),Math.cos(ang));const delta=Math.max(-.6,Math.min(.6,Math.atan2(2*Lw*Math.sin(al),La)));
if(bi<path.length-2){car.x+=v*Math.cos(car.th)*dt;car.y+=v*Math.sin(car.th)*dt;car.th+=v/Lw*Math.tan(delta)*dt;tr.push([car.x,car.y]);if(tr.length>800)tr.shift()}else reset();
const c=cv.ctx;c.clearRect(0,0,cv.W,cv.H);c.setLineDash([6,5]);c.strokeStyle=css('--mut');c.lineWidth=2;c.beginPath();path.forEach((p,i)=>i?c.lineTo(p[0]*s,p[1]*s):c.moveTo(p[0]*s,p[1]*s));c.stroke();c.setLineDash([]);
c.strokeStyle=css('--ok');c.beginPath();tr.forEach((p,i)=>i?c.lineTo(p[0]*s,p[1]*s):c.moveTo(p[0]*s,p[1]*s));c.stroke();
c.fillStyle=css('--acc');P.forEach(p=>{c.beginPath();c.arc(p[0]*cv.W,p[1]*cv.H,7,0,7);c.fill()});
c.strokeStyle=css('--acc2');c.beginPath();c.moveTo(car.x*s,car.y*s);c.lineTo(tg[0]*s,tg[1]*s);c.stroke();c.fillStyle=css('--acc2');c.beginPath();c.arc(tg[0]*s,tg[1]*s,5,0,7);c.fill();
c.save();c.translate(car.x*s,car.y*s);c.rotate(car.th);c.fillStyle=css('--fg');c.fillRect(-14,-9,28,18);c.fillStyle='#fff';c.fillRect(6,-6,8,12);c.restore();
$('r').innerHTML='steering angle <b>'+(delta*57.3).toFixed(1)+'°</b> &nbsp; cross-track error <b>'+bd.toFixed(2)+'</b> &nbsp; steering = atan(2·L·sin(α)/look-ahead)'});
