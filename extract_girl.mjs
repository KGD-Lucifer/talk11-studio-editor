import { spawn } from 'child_process';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = __dirname;
const PORT = 8116;

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  let reqUrl = decodeURI(req.url.split('?')[0]);
  const safePath = path.normalize(path.resolve(ROOT, '.' + reqUrl));
  fs.stat(safePath, (err, stats) => {
    if (err || !stats.isFile()) { res.writeHead(404); res.end('404'); return; }
    res.writeHead(200);
    fs.createReadStream(safePath).pipe(res);
  });
});

server.listen(PORT, '127.0.0.1', async () => {
  const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9255',
    '--window-size=1280,720',
    'about:blank'
  ]);
  await new Promise(r => setTimeout(r, 1500));

  try {
    const res = await fetch(`http://127.0.0.1:9255/json/new?${encodeURIComponent('http://127.0.0.1:' + PORT + '/Tao_Khung_Thoi_Su_Talk11.html')}`, { method: 'PUT' });
    const target = await res.json();
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    let idSeq = 1;
    const pending = new Map();

    function send(method, params = {}) {
      return new Promise((resolve, reject) => {
        const id = idSeq++;
        pending.set(id, { resolve, reject });
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    await new Promise(r => { ws.onopen = r; });
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        const p = pending.get(msg.id);
        pending.delete(msg.id);
        if (msg.error) p.reject(msg.error);
        else p.resolve(msg.result);
      }
    };

    await send('Runtime.enable');
    await send('Page.enable');
    await new Promise(r => setTimeout(r, 2000));

    const frame = await send('Runtime.evaluate', {
      expression: `(async () => {
        const v = document.createElement('video');
        v.src = 'student_input_sample.mp4';
        v.muted = true;
        await new Promise(r => { v.onloadedmetadata = r; });
        v.currentTime = 3.0;
        await new Promise(r => setTimeout(r, 500));
        const c = document.createElement('canvas');
        c.width = v.videoWidth;
        c.height = v.videoHeight;
        const ctx = c.getContext('2d');
        ctx.drawImage(v, 0, 0);
        return {
          w: v.videoWidth,
          h: v.videoHeight,
          dur: v.duration,
          dataUrl: c.toDataURL('image/jpeg', 0.85)
        };
      })()`,
      awaitPromise: true,
      returnByValue: true
    });

    console.log('Video Info:', frame.result.value.w, frame.result.value.h, frame.result.value.dur);
    const b64 = frame.result.value.dataUrl.replace(/^data:image\/jpeg;base64,/, '');
    fs.writeFileSync('extracted_student_girl.jpg', Buffer.from(b64, 'base64'));
    console.log('Saved extracted_student_girl.jpg, bytes:', fs.statSync('extracted_student_girl.jpg').size);

  } catch(e) {
    console.error(e);
  } finally {
    edgeProc.kill();
    server.close();
    process.exit(0);
  }
});
