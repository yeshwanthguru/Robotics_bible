//TITLE: Kalman filter tracking a moving object
//NOTE: A hidden object moves; the sensor gives noisy position readings (grey dots). The Kalman filter (blue) blends its motion model with the readings. Raise measurement noise R and it trusts the model more; raise process noise Q and it trusts the sensor more.
const cv=setup($('c'),0.5);let Q=0.05,R=1.2,ctl=$('k');
slider(ctl,'process noise Q',0.001,2,0.001,Q,a=>Q=a,v=>(+v).toFixed(3));slider(ctl,'sensor noise R (true σ=1.2 → R≈1.4)',0.05,10,0.05,R,a=>R=a);btn(ctl,'Restart',init);
let t,tx,tv,x,vv,P,H;
function init(){t=0;tx=0;tv=1.5;x=0;vv=0;P=[[10,0],[0,10]];H=[]}init();
function step(dt){tv+=gauss()*0.8*dt;tx+=tv*dt;t+=dt;const z=tx+gauss()*1.2;
// predict with constant-velocity model
x+=vv*dt;const a=P[0][0]+dt*(P[1][0]+P[0][1])+dt*dt*P[1][1]+Q*dt,b=P[0][1]+dt*P[1][1],c=P[1][0]+dt*P[1][1],d=P[1][1]+Q*dt;
const S=a+R,K0=a/S,K1=c/S,y=z-x;x+=K0*y;vv+=K1*y;P=[[(1-K0)*a,(1-K0)*b],[c-K1*a,d-K1*b]];
H.push({t,tx,z,x});if(H.length>260)H.shift()}
let acc=0;loop(dt=>{acc+=dt;while(acc>0.04){step(0.04);acc-=0.04}draw()});
function draw(){const c=cv.ctx,W=cv.W,Hh=cv.H;c.clearRect(0,0,W,Hh);if(H.length<2)return;
const lo=Math.min(...H.map(h=>Math.min(h.tx,h.z,h.x)))-1,hi=Math.max(...H.map(h=>Math.max(h.tx,h.z,h.x)))+1;
const X=i=>i/259*W,Y=v=>Hh*(1-(v-lo)/(hi-lo));
c.fillStyle=css('--mut');H.forEach((h,i)=>{c.beginPath();c.arc(X(i),Y(h.z),2.2,0,7);c.fill()});
c.lineWidth=2;c.strokeStyle=css('--ok');c.beginPath();H.forEach((h,i)=>i?c.lineTo(X(i),Y(h.tx)):c.moveTo(X(i),Y(h.tx)));c.stroke();
c.strokeStyle=css('--acc');c.beginPath();H.forEach((h,i)=>i?c.lineTo(X(i),Y(h.x)):c.moveTo(X(i),Y(h.x)));c.stroke();c.lineWidth=1;
c.fillStyle=css('--fg');c.fillText('grey: noisy sensor   green: truth   blue: Kalman estimate',8,14);
const l=H[H.length-1];$('r').innerHTML='estimate error <b>'+Math.abs(l.x-l.tx).toFixed(2)+'</b> &nbsp; raw sensor error <b>'+Math.abs(l.z-l.tx).toFixed(2)+'</b> &nbsp; velocity estimate <b>'+vv.toFixed(2)+'</b> (true '+tv.toFixed(2)+')'}
