import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://127.0.0.1:8080/Tao_Khung_Thoi_Su_Talk11.html';

async function testPage() {
  console.log('Launching headless Edge to verify CapCut cutout upgrade...');
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9244',
    '--window-size=1680,980',
    '--autoplay-policy=no-user-gesture-required',
    '--disable-gpu',
    'about:blank'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const res = await fetch('http://127.0.0.1:9244/json/new?' + encodeURIComponent(APP_URL), { method: 'PUT' });
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

    await new Promise((resolve, reject) => {
      ws.onopen = resolve;
      ws.onerror = reject;
    });

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
    await new Promise(r => setTimeout(r, 3000));

    // Check variables in page
    const checkRes = await send('Runtime.evaluate', {
      expression: `(() => {
        return {
          studentAiErodeRadius,
          studentChromaTolerance,
          studentChromaFeather,
          beautyBrightness,
          beautyPreset,
          beautyContrast,
          beautySaturation,
          beautySmoothness,
          sliderAiErodeVal: document.getElementById('sliderAiErode')?.value,
          sliderAiErodeLbl: document.getElementById('valAiErode')?.textContent,
          sliderBrightVal: document.getElementById('sliderBeautyBright')?.value,
          sliderBrightLbl: document.getElementById('valBeautyBright')?.textContent,
          activePreset: document.querySelector('#beautyPresetPills .btn-tint-pill.active')?.getAttribute('data-beauty'),
          title: document.title
        };
      })()`,
      returnByValue: true
    });

    console.log('Verified Page State:', JSON.stringify(checkRes.result.value, null, 2));

    // Take screenshot of preview area
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('capcut_upgrade_preview.png', Buffer.from(shot.data, 'base64'));
    console.log('[OK] Captured screenshot: capcut_upgrade_preview.png');

    ws.close();
  } catch (err) {
    console.error('Error during test:', err);
  } finally {
    edgeProc.kill();
  }
}

testPage();
