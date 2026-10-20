import { spawn } from 'child_process';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'file:///' + path.resolve('Tao_Khung_Thoi_Su_Talk11.html').replace(/\\/g, '/');

async function test() {
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9290',
    'about:blank'
  ]);
  let res = null;
  for (let i = 0; i < 15; i++) {
    await new Promise(r => setTimeout(r, 300));
    try {
      res = await fetch('http://127.0.0.1:9290/json/new?' + encodeURIComponent(APP_URL), { method: 'PUT' });
      if (res.ok) break;
    } catch(e) {}
  }
  const target = await res.json();
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);

  let seq = 1;
  function send(method, params = {}) {
    return new Promise(resolve => {
      const id = seq++;
      const handler = (evt) => {
        const msg = JSON.parse(evt.data);
        if (msg.id === id) {
          ws.removeEventListener('message', handler);
          resolve(msg.result);
        }
      };
      ws.addEventListener('message', handler);
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  await send('Page.enable');
  await send('Runtime.enable');
  await new Promise(r => setTimeout(r, 1500));

  const result = await send('Runtime.evaluate', {
    expression: `(() => {
      const c = document.createElement('canvas');
      c.width = 640; c.height = 360;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#FFA07A'; ctx.fillRect(200, 50, 240, 260);
      const stream = c.captureStream(30);
      const vid = document.createElement('video');
      vid.srcObject = stream;
      vid.muted = true;
      studentVideoElem = vid;
      enableStudentVideo = true;

      aiMaskCanvas.width = 640; aiMaskCanvas.height = 360;
      const mCtx = aiMaskCanvas.getContext('2d');
      mCtx.fillStyle = '#FFFFFF'; mCtx.fillRect(200, 50, 240, 260);
      hasValidAiMask = true;

      const times = [];
      for (let i = 0; i < 10; i++) {
        forceChromaReprocess = true;
        const t0 = performance.now();
        processStudentChromaKey();
        times.push(performance.now() - t0);
      }
      return {
        times,
        avg: times.reduce((a, b) => a + b, 0) / times.length
      };
    })()`,
    returnByValue: true
  });
  console.log('Execution timing of processStudentChromaKey:', result.result.value);
  ws.close();
  edgeProc.kill();
}
test();
