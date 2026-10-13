//TITLE: Underfitting vs overfitting (bias and variance)
//NOTE: Dots are noisy samples of a hidden curve (green). The blue line is a polynomial fitted to the training points (dark dots); hollow dots are unseen test points. Low degree underfits (high bias); very high degree wiggles through the noise (high variance): training error falls but test error rises.
const cv=setup($('c'),0.55),ctl=$('k');let deg=3,n=15,noise=0.25,tr=[],te=[];const tru=x=>Math.sin(2*Math.PI*x);
slider(ctl,'polynomial degree',0,12,1,deg,a=>deg=a);slider(ctl,'training points',6,40,1,n,a=>{n=a;gen()});slider(ctl,'noise',0,0.6,0.01,noise,a=>{noise=a;gen()});btn(ctl,'New data',gen,1);
function gen(){tr=[];te=[];for(let i=0;i<n;i++){const x=Math.random();tr.push([x,tru(x)+gauss()*noise])}for(let i=0;i<60;i++){const x=Math.random();te.push([x,tru(x)+gauss()*noise])}}gen();
function fit(d){const m=d+1,A=Array.from({length:m},()=>Array(m+1).fill(0));tr.forEach(p=>{const pw=[];for(let i=0;i<m;i++)pw.push(p[0]**i);for(let i=0;i<m;i++){for(let j=0;j<m;j++)A[i][j]+=pw[i]*pw[j];A[i][m]+=pw[i]*p[1]}});
for(let i=0;i<m;i++)A[i][i]+=1e-9; for(let i=0;i<m;i++){let p=i;for(let r=i+1;r<m;r++)if(Math.abs(A[r][i])>Math.abs(A[p][i]))p=r;[A[i],A[p]]=[A[p],A[i]];for(let r=0;r<m;r++){if(r===i)continue;const f=A[r][i]/A[i][i];for(let c=i;c<=m;c++)A[r][c]-=f*A[i][c]}}
return A.map((r,i)=>r[m]/r[i])}
const ev=(w,x)=>w.reduce((a,c,i)=>a+c*x**i,0),mse=(w,D)=>D.reduce((a,p)=>a+(ev(w,p[0])-p[1])**2,0)/D.length;
loop(()=>{const c=cv.ctx,W=cv.W,H=cv.H;c.clearRect(0,0,W,H);const X=x=>x*W,Y=y=>H*(.5-y*.32);const w=fit(deg);
c.strokeStyle=css('--ok');c.lineWidth=2;c.beginPath();for(let i=0;i<=100;i++){const x=i/100;i?c.lineTo(X(x),Y(tru(x))):c.moveTo(X(x),Y(tru(x)))}c.stroke();
c.strokeStyle=css('--acc');c.lineWidth=2.5;c.beginPath();for(let i=0;i<=200;i++){const x=i/200,y=Math.max(-2.4,Math.min(2.4,ev(w,x)));i?c.lineTo(X(x),Y(y)):c.moveTo(X(x),Y(y))}c.stroke();
c.fillStyle=css('--fg');tr.forEach(p=>{c.beginPath();c.arc(X(p[0]),Y(p[1]),4,0,7);c.fill()});c.strokeStyle=css('--mut');c.lineWidth=1;te.forEach(p=>{c.beginPath();c.arc(X(p[0]),Y(p[1]),3,0,7);c.stroke()});
const a=mse(w,tr),b=mse(w,te);$('r').innerHTML='training error <b>'+a.toFixed(3)+'</b> &nbsp; test error <b>'+b.toFixed(3)+'</b> &nbsp; '+(b>a*3&&deg>5?'<b style="color:var(--warn)">overfitting: test error much larger than training</b>':deg<2?'<b style="color:var(--warn)">underfitting: model too simple</b>':'reasonable fit')});
