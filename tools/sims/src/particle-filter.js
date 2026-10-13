//TITLE: Monte Carlo localization (particle filter)
//NOTE: The robot (green) drives around and measures distance to the three landmarks (squares). Each blue dot is a guess of where it is. Dots that match the measurements survive and multiply. Click to teleport the robot (the "kidnapped robot" problem).
const cv=setup($('c'),0.62);const LM=[[0.15,0.2],[0.85,0.25],[0.5,0.85]];let N=300,ns=0.04,rob={x:0.3,y:0.5,a:0},ps=[],ctl=$('k');
slider(ctl,'particles',20,1500,10,N,a=>{N=a;init()});slider(ctl,'sensor noise',0.01,0.2,0.005,ns,a=>ns=a,v=>(+v).toFixed(3));btn(ctl,'Scatter again',init,1);
function init(){ps=[];for(let i=0;i<N;i++)ps.push({x:Math.random(),y:Math.random(),a:Math.random()*6.28,w:1/N})}init();
cv.addEventListener('pointerdown',e=>{const q=pos(cv,e);rob.x=q[0]/cv.W;rob.y=q[1]/cv.H});
function step(){const v=0.012,w=0.05*Math.sin(performance.now()/1700)+0.03;rob.a+=w;rob.x+=v*Math.cos(rob.a);rob.y+=v*Math.sin(rob.a);
if(rob.x<0.05||rob.x>0.95)rob.a=Math.PI-rob.a;if(rob.y<0.05||rob.y>0.95)rob.a=-rob.a;rob.x=Math.max(0.03,Math.min(0.97,rob.x));rob.y=Math.max(0.03,Math.min(0.97,rob.y));
const z=LM.map(l=>Math.hypot(l[0]-rob.x,l[1]-rob.y)+gauss()*ns);
let s=0;ps.forEach(p=>{p.a+=w+gauss()*0.03;const vv=v+gauss()*0.003;p.x+=vv*Math.cos(p.a);p.y+=vv*Math.sin(p.a);p.x=Math.max(0,Math.min(1,p.x));p.y=Math.max(0,Math.min(1,p.y));
let l=0;LM.forEach((m,i)=>{const e=Math.hypot(m[0]-p.x,m[1]-p.y)-z[i];l+=e*e/(2*ns*ns)});p.w=Math.exp(-l)+1e-12;s+=p.w});
ps.forEach(p=>p.w/=s);
const n=ps.length,out=[];let r=Math.random()/n,cum=ps[0].w,i=0;for(let m=0;m<n;m++){const u=r+m/n;while(u>cum&&i<n-1){i++;cum+=ps[i].w}out.push({...ps[i],w:1/n})}
ps=out;ps.forEach(p=>{p.x+=gauss()*0.004;p.y+=gauss()*0.004})}
let acc=0;loop(dt=>{acc+=dt;while(acc>0.05){step();acc-=0.05}const c=cv.ctx,W=cv.W,H=cv.H;c.clearRect(0,0,W,H);
c.fillStyle=css('--acc2');LM.forEach(l=>c.fillRect(l[0]*W-7,l[1]*H-7,14,14));
c.fillStyle=css('--acc');c.globalAlpha=0.55;ps.forEach(p=>{c.beginPath();c.arc(p.x*W,p.y*H,2.4,0,7);c.fill()});c.globalAlpha=1;
c.fillStyle=css('--ok');c.beginPath();c.arc(rob.x*W,rob.y*H,8,0,7);c.fill();c.strokeStyle=css('--fg');c.beginPath();c.moveTo(rob.x*W,rob.y*H);c.lineTo(rob.x*W+16*Math.cos(rob.a),rob.y*H+16*Math.sin(rob.a));c.stroke();
const mx=ps.reduce((a,p)=>a+p.x,0)/ps.length,my=ps.reduce((a,p)=>a+p.y,0)/ps.length;
$('r').innerHTML='estimate error <b>'+(Math.hypot(mx-rob.x,my-rob.y)*100).toFixed(1)+'</b> % of map width &nbsp; spread shrinks as the filter converges'});
