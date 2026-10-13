//TITLE: Two-link arm: forward and inverse kinematics
//NOTE: Drag the red target. The solver finds joint angles that put the hand on it. Flip elbow-up/down; drag beyond reach, or very near the base, to see singularities.
const cv=setup($('c'),0.7);let L1=1.0,L2=0.8,up=true,T=[1.0,0.6],ctl=$('k');
slider(ctl,'link 1',0.4,1.5,0.05,L1,a=>L1=a);slider(ctl,'link 2',0.4,1.5,0.05,L2,a=>L2=a);btn(ctl,'Flip elbow',()=>up=!up);
const S=()=>cv.H/4.2, ox=()=>cv.W/2, oy=()=>cv.H*0.5;
function mv(x,y){T=[(x-ox())/S(),-(y-oy())/S()]}drag(cv,mv,mv);
loop(()=>{const c=cv.ctx,s=S();c.clearRect(0,0,cv.W,cv.H);
c.strokeStyle=css('--line');c.setLineDash([4,4]);[L1+L2,Math.abs(L1-L2)].forEach(r=>{c.beginPath();c.arc(ox(),oy(),r*s,0,7);c.stroke()});c.setLineDash([]);
let d=Math.hypot(T[0],T[1]);const out=d>L1+L2||d<Math.abs(L1-L2);let tx=T[0],ty=T[1];
if(d>L1+L2){tx=T[0]/d*(L1+L2);ty=T[1]/d*(L1+L2)}else if(d<Math.abs(L1-L2)&&d>1e-6){const k=Math.abs(L1-L2)/d;tx*=k;ty*=k}
d=Math.hypot(tx,ty);let cq2=(d*d-L1*L1-L2*L2)/(2*L1*L2);cq2=Math.max(-1,Math.min(1,cq2));const q2=Math.acos(cq2)*(up?-1:1);
const q1=Math.atan2(ty,tx)-Math.atan2(L2*Math.sin(q2),L1+L2*Math.cos(q2));
const ex=L1*Math.cos(q1),ey=L1*Math.sin(q1),hx=ex+L2*Math.cos(q1+q2),hy=ey+L2*Math.sin(q1+q2);
const P=(x,y)=>[ox()+x*s,oy()-y*s];c.lineCap='round';c.lineWidth=9;c.strokeStyle=css('--acc');c.beginPath();c.moveTo(...P(0,0));c.lineTo(...P(ex,ey));c.stroke();
c.strokeStyle=css('--ok');c.beginPath();c.moveTo(...P(ex,ey));c.lineTo(...P(hx,hy));c.stroke();c.lineWidth=1;
c.fillStyle=css('--fg');[[0,0],[ex,ey],[hx,hy]].forEach(q=>{c.beginPath();c.arc(...P(...q),6,0,7);c.fill()});
c.fillStyle=css('--acc2');c.beginPath();c.arc(...P(T[0],T[1]),8,0,7);c.fill();
const J=L1*L2*Math.sin(q2);
$('r').innerHTML='q1 <b>'+(q1*57.296).toFixed(1)+'°</b> &nbsp; q2 <b>'+(q2*57.296).toFixed(1)+'°</b> &nbsp; '+(out?'<b style="color:var(--warn)">target unreachable: arm stretches toward it</b>':Math.abs(Math.sin(q2))<0.05?'<b style="color:var(--warn)">near singularity</b>':'reachable')+'<br>det(Jacobian) = L1·L2·sin(q2) = <b>'+J.toFixed(3)+'</b> (zero = singular: one direction of hand motion is lost)'});
