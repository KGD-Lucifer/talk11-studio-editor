import { spawn } from 'child_process';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'file:///' + path.resolve('Tao_Khung_Thoi_Su_Talk11.html').replace(/\\/g, '/');

async function test() {
  console.log('Testing Playback Smoothness & Zero-Seeking Loop in Headless Edge...');
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9292',
    '--window-size=1680,980',
    '--disable-gpu',
    'about:blank'
  ]);

  let res = null;
  for (let i = 0; i < 15; i++) {
    await new Promise(r => setTimeout(r, 400));
    try {
      res = await fetch('http://127.0.0.1:9292/json/new?' + encodeURIComponent(APP_URL), { method: 'PUT' });
      if (res.ok) break;
    } catch(e) {}
  }

  const target = await res.json();
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);

  let idSeq = 1;
  const pending = new Map();
  function send(method, params = {}) {
    return new Promise((resolve) => {
      const id = idSeq++;
      pending.set(id, resolve);
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) {
      const resolve = pending.get(msg.id);
      pending.delete(msg.id);
      resolve(msg);
    }
  };

  await send('Page.enable');
  await send('Runtime.enable');
  await new Promise(r => setTimeout(r, 2000));

  const playbackEval = await send('Runtime.evaluate', {
    expression: `(async () => {
      // Create mock video stream
      const c = document.createElement('canvas');
      c.width = 640; c.height = 360;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#FF8C00'; ctx.fillRect(100, 50, 200, 250);
      const stream = c.captureStream(30);
      const vid = document.createElement('video');
      vid.srcObject = stream;
      vid.muted = true;
      document.body.appendChild(vid);
      await vid.play();

      studentVideoElem = vid;
      enableStudentVideo = true;
      rawStudentVideoDuration = 30;
      studentVideoDuration = 30;

      // Start timeline playback
      isTimelinePlaying = true;
      let seekCount = 0;
      vid.addEventListener('seeking', () => { seekCount++; });

      const startSec = previewCurrentSec;
      const t0 = performance.now();
      let framesCounted = 0;

      await new Promise(r => {
        const interval = setInterval(() => {
          framesCounted++;
          if (performance.now() - t0 >= 1500) {
            clearInterval(interval);
            r();
          }
        }, 16);
      });

      return {
        playedForMs: performance.now() - t0,
        seekCountDuringPlay: seekCount,
        previewCurrentSec,
        videoCurrentTime: vid.currentTime,
        isTimelinePlaying,
        isPaused: vid.paused
      };
    })()`,
    awaitPromise: true,
    returnByValue: true
  });

  console.log('Playback Smoothness Results:', playbackEval.result?.result?.value);
  ws.close();
  edgeProc.kill();
}

test().catch(console.error);
