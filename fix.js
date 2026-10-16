const fs = require('fs');
const content = `import React, { useEffect, useRef } from 'react';
import { staticFile } from 'remotion';

export const Studio3DCanvasTest: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const bgImg = new Image();
    bgImg.src = staticFile('03_ASSETS/Studio_Backgrounds/studio_cyber_neon.jpg');
    const sampleImg = new Image();
    sampleImg.src = staticFile('03_ASSETS/Studio_Backgrounds/topic_vietnam_history.jpg');

    function renderTri(ctx, img, x0, y0, x1, y1, x2, y2, u0, v0, u1, v1, u2, v2, srcX, srcY, srcW, srcH) {
      const delta = u0*(v1-v2)-v0*(u1-u2)+(u1*v2-u2*v1);
      if (Math.abs(delta)<0.00001) return;
      const a=(x0*(v1-v2)-v0*(x1-x2)+(x1*v2-x2*v1))/delta;
      const b=(y0*(v1-v2)-v0*(y1-y2)+(y1*v2-y2*v1))/delta;
      const c=(u0*(x1-x2)-x0*(u1-u2)+(u1*x2-u2*x1))/delta;
      const d=(u0*(y1-y2)-y0*(u1-u2)+(u1*y2-u2*y1))/delta;
      const e=(u0*(v1*x2-v2*x1)-v0*(u1*x2-u2*x1)+x0*(u1*v2-u2*v1))/delta;
      const f=(u0*(v1*y2-v2*y1)-v0*(u1*y2-u2*y1)+y0*(u1*v2-u2*v1))/delta;
      ctx.save(); ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1,y1); ctx.lineTo(x2,y2); ctx.closePath(); ctx.clip();
      ctx.transform(a,b,c,d,e,f); ctx.drawImage(img,srcX,srcY,srcW,srcH,0,0,srcW,srcH); ctx.restore();
    }

    function drawQuad(ctx, img, p0, p1, p2, p3, label) {
      const w = img.naturalWidth||img.width||400; const h = img.naturalHeight||img.height||300;
      const targetRatio = 16/9; const mediaRatio = w/h;
      let srcX=0,srcY=0,srcW=w,srcH=h;
      if (mediaRatio>targetRatio) { srcH=h; srcW=h*targetRatio; srcX=(w-srcW)/2; srcY=0; }
      else { srcW=w; srcH=w/targetRatio; srcX=0; srcY=(h-srcH)/2; }
      
      ctx.globalAlpha = 0.5;
      renderTri(ctx,img,p0.x,p0.y,p1.x,p1.y,p2.x,p2.y,0,0,srcW,0,srcW,srcH,srcX,srcY,srcW,srcH);
      renderTri(ctx,img,p0.x,p0.y,p2.x,p2.y,p3.x,p3.y,0,0,srcW,srcH,0,srcH,srcX,srcY,srcW,srcH);
      ctx.globalAlpha = 1.0;

      ctx.save(); ctx.beginPath();
      ctx.moveTo(p0.x,p0.y); ctx.lineTo(p1.x,p1.y); ctx.lineTo(p2.x,p2.y); ctx.lineTo(p3.x,p3.y);
      ctx.closePath(); ctx.strokeStyle='#00FF00'; ctx.lineWidth=2; ctx.stroke();
      ctx.fillStyle='white'; ctx.font='bold 24px Arial'; ctx.fillText(label, p0.x+20, p0.y+50);
      ctx.restore();
    }

    bgImg.onload = () => {
      ctx.drawImage(bgImg, 0, 0, 1920, 1080);
      const rightWallScreens = [
        { label: '1', p0:{x:1230,y:20}, p1:{x:1370,y:-10}, p2:{x:1370,y:160}, p3:{x:1230,y:190} },
        { label: '2', p0:{x:1230,y:220}, p1:{x:1370,y:195}, p2:{x:1370,y:395}, p3:{x:1230,y:430} },
        { label: '3', p0:{x:1230,y:465}, p1:{x:1370,y:435}, p2:{x:1370,y:640}, p3:{x:1230,y:675} },
        { label: '4', p0:{x:1400,y:-25}, p1:{x:1580,y:-65}, p2:{x:1585,y:130}, p3:{x:1400,y:160} },
        { label: '5', p0:{x:1400,y:185}, p1:{x:1785,y:110}, p2:{x:1795,y:410}, p3:{x:1400,y:475} },
        { label: '6', p0:{x:1400,y:510}, p1:{x:1795,y:445}, p2:{x:1805,y:715}, p3:{x:1400,y:785} },
      ];
      sampleImg.onload = () => {
        rightWallScreens.forEach(sc => drawQuad(ctx, sampleImg, sc.p0, sc.p1, sc.p2, sc.p3, sc.label));
      };
    };
  }, []);

  return <canvas ref={canvasRef} width={1920} height={1080} style={{ width: '100%', height: '100%' }} />;
};
`;
fs.writeFileSync('remotion-prompt-to-video/src/components/Studio3DCanvasTest.tsx', content, 'utf8');
