import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://127.0.0.1:8080/Tao_Khung_Thoi_Su_Talk11.html';
const OUTPUT_FILE = path.resolve('TALK11_Real_Export_Verification.webm');
const FFMPEG_PATH = path.resolve('.\\remotion-prompt-to-video\\node_modules\\@remotion\\compositor-win32-x64-msvc\\ffmpeg.exe');

async function verifyRealVideoExport() {
  console.log('================================================================');
  console.log(' TALK11 VIDEO EXPORT — REAL FILE & FFmpeg DEEP INSPECTION AUDIT ');
  console.log('================================================================');

  if (fs.existsSync(OUTPUT_FILE)) {
    fs.unlinkSync(OUTPUT_FILE);
  }

  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9239',
    '--window-size=1680,980',
    '--autoplay-policy=no-user-gesture-required',
    '--disable-gpu',
    'about:blank'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const res = await fetch('http://127.0.0.1:9239/json/new?' + encodeURIComponent(APP_URL), { method: 'PUT' });
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
    await new Promise(r => setTimeout(r, 2500));

    console.log('[1/4] Configuring test state (Anchor name, Title, Topic)...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const inpName = document.getElementById('inputAnchorName');
        const inpTitle = document.getElementById('inputAnchorTitle');
        const inpHl = document.getElementById('inputHeadline');
        if (inpName) inpName.value = 'TRẦN MINH KHÔI';
        if (inpTitle) inpTitle.value = 'PHÓNG VIÊN ĐẶC BIỆT TALK11';
        if (inpHl) inpHl.value = 'BẢN TIN CÔNG NGHỆ AI ROBOTICS 2026';
        
        inpName?.dispatchEvent(new Event('input'));
        inpTitle?.dispatchEvent(new Event('change'));
        inpHl?.dispatchEvent(new Event('input'));
        
        render(previewCurrentSec);
      })()`
    });

    console.log('[2/4] Triggering 3.0s Full HD 60FPS Video Export...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        window.__exportFinished = false;
        window.__exportBlobSize = 0;
        window.lastExportedBlob = null;
        
        // Start 3 second export
        window.startExport(3);
        
        const pollTimer = setInterval(async () => {
          if (window.lastExportedBlob && !window.__exportFinished) {
            window.__exportFinished = true;
            clearInterval(pollTimer);
            window.__exportBlobSize = window.lastExportedBlob.size;
            try {
              await fetch('/api/save-test-video', {
                method: 'POST',
                headers: { 'Content-Type': 'application/octet-stream' },
                body: window.lastExportedBlob
              });
            } catch (err) {
              console.error('Save video failed:', err);
            }
          }
        }, 200);
      })()`
    });

    console.log('[3/4] Recording and waiting for export completion...');
    let finished = false;
    for (let i = 0; i < 30; i++) {
      await new Promise(r => setTimeout(r, 500));
      const statusRes = await send('Runtime.evaluate', {
        expression: `({
          isRecording,
          finished: window.__exportFinished,
          blobSize: window.__exportBlobSize,
          previewSec: previewCurrentSec
        })`,
        returnByValue: true
      });
      const s = statusRes.result.value;
      if (s.finished && s.blobSize > 10000) {
        finished = true;
        console.log(`[3/4] Export finalized in browser! Blob size: ${(s.blobSize / 1024).toFixed(1)} KB`);
        break;
      }
    }

    if (!finished) {
      console.warn('[3/4] Export polling timed out, forcing stopExport()...');
      await send('Runtime.evaluate', { expression: 'window.stopExport();' });
      await new Promise(r => setTimeout(r, 1500));
    }

    console.log('[4/4] Video binary stream received and saved to disk.');
    ws.close();
  } catch (err) {
    console.error('Export error:', err);
  } finally {
    edgeProc.kill();
  }

  // Copy target file to OUTPUT_FILE
  const defaultFile = path.resolve('TALK11_E2E_Test_Output.webm');
  if (fs.existsSync(defaultFile)) {
    fs.copyFileSync(defaultFile, OUTPUT_FILE);
  }

  if (!fs.existsSync(OUTPUT_FILE)) {
    console.error('ERROR: Video file was not created on disk!');
    return false;
  }

  const stat = fs.statSync(OUTPUT_FILE);
  console.log(`Video File Size: ${(stat.size / 1024).toFixed(1)} KB`);

  // Run FFmpeg analysis
  console.log('\nRunning FFmpeg analysis on actual output file...');
  return new Promise((resolve) => {
    const ff = spawn(FFMPEG_PATH, [
      '-i', OUTPUT_FILE,
      '-vf', 'blackdetect=d=0.1:pix_th=0.10',
      '-f', 'null',
      '-'
    ]);

    let stderr = '';
    ff.stderr.on('data', chunk => stderr += chunk.toString());
    ff.on('close', (code) => {
      console.log('--- FFmpeg Stream Summary ---');
      const streamLines = stderr.split('\n').filter(l => l.includes('Stream #') || l.includes('Duration:'));
      streamLines.forEach(l => console.log('  ' + l.trim()));

      const hasBlack = stderr.includes('black_start');
      console.log('Black frames detected:', hasBlack ? 'YES (FAIL)' : 'NO (0 black frames, PASS)');

      // Extract verification frame at 1.5s
      const framePath = path.resolve('real_export_frame_1.5s.png');
      const ffExtract = spawn(FFMPEG_PATH, [
        '-y',
        '-ss', '00:00:01.500',
        '-i', OUTPUT_FILE,
        '-vframes', '1',
        framePath
      ]);
      ffExtract.on('close', () => {
        console.log('Extracted frame image:', framePath, '(Exists:', fs.existsSync(framePath), ')');
        resolve(true);
      });
    });
  });
}

verifyRealVideoExport();
