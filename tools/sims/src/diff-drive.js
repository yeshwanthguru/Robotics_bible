//TITLE: Differential-drive robot and odometry drift
//NOTE: Two wheels, two speeds. Equal speeds drive straight; unequal speeds turn. The green path is the truth; the dashed path is dead-reckoning odometry using slightly wrong wheel-radius and noisy encoders. Notice how error accumulates, which is why robots need SLAM or other corrections.
const cv=setup($('c'),0.62),ctl=$('k');let vl=0.8,vr=1.1,noise=0.02,bias=1.03,r={x:0,y:0,th:0},o={x:0,y:0,th:0},tr=[],od=[],L=0.5;
slider(ctl,'left wheel',-1.5,1.5,0.05,vl,a=>vl=a);slider(ctl,'right wheel',-1.5,1.5,0.05,vr,a=>vr=a);slider(ctl,'encoder noise',0,0.15,0.005,noise,a=>noise=a,v=>(+v).toFixed(3));slider(ctl,'wheel-size error',0.9,1.1,0.005,bias,a=>bias=a,v=>(+v).toFixed(3));btn(ctl,'Reset',reset,1);
function reset(){r={x:0,y:0,th:0};o={x:0,y:0,th:0};tr=[];od=[]}
loop(dt=>{for(let i=0;i<3;i++){const h=dt/3,v=(vl+vr)/2,w=(vr-vl)/L;r.x+=v*Math.cos(r.th)*h;r.y+=v*Math.sin(r.th)*h;r.th+=w*h;
const ml=vl*bias+gauss()*noise,mr=vr*bias+gauss()*noise,mv=(ml+mr)/2,mw=(mr-ml)/L;o.x+=mv*Math.cos(o.th)*h;o.y+=mv*Math.sin(o.th)*h;o.th+=mw*h}
tr.push([r.x,r.y]);od.push([o.x,o.y]);if(tr.length>1500){tr.shift();od.shift()}
const c=cv.ctx,W=cv.W,H=cv.H;c.clearRect(0,0,W,H);const all=tr.concat(od),cx=r.x,cy=r.y,sc=Math.min(W,H)/9;const P=(x,y)=>[W/2+(x-cx)*sc,H/2-(y-cy)*sc];
c.strokeStyle=css('--line');c.lineWidth=.5;for(let g=-10;g<=10;g++){const a=P(Math.round(cx)+g,0),b=P(0,Math.round(cy)+g);c.beginPath();c.moveTo(a[0],0);c.lineTo(a[0],H);c.moveTo(0,b[1]);c.lineTo(W,b[1]);c.stroke()}
c.lineWidth=2.5;c.strokeStyle=css('--ok');c.beginPath();tr.forEach((q,i)=>{const p=P(...q);i?c.lineTo(...p):c.moveTo(...p)});c.stroke();
c.setLineDash([6,4]);c.strokeStyle=css('--acc2');c.beginPath();od.forEach((q,i)=>{const p=P(...q);i?c.lineTo(...p):c.moveTo(...p)});c.stroke();c.setLineDash([]);
const p=P(r.x,r.y);c.save();c.translate(...p);c.rotate(-r.th);c.fillStyle=css('--acc');c.fillRect(-14,-10,28,20);c.fillStyle='#fff';c.fillRect(6,-4,8,8);c.restore();
$('r').innerHTML='v = (vL+vR)/2 = <b>'+((vl+vr)/2).toFixed(2)+'</b> m/s &nbsp; ω = (vR−vL)/L = <b>'+((vr-vl)/L).toFixed(2)+'</b> rad/s &nbsp; odometry error <b>'+Math.hypot(r.x-o.x,r.y-o.y).toFixed(2)+'</b> m'});
