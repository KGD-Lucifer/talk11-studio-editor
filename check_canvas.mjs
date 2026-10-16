import { spawn } from 'child_process';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = 8094;
const ROOT = __dirname;

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  res.setHeader('Cross-Origin-Embedder-Policy', 'credentialless');

  let reqUrl = decodeURI(req.url.split('?')[0]);
  if (reqUrl === '/' || reqUrl === '') reqUrl = '/Tao_Khung_Thoi_Su_Talk11.html';

  const safePath = path.normalize(path.resolve(ROOT, '.' + reqUrl));
  fs.stat(safePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404);
      res.end('404');
      return;
    }
    res.writeHead(200);
    fs.createReadStream(safePath).pipe(res);
  });
});

server.listen(PORT, '127.0.0.1', async () => {
  const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9227',
    '--window-size=1680,980',
    'about:blank'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const res = await fetch(`http://127.0.0.1:9227/json/new?http://127.0.0.1:${PORT}/Tao_Khung_Thoi_Su_Talk11.html`, { method: 'PUT' });
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

    console.log('[QA] Waiting 5s...');
    await new Promise(r => setTimeout(r, 5000));

    console.log('[QA] Loading video...');
    await send('Runtime.evaluate', {
      expression: `
        fetch('student_input_sample.mp4')
          .then(r => r.blob())
          .then(b => setupStudentVideoFromBlob(b, 'student_input_sample.mp4'));
      `
    });

    await new Promise(r => setTimeout(r, 6000));

    const evalDebug = await send('Runtime.evaluate', {
      expression: `(() => {
        const vid = studentVideoElem;
        const mask = latestSegmentMask;
        
        let maskStats = null;
        if (mask) {
          const c = document.createElement('canvas');
          c.width = 640; c.height = 360;
          const cx = c.getContext('2d');
          cx.drawImage(mask, 0, 0, 640, 360);
          const d = cx.getImageData(0, 0, 640, 360).data;
          let maxVal = 0, minVal = 255, aboveCutoff = 0;
          for (let i = 0; i < d.length; i += 4) {
            const v = Math.max(d[i], d[i+1], d[i+2], d[i+3]);
            if (v > maxVal) maxVal = v;
            if (v < minVal) minVal = v;
            if (v > 95) aboveCutoff++;
          }
          maskStats = { minVal, maxVal, aboveCutoff, first10Pixels: Array.from(d.slice(0, 40)) };
        }

        return {
          studentCropLeft: typeof studentCropLeft !== 'undefined' ? studentCropLeft : null,
          studentCropRight: typeof studentCropRight !== 'undefined' ? studentCropRight : null,
          studentCropBottom: typeof studentCropBottom !== 'undefined' ? studentCropBottom : null,
          studentChromaTolerance,
          maskStats
        };
      })()`,
      returnByValue: true
    });

    console.log('DEBUG DETAILS:', JSON.stringify(evalDebug.result.value, null, 2));

    const canvasDataUrl = await send('Runtime.evaluate', {
      expression: `document.getElementById('mainCanvas').toDataURL('image/png')`
    });
    if (canvasDataUrl.result.value) {
      const b64 = canvasDataUrl.result.value.replace(/^data:image\/png;base64,/, '');
      fs.writeFileSync('test_studio_canvas_only.png', Buffer.from(b64, 'base64'));
      console.log('[QA] Saved test_studio_canvas_only.png');
    }

  } catch (err) {
    console.error(err);
  } finally {
    edgeProc.kill();
    server.close();
    process.exit(0);
  }
});
