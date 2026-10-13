//TITLE: Softmax and attention in 2-D
//NOTE: Drag the query (red arrow tip). Each key (blue) gets a score = dot product with the query; softmax turns scores into attention weights (bars). Lower the temperature and the weights become winner-take-all; raise it and they flatten. The output is the weighted mix of the values.
const cv=setup($('c'),0.55),ctl=$('k');let T=1,Qv=[1.2,0.5];const K=[[1.5,0.3],[0.2,1.4],[-1.2,0.6],[-0.4,-1.3],[1.0,-1.0]],names=['the','cat','sat','on','mat'];
slider(ctl,'temperature',0.1,4,0.05,T,a=>T=a);
const S=()=>Math.min(cv.W*.22,cv.H*.3),ox=()=>cv.W*.25,oy=()=>cv.H*.5;function mv(x,y){Qv=[(x-ox())/S(),-(y-oy())/S()]}drag(cv,(x,y)=>{if(x<cv.W*.5)mv(x,y)},(x,y)=>{if(x<cv.W*.5||true)mv(x,y)});
loop(()=>{const c=cv.ctx,W=cv.W,H=cv.H,s=S();c.clearRect(0,0,W,H);const sc=K.map(k=>(k[0]*Qv[0]+k[1]*Qv[1])/Math.sqrt(2)/T),mx=Math.max(...sc),ex=sc.map(v=>Math.exp(v-mx)),sm=ex.reduce((a,b)=>a+b),w=ex.map(v=>v/sm);
const P=(x,y)=>[ox()+x*s,oy()-y*s];c.strokeStyle=css('--line');c.beginPath();c.moveTo(0,oy());c.lineTo(W*.5,oy());c.moveTo(ox(),0);c.lineTo(ox(),H);c.stroke();
K.forEach((k,i)=>{const p=P(...k);c.strokeStyle=css('--acc');c.globalAlpha=.25+.75*w[i];c.lineWidth=2+6*w[i];c.beginPath();c.moveTo(...P(0,0));c.lineTo(...p);c.stroke();c.globalAlpha=1;c.fillStyle=css('--fg');c.fillText(names[i],p[0]+6,p[1]-6)});
const q=P(...Qv);c.strokeStyle=css('--acc2');c.lineWidth=3;c.beginPath();c.moveTo(...P(0,0));c.lineTo(...q);c.stroke();c.fillStyle=css('--acc2');c.beginPath();c.arc(...q,8,0,7);c.fill();c.lineWidth=1;
const bx=W*.55,bw=W*.4;c.font='13px sans-serif';names.forEach((n,i)=>{const y=H*.12+i*H*.16;c.fillStyle=css('--fg');c.fillText(n+'  score '+(sc[i]*T).toFixed(2),bx,y);c.fillStyle=css('--acc');c.fillRect(bx,y+5,bw*w[i],14);c.fillStyle=css('--fg');c.fillText((w[i]*100).toFixed(0)+'%',bx+bw*w[i]+6,y+17)});
$('r').innerHTML='weights sum to <b>'+w.reduce((a,b)=>a+b).toFixed(2)+'</b> &nbsp; This is the core of every Transformer: score = q·k / √d, then softmax, then weighted sum of values.'});
