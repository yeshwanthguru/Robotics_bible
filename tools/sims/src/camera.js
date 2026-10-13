//TITLE: Pinhole camera projection
//NOTE: A 3-D cube is seen through a pinhole camera. Left: the 3-D scene from above. Right: the image the camera sees. Change the focal length (zoom) and move the camera; the image point is u = f·X/Z + cx, v = f·Y/Z + cy.
const cv=setup($('c'),0.5),ctl=$('k');let f=500,tx=0,tz=-5,yaw=0.3;
slider(ctl,'focal length f (px)',200,1200,10,f,a=>f=a);slider(ctl,'camera x',-3,3,0.1,tx,a=>tx=a);slider(ctl,'camera distance',2,12,0.1,-tz,a=>tz=-a);slider(ctl,'camera yaw',-0.8,0.8,0.02,yaw,a=>yaw=a);
const V=[];for(const x of[-1,1])for(const y of[-1,1])for(const z of[-1,1])V.push([x,y,z]);const E=[];V.forEach((a,i)=>V.forEach((b,j)=>{if(j>i&&a.filter((v,k)=>v!==b[k]).length===1)E.push([i,j])}));
loop(()=>{const c=cv.ctx,W=cv.W,H=cv.H;c.clearRect(0,0,W,H);const hw=W/2;
// top view left
const s=hw/16,cx=hw/2,cy=H*.5;const T=(x,z)=>[cx+x*s,cy-z*s];c.strokeStyle=css('--line');c.strokeRect(0,0,hw,H);
c.strokeStyle=css('--acc');c.lineWidth=2;c.beginPath();[[-1,-1],[1,-1],[1,1],[-1,1],[-1,-1]].forEach((q,i)=>{const p=T(q[0],q[1]);i?c.lineTo(...p):c.moveTo(...p)});c.stroke();
const cp=T(tx,tz);c.fillStyle=css('--acc2');c.beginPath();c.arc(...cp,6,0,7);c.fill();const fov=Math.atan((320)/f);
c.strokeStyle=css('--acc2');c.lineWidth=1;[-1,1].forEach(sg=>{c.beginPath();c.moveTo(...cp);const a=yaw+sg*fov;c.lineTo(cp[0]+Math.sin(a)*s*14,cp[1]-Math.cos(a)*s*14);c.stroke()});
c.fillStyle=css('--mut');c.fillText('top view (camera = red, field of view lines)',6,14);
// image right
const iw=hw-12,ih=H-12,ox=hw+6,oy=6,sc=Math.min(iw/640,ih/480);c.save();c.beginPath();c.rect(ox,oy,640*sc,480*sc);c.clip();c.fillStyle=css('--bg');c.fillRect(ox,oy,640*sc,480*sc);
const proj=v=>{let X=v[0]-tx,Y=-v[1],Z=v[2]-tz;const cx_=Math.cos(yaw),sy=Math.sin(yaw);const x2=X*cx_-Z*sy,z2=X*sy+Z*cx_;return z2>0.1?[ox+(f*x2/z2+320)*sc,oy+(f*Y/z2+240)*sc]:null};
c.strokeStyle=css('--acc');c.lineWidth=2;E.forEach(e=>{const a=proj(V[e[0]]),b=proj(V[e[1]]);if(a&&b){c.beginPath();c.moveTo(...a);c.lineTo(...b);c.stroke()}});c.restore();
c.strokeStyle=css('--fg');c.lineWidth=1;c.strokeRect(ox,oy,640*sc,480*sc);c.fillStyle=css('--mut');c.fillText('camera image (640×480)',ox+4,oy+14);
$('r').innerHTML='horizontal field of view <b>'+(2*Math.atan(320/f)*57.3).toFixed(0)+'°</b> &nbsp; Larger f = zoomed in (narrower view); nearer camera = bigger cube, stronger perspective.'});
